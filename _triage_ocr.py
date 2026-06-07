# -*- coding: utf-8 -*-
"""Triagem v2 (alta precisão) de anomalias de OCR no content_ja.
Detectores: numeros PT ausentes no JA, eras impossíveis, ASCII em CJK,
kana-duplicado filtrado, parágrafo sem pontuação final, padrões conhecidos.
Não altera o JSON; só relatório."""
import io, json, re, collections

DIR = r"D:\Mioshie_Sites\Asu_No_Ijutsu_Wo_Ikiru_bilingue"
data = json.load(io.open(DIR + r"\ashita-no-ijitsu.bilingual.json", encoding="utf-8"))

nodes = []
def walk(secs, path):
    for i, s in enumerate(secs, 1):
        p = ".".join(path + [str(i)])
        if s.get("content_ja"):
            nodes.append((p, s))
        walk(s.get("children", []), path + [str(i)])
walk(data["sections"], [])

ANCHORS = [(1, 11), (437, 73), (719, 121), (1206, 149), (1963, 202), (4264, 338), (5126, 391)]
def page_of(line):
    for (l1, p1), (l2, p2) in zip(ANCHORS, ANCHORS[1:]):
        if l1 <= line <= l2:
            return round(p1 + (line - l1) * (p2 - p1) / (l2 - l1))
    return None

# ---------- números ----------
KD = {"〇":0,"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9}
def kanji2int(t):
    # converte 二十二 / 百 / 三千 simples
    total, cur = 0, 0
    for c in t:
        if c in KD: cur = cur*10 + KD[c] if cur and KD[c] else KD[c] if not cur else cur+KD[c]
        elif c == "十": total += (cur or 1)*10; cur = 0
        elif c == "百": total += (cur or 1)*100; cur = 0
        elif c == "千": total += (cur or 1)*1000; cur = 0
        else: return None
    return total + cur

ERA_BASE = {"昭和": 1925, "大正": 1911, "平成": 1988, "明治": 1867}
def ja_numbers(t):
    t = t.replace("，", "").replace(",", "")
    ns = set()
    for m in re.finditer(r"\d+", t):
        ns.add(int(m.group(0)))
    for m in re.finditer(r"[〇一二三四五六七八九十百千]{2,}", t):
        v = kanji2int(m.group(0))
        if v: ns.add(v)
    # anos de era -> ano ocidental
    for era, base in ERA_BASE.items():
        for m in re.finditer(era + r"(\d{1,2}|[〇一二三四五六七八九十]{1,4})年", t):
            g = m.group(1)
            v = int(g) if g.isdigit() else kanji2int(g)
            if v: ns.add(base + v)
    return ns

def pt_numbers(t):
    t = re.sub(r"(\d)\.(\d{3})", r"\1\2", t)   # 2.000 -> 2000
    return {int(m.group(0)) for m in re.finditer(r"\d+", t)}

# ---------- detectores ----------
RED_OK = re.compile(r"(いろ|ただ|どん|ます|つく|しみ|それ|たま|わざ|もの|ねが|かさ|こも|べつ|ちょ|やや|ぼつ|either)")
ERA_RANGE = {"昭和": (1, 64), "大正": (1, 15), "平成": (1, 31), "明治": (1, 45)}
# kanji EXCLUSIVAMENTE simplificado-chinês (inexistentes em japonês) — alta precisão
SIMP = set("刘这们对说时间问题东发样开关变难单证买乐乡亚产亲亿仅仓仪俩价众优伟传滟谁误读语论让识词请谢")

findings = []
for path, s in nodes:
    t, pt = s["content_ja"], s.get("content") or ""
    lines = s.get("ja_content_lines", [None, None])
    pg = page_of(lines[0]) if lines[0] else None
    f = []
    # 1. números do PT ausentes no JA (ignora pequenos <=3: ordinais/numeração)
    npt, nja = pt_numbers(pt), ja_numbers(t)
    missing = {n for n in npt - nja if n > 3}
    # tolerâncias: ano vs idade etc. — só reporta se nem vizinho ±1 existe
    missing = {n for n in missing if not ({n-1, n+1} & nja)}
    if missing:
        f.append(("numeros-PT-sem-JA", sorted(missing)))
    # 2. eras impossíveis
    for era, (lo, hi) in ERA_RANGE.items():
        for m in re.finditer(era + r"(\d+)", t):
            v = int(m.group(1))
            if not (lo <= v <= hi):
                f.append(("era-impossivel", m.group(0)))
    # 3. ASCII no meio de CJK (l8, MR exceto siglas conhecidas)
    for m in re.finditer(r"[ぁ-ん一-鿿][a-zl|][ぁ-ん一-鿿]", t):
        f.append(("ascii-em-cjk", f"…{t[max(0,m.start()-8):m.end()+8]}…"))
    # 4. kanji simplificado chinês
    for c in set(t) & SIMP:
        i = t.index(c)
        f.append(("kanji-chines", f"{c} …{t[max(0,i-10):i+10]}…"))
    # (kana-duplicado removido: reduplicação é comum demais em japonês — só falso positivo)
    # 6. parágrafo sem pontuação final
    for parag in t.split("\n\n"):
        last = parag.strip()[-1:]
        if last and last not in "。」』！？）—…す」":
            f.append(("paragrafo-sem-fim", "…" + parag.strip()[-25:]))
    # 7. padrões de erro conhecidos
    for m in re.finditer(r"メシ[やゃ](?!か)|(?<![信預証発助宣])言者|(?<!信)仰者|もらた|いただいたかず|り得ても", t):
        f.append(("padrao-conhecido", f"…{t[max(0,m.start()-10):m.end()+10]}…"))
    if f:
        findings.append((path, pg, lines, f))

total = sum(len(x[3]) for x in findings)
print(f"secoes com achados: {len(findings)}/{len(nodes)} | total: {total}\n")
kinds_all = collections.Counter(k for _, _, _, fs in findings for k, _ in fs)
print("por tipo:", dict(kinds_all), "\n")
for path, pg, lines, f in findings:
    print(f"== {path}  (OCR L{lines[0]}-{lines[1]}, ~p.{pg})")
    for k, detail in f:
        print(f"   [{k}] {detail}")
