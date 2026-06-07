# -*- coding: utf-8 -*-
"""Corrige títulos JA suspeitos contra o scan e marca os reconstruídos como confirmados."""
import io, json

F = r"D:\Mioshie_Sites\Asu_No_Ijutsu_Wo_Ikiru_bilingue\ashita-no-ijitsu.bilingual.json"
data = json.load(io.open(F, encoding="utf-8"))

nodes = {}
def walk(secs, path):
    for i, s in enumerate(secs, 1):
        p = ".".join(path + [str(i)])
        nodes[p] = s
        walk(s.get("children", []), path + [str(i)])
walk(data["sections"], [])

FIXES = {
    "2.3":   ("大先生を奉", "大先生を信奉", "p.34 (Scans/11-72.pdf)"),
    "2.4.5": ("罪の許し―「八衢へ上げあげる」", "罪の許し―「八衢へ上げてあげる」", "p.97 (Scans/73-121.pdf)"),
    "2.7":   ("メシャ降誕", "メシヤ降誕", "p.149 (Scans/122-173 page fix .pdf)"),
    "3.2.2": ("明主様の神智 | 神幽現、過現末の一切が分かる", "明主様の神智―神幽現、過現未の一切が分かる", "p.203 (Scans/174-223.pdf)"),
    "3.7.7": ("人の眼はり得ても神の眼は偽り得ない", "人の眼は偽り得ても神の眼は偽り得ない", "p.338 (Scans/325-391.pdf)"),
}
for path, (old, new, src) in FIXES.items():
    s = nodes[path]
    assert s["title_ja"] == old, (path, s["title_ja"])
    s["title_ja"] = new
    s["ja_note"] = f"Título corrigido contra o scan do livro, {src}. OCR original: 「{old}」."
    if path in data.get("ja_ocr_suspect_paths", []):
        data["ja_ocr_suspect_paths"].remove(path)

# reconstruído 2.4.6 confirmado idêntico no scan
s = nodes["2.4.6"]
assert s["title_ja"] == "救世主のご神格ー『私はミロク』"
s["ja_note"] = "Título reconstruído confirmado contra o scan, p.101 (Scans/73-121.pdf): 「救世主のご神格―『私はミロク』」."

data["note_scan_verification"] = (
    "2026-06-08: títulos ja_ocr_suspect corrigidos e títulos reconstruídos (2.4.6, 2.5.5, 2.7.2) "
    "confirmados contra os scans em Scans/*.pdf. Lacunas de página do OCR (2.5.5, 2.7.1, 2.7.2) "
    "recuperadas por transcrição do scan (p.116, p.150-151). Offsets dos PDFs: 11-72.pdf começa na p.13 "
    "do livro (índice = página-13); demais PDFs: índice = página - primeiro número do nome do arquivo.")

io.open(F, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=2))
print("OK. ja_ocr_suspect_paths restante:", data["ja_ocr_suspect_paths"])
