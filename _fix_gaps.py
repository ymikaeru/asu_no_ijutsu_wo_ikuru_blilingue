# -*- coding: utf-8 -*-
"""Recupera do scan (Scans/*.pdf) os trechos perdidos pelo OCR e corrige título 3.2.
Fontes: p.116 (gap 2.5.5), p.150-151 (gap 2.7.1/2.7.2), p.202 (título 3.2)."""
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

# ---------- 2.5.5 : início recuperado do scan p.116 ----------
s = nodes["2.5.5"]
assert s["content_ja"].startswith("ませんか。例えば"), s["content_ja"][:20]
rec_2_5_5 = (
    "この浄化療法は、宗教行為として捉えられやすい面があります。それは、いまだに戦中戦後と変わらないかと思います。"
    "浄化療法によって大先生に対して信仰的な心情が生まれるのもそうです。それらのことについて、私は、次のように語っていました。\n\n"
    "「この浄化療法は信仰じゃない。技術的に習得した結果、心身変化によってその有り難さ―感謝の気持ちは信仰の心理状態に移行する。"
    "宗教信者は祈りによって御利益を得ると言うし、こちらは有り難い事実を得て信仰状態に入るのです。こういうことは一般に多くあるではあり"
)
s["content_ja"] = rec_2_5_5 + s["content_ja"]
s["ja_note_content"] = "Início (perdido no OCR) recuperado do scan, livro p.116 (Scans/73-121.pdf). Título 「最大の尊敬者に最大の言葉」 confirmado contra o scan p.116."

# ---------- 2.7.1 : final recuperado do scan p.150-151 ----------
s = nodes["2.7.1"]
assert s["content_ja"].endswith("私の代理として立派に力をふ"), s["content_ja"][-25:]
rec_2_7_1 = (
    "るい、仕事ができるわけです。だから今言ったことをよく心に入れて大いにやって下さい」（講話　昭和29年4月12日）と述べられました。\n\n"
    "『私の代理』というお言葉の持つ意味の深さについては分かりませんが、帰りの汽車の中で、その時のお話を幾度となく思い返すうちに、"
    "あれは明主様のご遺言ではないか、経綸の大きな変わり目ではないか、と思われました。\n\n"
    "明主様は奈良県公会堂でお話をされてから室生寺に行かれ、その後、奈良ホテルで、幹部たちと一緒に会食をされました。"
    "ありがたいことに、私もお相伴にあずかりました。\n\n"
    "その席上、明主様は室生寺での神秘的な出来事「龍神のうれし涙」のお話をされました。"
    "内容は『東方之光』の下巻632頁から633頁に載っていますので、引用します。\n\n"
    "「きょうは、私は一日中うれしくてたまらない。この喜びは誰にもわからないだろう。きょう雨が降ったのは、あれは龍神が行なったのです。"
    "龍神というのは神様ですが、やはり罪のために龍神になったのです。それで五六七の御代の建設のため、神様のお手伝いをしたいのですが、"
    "龍神ではそれができない。それには、元の神格に返らなくてはならない。そうなるには光に浴するしかないのです。"
    "それできょう、私がここに来るのがわかったので、お光に浴するわけです。それは何万という龍神です。その感謝を雨で表わしたのです。"
    "私の車の前を雨が降って行くのです。その龍神の感謝の気持ちが私に来るので、涙が出るほどうれしいのです」\n\n"
    "この話が終わり、少し息を継がれた後のことです。もうこれでおしまいだなと思った時に、明主様は言葉を継がれたのです。"
    "そして『私は必要なことはみんな書いた』と仰ったのです。\n\n"
    "その日、明主様は奈良ホテルに泊まられ、翌朝、同ホテルを後にして、吉野山へと向かわれました。"
    "私は、奈良ホテルでお見送りをして、車が出発した後、新潟に帰りました。\n\n"
    "『私は必要なことはみんな書いた』とのお言葉が、私には不思議に思えて、耳から離れませんでした。"
    "お歌に「四十五歳吾真実となりて立ち現はれ説きし悉真理なりける」というのがあります。\n\n"
    "今にして思えば、明主様はメシヤとなられ、2カ月間メシヤとして過ごされ、12月23日に明主様御降誕祭を斎行されたことによって、"
    "見真実となられた昭和元年から30年間の現界におけるご神業を完結されて、天界へとお帰りになられたのだと理解しています。"
)
s["content_ja"] = s["content_ja"] + rec_2_7_1
s["ja_note_content"] = "Final (perdido no OCR) recuperado do scan, livro p.150-151 (Scans/122-173 page fix .pdf)."

# ---------- 2.7.2 : início recuperado do scan p.151 ----------
s = nodes["2.7.2"]
assert s["content_ja"].startswith("ブルのスーツ"), s["content_ja"][:15]
rec_2_7_2 = (
    "奈良県公会堂におけるご講話から約2カ月後のことです。\n\n"
    "本部から直接電話があり、碧雲荘に礼服で来るようにとのことでした。"
    "そして昭和29年6月5日、私はモーニングを着てご面会に上がらせていただきました。\n\n"
    "ご面会者は役員や75人の教会長など総勢150人ほどで、男性は皆モーニングや礼装用のダ"
)
s["content_ja"] = rec_2_7_2 + s["content_ja"]
s["ja_note_content"] = "Início (perdido no OCR) recuperado do scan, livro p.151 (Scans/122-173 page fix .pdf). Título 「碧雲荘でのご面会―『メシヤが生まれた』」 confirmado contra o scan p.151."

# ---------- 3.2 : título corrigido contra scan p.202 ----------
s = nodes["3.2"]
assert s["title_ja"] == "滟刘力の発揮", s["title_ja"]
s["title_ja"] = "絶対力の発揮"
s["ja_note"] = "OCR corrompido (「滟刘力の発揮」); corrigido contra o scan, livro p.202 (Scans/174-223.pdf): 「絶対力の発揮」."
if "3.2" in data.get("ja_ocr_suspect_paths", []):
    data["ja_ocr_suspect_paths"].remove("3.2")

io.open(F, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=2))
print("OK: 2.5.5 +", len(rec_2_5_5), "| 2.7.1 +", len(rec_2_7_1), "| 2.7.2 +", len(rec_2_7_2), "| titulo 3.2 corrigido")
