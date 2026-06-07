# -*- coding: utf-8 -*-
"""Remove linhas finais que são só lixo de enumerador (ex.: '3\\)', '(16)', '） 2', '(').
Idempotente. Não toca em fins truncados reais (que terminam em kanji/kana)."""
import io, json, re

F = r"D:\Mioshie_Sites\Asu_No_Ijutsu_Wo_Ikiru_bilingue\ashita-no-ijitsu.bilingual.json"
data = json.load(io.open(F, encoding="utf-8"))

PURE_JUNK = re.compile(r"^[\s()（）\\\d.、,]+$")
fixed = []
def clean(secs, path):
    for i, s in enumerate(secs, 1):
        p = ".".join(path + [str(i)])
        t = s.get("content_ja")
        if t:
            parts = t.split("\n")
            changed = False
            while parts and PURE_JUNK.match(parts[-1].strip() or "x") and parts[-1].strip():
                parts.pop(); changed = True
            if changed:
                s["content_ja"] = "\n".join(parts).rstrip()
                fixed.append((p, repr(t[-15:])))
        clean(s.get("children", []), path + [str(i)])
clean(data["sections"], [])

io.open(F, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=2))
print(f"linhas-lixo removidas em {len(fixed)} secoes:")
for p, tail in fixed:
    print("  ", p, tail)
