# -*- coding: utf-8 -*-
"""Correções de OCR descobertas ao verificar a Seção B do REVISAO_PT (contra o scan)."""
import io, json

F = r"D:\Mioshie_Sites\Asu_No_Ijutsu_Wo_Ikiru_bilingue\ashita-no-ijitsu.bilingual.json"
data = json.load(io.open(F, encoding="utf-8"))
nodes = {}
def walk(secs, path):
    for i, s in enumerate(secs, 1):
        p = ".".join(path + [str(i)]); nodes[p] = s
        walk(s.get("children", []), path + [str(i)])
walk(data["sections"], [])

# 2.5.9: ano (l->1) + 疥 perdido (癬 -> 疥癬), confirmado no scan p.131
s = nodes["2.5.9"]
old = "昭和2l年12月から癬の浄化"
new = "昭和21年12月から疥癬の浄化"
assert old in s["content_ja"], repr([x for x in s["content_ja"] if False])
s["content_ja"] = s["content_ja"].replace(old, new)
s["ja_note_content"] = (s.get("ja_note_content","") + " OCR '昭和2l年' -> '昭和21年'; "
    "弥癬/癬 -> 疥癬 (scan p.131, titulo 「疥癬の浄化」). PT '1946' confirmado correto.").strip()

# 3.1.2: 昭利->昭和, 21年代->20年代, 半は->半ば (scan p.199)
s = nodes["3.1.2"]
old = "昭利21年代の半は頃"
new = "昭和20年代の半ば頃"
assert old in s["content_ja"]
s["content_ja"] = s["content_ja"].replace(old, new)
s["ja_note_content"] = (s.get("ja_note_content","") + " OCR '昭利21年代の半は頃' -> '昭和20年代の半ば頃' "
    "(scan p.199). ATENCAO: PT diz 'meados de 1946', mas o livro diz 昭和20年代半ば (~1950); erro no PT.").strip()
# foto p.199
s.setdefault("images", []).append({
    "book_page": 199, "source_pdf": "Scans/174-223.pdf",
    "caption_ja": "明主様のご遺品の羽織紐",
    "caption_pt": "Cordão de haori (haori-himo), relíquia de Meishu-Sama.",
    "file": None})

# global: 弥癬 / 弥癖 -> 疥癬 (erro sistematico de OCR; confirmado no scan p.131/132)
tot = 0
def fix_global(secs):
    global tot
    for s in secs:
        if s.get("content_ja"):
            c = s["content_ja"]
            n = c.count("弥癬") + c.count("弥癖")
            if n:
                s["content_ja"] = c.replace("弥癬", "疥癬").replace("弥癖", "疥癬")
                tot += n
        fix_global(s.get("children", []))
fix_global(data["sections"])

io.open(F, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=2))
print("2.5.9 e 3.1.2 corrigidos; foto p.199 catalogada")
print("弥癬/弥癖 -> 疥癬 (global):", tot, "ocorrencias")
