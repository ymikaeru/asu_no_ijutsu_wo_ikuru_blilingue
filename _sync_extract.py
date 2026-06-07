# -*- coding: utf-8 -*-
"""Passo 2: extrair content_ja do 'All OCR 11 - 391.md' usando os anchors do passo 1,
limpar (des-espaçar, rejuntar quebras de página) e validar contra o PT (anos).
--write para gravar no JSON; sem flag, só relatório."""
import io, json, re, difflib, sys

DIR = r"D:\Mioshie_Sites\Asu_No_Ijutsu_Wo_Ikiru_bilingue"
OCR = DIR + r"\All OCR 11 - 391.md"
JSONF = DIR + r"\ashita-no-ijitsu.bilingual.json"
WRITE = "--write" in sys.argv

ocr_lines = io.open(OCR, encoding="utf-8").read().splitlines()
data = json.load(io.open(JSONF, encoding="utf-8"))

# ---------- matching (idêntico ao passo 1) ----------
def norm(s):
    s = re.sub(r"[\s　]+", "", s)
    return s.replace("#", "").replace("*", "").replace("_", "")

def strip_enum(s):
    return re.sub(r"^[（）()0-9①-⑮\.、．]+", "", s)

nodes = []
def walk(secs, path):
    for i, s in enumerate(secs, 1):
        p = path + [str(i)]
        nodes.append([".".join(p), s, None])
        walk(s.get("children", []), p)
walk(data["sections"], [])
bypath = {n[0]: n for n in nodes}

ordered = sorted([n for n in nodes if n[1].get("ja_src_line") is not None],
                 key=lambda n: n[1]["ja_src_line"])
nlines = [norm(l) for l in ocr_lines]

def score(key, li):
    nl = nlines[li]
    if not nl or len(nl) > len(key) + 30:
        return 0.0
    sc = difflib.SequenceMatcher(None, key, strip_enum(nl)).ratio()
    if key and key in nl:
        sc = max(sc, 0.99)
    return sc

def best_in(key, lo, hi):
    b = (None, 0.0)
    for li in range(lo, hi):
        sc = score(key, li)
        if sc > b[1]:
            b = (li, sc)
        if sc >= 0.99:
            break
    return b

cursor = 0
for n in ordered:
    key = strip_enum(norm(n[1]["title_ja"]))
    li, sc = best_in(key, cursor, len(ocr_lines))
    if li is not None and sc >= 0.90:
        n[2] = li
        cursor = li + 1
for idx, n in enumerate(ordered):
    if n[2] is not None:
        continue
    lo = next((ordered[j][2] + 1 for j in range(idx - 1, -1, -1) if ordered[j][2] is not None), 0)
    hi = next((ordered[j][2] for j in range(idx + 1, len(ordered)) if ordered[j][2] is not None), len(ocr_lines))
    key = strip_enum(norm(n[1]["title_ja"]))
    li, sc = best_in(key, lo, hi)
    if li is not None and sc >= 0.55:
        n[2] = li

assert all(n[2] is not None for n in ordered), "anchor faltando"
anchors = sorted(n[2] for n in ordered)
assert anchors == sorted(set(anchors)), "anchor duplicado"

# ---------- fatias (0-based, [start, end) de conteúdo após o heading) ----------
slices = {}
anc = sorted(ordered, key=lambda n: n[2])
for i, n in enumerate(anc):
    start = n[2] + 1
    end = anc[i + 1][2] if i + 1 < len(anc) else len(ocr_lines)
    slices[n[0]] = [start, end]

# overrides manuais (1-based inclusivo -> convertido), seções reconstruídas e vizinhas
def rng(a, b):  # linhas 1-based inclusivas -> 0-based [start, end)
    return [a - 1, b]
slices["2.4.5"] = rng(590, 621)
slices["2.4.6"] = rng(622, 632)
slices["2.5.4"] = rng(687, 698)
slices["2.5.5"] = rng(700, 708)
slices["2.7.1"] = rng(1207, 1217)
slices["2.7.2"] = rng(1219, 1245)

JA_NOTES = {
    "2.5.5": "Início da seção perdido no OCR (salto de página após L698); texto começa no meio de uma frase.",
    "2.7.1": "Fim da seção perdido no OCR (L1217 termina no meio de uma frase; salto de página).",
    "2.7.2": "Início da seção perdido no OCR (texto começa no meio de uma frase, 「ブルのスーツ」=ダブルのスーツ).",
}

# ---------- limpeza ----------
PUNCT_END = tuple("。」』！？）!?）")
def despace(line):
    toks = line.split()
    if len(toks) >= 4 and sum(1 for t in toks if len(t) == 1) / len(toks) >= 0.7:
        return re.sub(r"[\s　]+", "", line)
    return line.strip()

