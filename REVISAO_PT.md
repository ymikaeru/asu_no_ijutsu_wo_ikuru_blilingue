# Revisão da tradução PT — erros e candidatos

Arquivo de trabalho para conferir e corrigir o texto **português** (`content`) do
`ashita-no-ijitsu.bilingual.json`. Gerado cruzando datas/números entre o JA
(fonte, já corrigido contra o scan no Cap.1) e o PT.

**Regra de ouro:** o JA do livro impresso (scan em `Scans/*.pdf`) é a fonte da
verdade. Onde o PT diverge do livro, o PT é que se corrige.

Como verificar uma data: renderizar a página do scan (ver offsets na memória do
projeto ou em `_fix_gaps.py`) e ler o trecho. As páginas estão estimadas abaixo.

Status: `[ ]` a fazer · `[x]` resolvido · `[~]` descartado (falso positivo)

---

## A. Erros confirmados (corrigir o PT)

- [x] **2.3.9** — *9. O Ataque Aéreo de Maebashi* (p.64) — **CORRIGIDO 2026-06-08**
  - PT dizia: *"(\"Até se Tornar Religião\", 30 de dezembro de **1952**)"*
  - Livro impresso (scan p.64, dígito conferido em zoom): **昭和24年 = 1949**.
  - Aplicado: `1952` → `1949` no PT. (JA = 昭和24年.)

- [x] **3.4.4** — *4. Geração e Eliminação de Nuvens Espirituais* (p.250) — **CORRIGIDO 2026-06-08**
  - PT dizia: *"(\"Vida e Morte\", 23 de **janeiro** de 1943)"*
  - Livro impresso (scan p.250): **昭和18年10月23日** = 23 de **outubro** de 1943.
  - Aplicado: `janeiro` → `outubro` no PT. (JA = 昭和18年10月23日.)

- [x] **3.1.2** — *2. Jeová Direto e o Intermediário* (p.199) — **CORRIGIDO 2026-06-08**
  - PT dizia: *"Creio que foi em meados de **1946**. Fui levado pela polícia…"*
  - Livro impresso (scan p.199, confirmado em zoom): **昭和20年代の半ば頃**.
    昭和20年 = **1945** (Showa começa em 1926); 昭和20年代 = 1945–1954; o meio ≈ **~1950**.
    O OCR estava corrompido (昭利21年代の半は頃).
  - Aplicado: *"em meados de 1946"* → *"por volta de meados da década de 20 da Era Showa
    (aproximadamente 1950)"*. O JA foi corrigido para 昭和20年代の半ば頃.

---

## B. Candidatos verificados contra o scan — RESOLVIDOS (2026-06-08)

- [~] **2.3.3** — *Oferenda de Arroz* — **falso positivo (PT correto)**
  - JA: 「翌27年元旦」 = 昭和27年 = 1º de janeiro de **1952**. PT certo. (O detector não lê 「翌N年」.)
- [~] **2.5.8** — *Fundação da Igreja Koyo* — **falso positivo (PT correto)**
  - JA: 「翌23年8月」 = 昭和23年 = agosto de **1948**. PT certo.
- [~] **2.5.9** — *A Purificação da Sarna* — **PT correto; JA tinha erro de OCR (corrigido)**
  - JA dizia 「昭和2l年」 (L minúsculo) = 昭和21年 = **1946**. PT certo. Corrigido o JA
    (昭和21年; 弥癬/癬 → 疥癬, confirmado no scan p.131).
- [~] **2.6.1** — *A Fundação da Igreja* — **falso positivo (PT correto)**
  - JA: 「翌23年10月30日」 = 昭和23年 = **30 de outubro de 1948**. PT certo.
- [→] **3.1.2** — era **erro real de PT**; movido para a Seção A acima.

---

## C. Descartados (falso positivo — não mexer)

Conflitos que o detector apontou mas que são coerentes:

- [~] **2.1.1** — PT 1922 e 1926: o JA escreve 「同11年」(大正11=1922) e 「同15年」(大正15=1926);
  o conversor não lê 「同」. JA correto.
- [~] **2.5.12** — PT "desde 1948": o JA tem 「昭和23年」(=1948), confirmado no scan p.138.
- [~] **2.4.1**, **4 (Apêndice)**, **4.8** — PT usa intervalos ("1946 e 1947"); o JA tem
  昭和21/22年, coerente.
- [~] **2.8.6**, **2.8.7**, **3.5.6**, **3.6.4** — PT usa "década de 19X0"; o JA tem uma
  era dentro dessa década (ex.: 昭和30年=1955 dentro de "década de 1950"). Coerente.
- [~] **2.8.9** — PT "1976 a 1979": JA 「昭和51年から54年」 = exatamente 1976–1979. Coerente.

---

## D. Notas

- Esta lista cobre **datas/anos**. Erros de tradução *semânticos* (sentido, termos
  doutrinários) não são detectáveis automaticamente — exigem leitura comparada
  JA↔PT, a ser feita na revisão por capítulo.
- Reexecutar o detector após corrigir: `python _pt_conflicts.py`.
- O JA embarcado é OCR; onde o JA também estiver suspeito, conferir os dois contra o scan.
