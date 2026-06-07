# -*- coding: utf-8 -*-
"""Detecta possiveis ERROS DE TRADUCAO no PT comparando datas/anos entre JA e PT.
Sinaliza quando o PT tem um ano que NAO esta no JA mas esta proximo (<=12) de um ano do JA
(sugere mesmo evento com digito trocado) — o padrao do erro 1952/1949 ja confirmado."""
import io, json, re

F = r"D:\Mioshie_Sites\Asu_No_Ijutsu_Wo_Ikiru_bilingue\ashita-no-ijitsu.bilingual.json"
data = json.load(io.open(F, encoding="utf-8"))

KD={"〇":0,"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9}
def k2i(t):
    total,cur=0,0
    for c in t:
        if c in KD: cur=cur*10+KD[c] if (cur and KD[c]) else (KD[c] if not cur else cur+KD[c])
        elif c=="十": total+=(cur or 1)*10; cur=0
        elif c=="百": total+=(cur or 1)*100; cur=0
        elif c=="千": total+=(cur or 1)*1000; cur=0
        else: return None
    return total+cur
ERA={"昭和":1925,"大正":1911,"平成":1988,"明治":1867}
def ja_years(t):
    ys=set()
    for era,base in ERA.items():
        for m in re.finditer(era+r"(\d{1,2}|[〇一二三四五六七八九十]{1,4})年",t):
            g=m.group(1); v=int(g) if g.isdigit() else k2i(g)
            if v: ys.add(base+v)
        if re.search(era+r"元年",t): ys.add(base+1)
    for m in re.finditer(r"(18|19|20)\d\d年",t): ys.add(int(m.group(0)[:-1]))
    return ys
def pt_years(t):
    return {int(m.group(0)) for m in re.finditer(r"\b(18|19|20)\d\d\b",t)}

rows=[]
def walk(secs,path):
    for i,s in enumerate(secs,1):
        p=".".join(path+[str(i)])
        ja=s.get("content_ja") or ""; pt=s.get("content") or ""
        yj, yp = ja_years(ja), pt_years(pt)
        for y in sorted(yp-yj):
            near=[d for d in yj if abs(d-y)<=12]
            if near:
                # contexto PT
                m=re.search(r".{0,40}\b"+str(y)+r"\b.{0,20}",pt)
                ctx=m.group(0).replace("\n"," ") if m else ""
                rows.append((p, s.get("title",""), y, sorted(near), ctx))
        walk(s.get("children",[]),path+[str(i)])
walk(data["sections"],[])
print(f"candidatos a conflito de data PT x JA: {len(rows)}\n")
for p,title,y,near,ctx in rows:
    print(f"{p} [{title[:30]}] PT={y} vs JA~{near}\n    …{ctx}…")