def clean_slice(start, end):
    lines = [despace(l) for l in ocr_lines[start:end]]
    lines = [("" if re.fullmatch(r"[#\s*_]*", l) else l) for l in lines]  # descarta headings vazios do OCR
    # blocos separados por linhas vazias
    blocks, cur = [], []
    for l in lines:
        if l:
            cur.append(l)
        elif cur:
            blocks.append(cur); cur = []
    if cur:
        blocks.append(cur)
    # junta linhas dentro do bloco: quebra de linha vira nada (wrap no meio da frase)
    # ou \n se a linha anterior termina com pontuação final
    joined = []
    for b in blocks:
        out = b[0]
        for l in b[1:]:
            out += ("\n" + l) if out.endswith(PUNCT_END) else l
        joined.append(out)
    # mescla blocos partidos por salto de página (bloco não termina em pontuação)
    merged = []
    for b in joined:
        if merged and not merged[-1].endswith(PUNCT_END):
            merged[-1] += b
        else:
            merged.append(b)
    return "\n\n".join(merged).strip()

# ---------- validação PT x JA (anos) ----------
ERA = {"昭和": 1925, "大正": 1911, "平成": 1988, "明治": 1867}
def years_ja(t):
    t = re.sub(r"[\s　]+", "", t)
    ys = set()
    for era, base in ERA.items():
        for m in re.finditer(era + r"(\d{1,2})年", t):
            ys.add(base + int(m.group(1)))
    for m in re.finditer(r"(19\d\d|20\d\d)年", t):
        ys.add(int(m.group(1)))
    return ys

def years_pt(t):
    return {int(m.group(0)) for m in re.finditer(r"\b(19\d\d|20\d\d)\b", t)}

report_bad = []
results = {}
for path, n in bypath.items():
    s = n[1]
    if path not in slices:
        continue
    start, end = slices[path]
    ja = clean_slice(start, end)
    results[path] = (ja, start + 1, end)  # guarda 1-based p/ ja_content_lines
    pt = s.get("content") or ""
    if not pt:
        continue
    ypt, yja = years_pt(pt), years_ja(ja)
    if ypt:
        inter = ypt & yja
        if not inter:
            report_bad.append((path, sorted(ypt), sorted(yja)))

# proporção de tamanho PT/JA como segundo sinal
print(f"{'path':8} {'linhas':>11} {'lenJA':>6} {'lenPT':>6} ratio")
for path in [n[0] for n in nodes]:
    if path not in results:
        continue
    s = bypath[path][1]
    ja, a, b = results[path]
    pt = s.get("content") or ""
    if not pt:
        if len(ja) > 40:
            print(f"{path:8} {a:>5}-{b:<5} lenJA={len(ja)}  <<< JA sem PT (nó-galho com texto?)")
        continue
    r = len(ja) / max(1, len(pt))
    flag = "  <<< RATIO" if (r < 0.45 or r > 1.6) else ""
    print(f"{path:8} {a:>5}-{b:<5} {len(ja):>6} {len(pt):>6} {r:.2f}{flag}")

print("\nseções sem nenhum ano em comum (PT tem ano, JA não):")
for p, ypt, yja in report_bad:
    print(" ", p, "PT:", ypt, "JA:", yja)

# ---------- gravação ----------
if WRITE:
    for path, (ja, a, b) in results.items():
        s = bypath[path][1]
        if not (s.get("content") or path in ("2.4.6", "2.5.5", "2.7.2")):
            continue  # nós-galho sem conteúdo PT não recebem content_ja
        s["content_ja"] = ja
        s["ja_content_lines"] = [a, b]
        if path in JA_NOTES:
            s["ja_note_content"] = JA_NOTES[path]
    # re-ancora ja_src_line para o arquivo atual
    for n in ordered:
        n[1]["ja_src_line"] = n[2] + 1
    data["source_ja"] = "All OCR 11 - 391.md"
    data["note_content_ja"] = ("content_ja extraído de 'All OCR 11 - 391.md' por ancoragem de títulos "
        "(ja_content_lines = intervalo 1-based inclusivo de linhas). Texto é OCR bruto: des-espaçado e com "
        "parágrafos rejuntados mecanicamente, mas erros de OCR NÃO foram corrigidos. "
        "ja_note_content marca seções com lacunas de página no OCR.")
    io.open(JSONF, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=2))
    print("\nGRAVADO em", JSONF)
else:
    print("\n(dry-run; use --write para gravar)")
