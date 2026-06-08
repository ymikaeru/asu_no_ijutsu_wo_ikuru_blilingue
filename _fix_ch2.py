# -*- coding: utf-8 -*-
"""Revisão do Capítulo 2 (seção 3): correção de OCR verificada no scan + catálogo de fotos."""
import io, json

F = r"D:\Mioshie_Sites\Asu_No_Ijutsu_Wo_Ikiru_bilingue\ashita-no-ijitsu.bilingual.json"
data = json.load(io.open(F, encoding="utf-8"))
nodes = {}
def walk(secs, path):
    for i, s in enumerate(secs, 1):
        p = ".".join(path + [str(i)]); nodes[p] = s
        walk(s.get("children", []), path + [str(i)])
walk(data["sections"], [])

# 3.4.4: data da citação 「生と死」 corrigida contra o scan (p.250)
s = nodes["3.4.4"]
old = "（「生と死」昭和18：年0123日）"
new = "（「生と死」昭和18年10月23日）"
assert old in s["content_ja"]
s["content_ja"] = s["content_ja"].replace(old, new)
s["ja_note_content"] = ("OCR '昭和18：年0123日' -> '昭和18年10月23日' (scan p.250). "
    "ATENCAO: o PT diz '23 de janeiro de 1943', mas o livro diz 10月(outubro); erro de mes no PT.")
print("3.4.4 corrigido:", new)

# 3.7.7: fotos (p.339 x2, p.340 x1)
nodes["3.7.7"].setdefault("images", []).extend([
    {"book_page": 339, "source_pdf": "Scans/325-391.pdf",
     "caption_ja": "光陽教会の資格者らと共に（昭和38年2月、光陽教会玄関前）",
     "caption_pt": "Com os qualificados da Igreja Koyo (fevereiro de 1963, em frente à entrada da Igreja Koyo).",
     "file": None},
    {"book_page": 339, "source_pdf": "Scans/325-391.pdf",
     "caption_ja": "妻・繪子と五女・珠美（昭和38年2月、光陽教会玄関前）",
     "caption_pt": "Com a esposa Eko e a quinta filha Tamami (fevereiro de 1963, em frente à entrada da Igreja Koyo).",
     "file": None},
    {"book_page": 340, "source_pdf": "Scans/325-391.pdf",
     "caption_ja": "家族で（昭和51年8月19日、札幌空港）",
     "caption_pt": "Em família (19 de agosto de 1976, Aeroporto de Sapporo).",
     "file": None},
])
print("3.7.7: +3 fotos")

io.open(F, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=2))
print("gravado")
