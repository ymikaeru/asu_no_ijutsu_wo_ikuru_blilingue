# -*- coding: utf-8 -*-
"""Correções mecânicas de erros sistemáticos de OCR no content_ja.
Regras conservadoras (lookbehind para palavras legítimas); relatório de cada substituição."""
import io, json, re

F = r"D:\Mioshie_Sites\Asu_No_Ijutsu_Wo_Ikiru_bilingue\ashita-no-ijitsu.bilingual.json"
data = json.load(io.open(F, encoding="utf-8"))

RULES = [
    # OCR leu 信 como 言 (perdeu o radical 亻) ou comeu o 信
    ("言仰", re.compile(r"言仰"), "信仰"),                              # 無言仰者 -> 無信仰者
    ("言者", re.compile(r"(?<![預証発助宣])言者"), "信者"),             # 言者 -> 信者 (preserva 預言者 etc.)
    ("仰者", re.compile(r"(?<![信])仰者"), "信仰者"),                   # 仰者 -> 信仰者
    ("もらた", re.compile(r"もらた"), "もらった"),
    ("いただいたかず", re.compile(r"いただいたかず"), "いただかず"),
    ("メシや", re.compile(r"メシや(?!か)"), "メシヤ"),
    ("昭和338年", re.compile(r"昭和338年"), "昭和38年"),               # PT confirma 1963
]
TRAILING_JUNK = re.compile(r"\n\n[\s()（）\\\d.、]+$")   # enumerador do próximo heading que caiu na fatia
TRAILING_NUM = re.compile(r"(?<=[ぁ-ん一-鿿。」])\d{1,2}\\\)$")  # ex: 「…お使6\)」

counts = {}
trunc_watch = []
def walk(secs, path):
    for i, s in enumerate(secs, 1):
        p = ".".join(path + [str(i)])
        t = s.get("content_ja")
        if t:
            for name, rx, rep in RULES:
                t2, n = rx.subn(rep, t)
                if n:
                    counts[name] = counts.get(name, 0) + n
                    t = t2
            t2 = TRAILING_JUNK.sub("", t)
            if t2 != t:
                counts["lixo-final"] = counts.get("lixo-final", 0) + 1
                t = t2
            t2 = TRAILING_NUM.sub("", t)
            if t2 != t:
                counts["num-final"] = counts.get("num-final", 0) + 1
                trunc_watch.append((p, t2[-30:]))
                t = t2
            s["content_ja"] = t
        walk(s.get("children", []), path + [str(i)])
walk(data["sections"], [])

io.open(F, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=2))
print("substituicoes:", counts)
print("fins possivelmente truncados (conferir contra scan):")
for p, tail in trunc_watch:
    print(" ", p, "…", tail)
