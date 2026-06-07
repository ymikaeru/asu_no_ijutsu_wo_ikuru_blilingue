# -*- coding: utf-8 -*-
"""Revisão do Capítulo 1: correções de OCR verificadas contra o scan,
limpeza global de lixo de enumerador no fim das fatias, e catálogo de fotos."""
import io, json, re

F = r"D:\Mioshie_Sites\Asu_No_Ijutsu_Wo_Ikiru_bilingue\ashita-no-ijitsu.bilingual.json"
data = json.load(io.open(F, encoding="utf-8"))

nodes = {}
def walk(secs, path):
    for i, s in enumerate(secs, 1):
        p = ".".join(path + [str(i)])
        nodes[p] = s
        walk(s.get("children", []), path + [str(i)])
walk(data["sections"], [])

def repl(path, old, new, note=None):
    s = nodes[path]
    assert old in s["content_ja"], f"{path}: nao achei {old!r}"
    s["content_ja"] = s["content_ja"].replace(old, new, 1)
    if note:
        s["ja_note_content"] = (s.get("ja_note_content", "") + " " + note).strip()
    print(f"  {path}: {old!r} -> {new!r}")

# ---- correções verificadas contra o scan ----
repl("2.5.12", "5 、116人", "15、6人", "OCR '5、116人' corrigido para '15、6人' (scan p.138).")
repl("2.6.1", "肩徒数", "信徒数", "OCR '肩徒' -> '信徒' (信 lido como 肩).")
repl("2.8.3", "30万徒が5万に撤減", "30万信徒が5万に激減",
     "OCR '30万徒が5万に撤減' -> '30万信徒が5万に激減' (scan p.161: caiu 信; 撤->激).")
repl("2.3.9", "昭和7年12月30日", "昭和24年12月30日",
     "OCR '昭和7年' -> '昭和24年' (scan p.64: a obra impressa diz 昭和24年=1949). "
     "ATENCAO: o PT desta secao cita '1952' para 「宗教となる迄」, mas o livro fisico diz 昭和24年(1949); "
     "divergencia factual no PT a confirmar.")
# 昭和2年=1927 impossivel p/ palestra de Meishu-Sama; PT diz 1953=昭和28 (plausivel). Nao confirmado no scan.
repl("2.8.9", "講話昭和2年6月17日", "講話昭和28年6月17日",
     "OCR '昭和2年'(1927, impossivel) -> '昭和28年'(1953) conforme PT; nao verificado no scan, conferir no livro.")

# ---- catálogo de fotos (Cap.1, seção 2.8.9) ----
nodes["2.8.9"].setdefault("images", []).extend([
    {"book_page": 183, "source_pdf": "Scans/174-223.pdf",
     "caption_ja": "機関誌『21世紀のための健康科学』42号の対談記事。大事なところに赤線が引かれている",
     "caption_pt": "Artigo de entrevista na revista '21-Seiki no Tame no Kenko Kagaku' (Ciência da Saúde para o Século XXI), nº 42. As passagens importantes estão sublinhadas em vermelho.",
     "file": None},
    {"book_page": 184, "source_pdf": "Scans/174-223.pdf",
     "caption_ja": "地元の静岡新聞に掲載された、ショッキングなタイトルの書籍の広告",
     "caption_pt": "Anúncio, publicado no jornal local Shizuoka Shimbun, de um livro com título chocante ('As 47 Regras para Não Ser Morto pelo Médico', de Makoto Kondo).",
     "file": None},
])
print("  2.8.9: +2 fotos catalogadas")

# ---- limpeza global: bloco final só com enumerador/lixo ----
JUNK = re.compile(r"\n\n[\s()（）\\\d.、,]+$")
trunc = []
n_junk = 0
def clean(secs, path):
    global n_junk
    for i, s in enumerate(secs, 1):
        p = ".".join(path + [str(i)])
        t = s.get("content_ja")
        if t:
            t2 = JUNK.sub("", t)
            if t2 != t:
                n_junk += 1; t = t2; s["content_ja"] = t
            # detecta fim truncado real (sem pontuação terminal e não é lixo)
            tail = t.rstrip()[-1:]
            if tail and tail not in "。」』！？）—…":
                trunc.append((p, t.rstrip()[-30:]))
        clean(s.get("children", []), path + [str(i)])
clean(data["sections"], [])

io.open(F, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=2))
print(f"\nlixo de enumerador removido: {n_junk} secoes")
print("fins truncados reais (conferir no scan numa proxima rodada):")
for p, tail in trunc:
    print("  ", p, "…", tail)
