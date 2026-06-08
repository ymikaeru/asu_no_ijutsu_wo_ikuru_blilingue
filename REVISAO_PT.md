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

- [ ] **2.3.9** — *9. O Ataque Aéreo de Maebashi* (p.64)
  - PT diz: *"(\"Até se Tornar Religião\", 30 de dezembro de **1952**)"*
  - Livro impresso (scan p.64, dígito conferido em zoom): **昭和24年 = 1949**.
  - **Ação:** trocar `1952` → `1949` no PT. (O JA já foi corrigido para 昭和24年.)

- [ ] **3.4.4** — *4. Geração e Eliminação de Nuvens Espirituais* (p.250)
  - PT diz: *"(\"Vida e Morte\", 23 de **janeiro** de 1943)"*
  - Livro impresso (scan p.250): **昭和18年10月23日** = 23 de **outubro** de 1943.
  - **Ação:** trocar `janeiro` → `outubro` no PT (ano 1943 e dia 23 estão certos).
    (O JA já foi corrigido para 昭和18年10月23日.)

---

## B. Candidatos a verificar contra o scan

Datas específicas do PT que **não** têm a era correspondente no JA da seção.
Podem ser erro do PT, ou o JA expressa a data de outra forma (翌年, 西暦, só 年).
Conferir no scan antes de mexer.

- [ ] **2.3.3** — *3. Oferenda de Arroz* (p.~41) — **suspeita alta**
  - PT: *"No dia 1º de janeiro de **1952**, Ele comentou…"*
  - Eras no JA da seção: 昭和19, 21, 25, 26 (nenhuma = 昭和27/1952).
  - Obs.: a seção vizinha 2.3.4 fala de 「昭和20年の正月、まだ戦争中」 (Ano-Novo de 1945,
    em plena guerra). Se for a mesma oferenda de arroz, "1952" provavelmente está errado.

- [ ] **2.5.8** — *8. Fundação da Igreja Koyo* (p.~129) — **provável falso positivo**
  - PT: *"No ano seguinte, em agosto de **1948**…"*
  - JA tem 昭和22年 (1947). "No ano seguinte" de 1947 = 1948 → o PT pode estar certo
    (o JA deve dizer 「翌年」). Confirmar só por segurança.

- [ ] **2.5.9** — *9. A Purificação da Sarna* (p.~131)
  - PT: *"…entrou em purificação de sarna em dezembro de **1946**…"*
  - Eras no JA: 昭和20, 22, 24 (nenhuma = 昭和21/1946). Conferir o ano real do episódio.

- [ ] **2.6.1** — *1. A Fundação da Igreja* (p.~143)
  - PT: *"Em 30 de outubro de **1948**, foi fundada a Igreja Miroku…"*
  - Eras no JA: 昭和21, 22, 24, 25. Data histórica de fundação — conferir contra o livro.

- [ ] **3.1.2** — *2. Jeová Direto e o Intermediário* (p.~194)
  - PT: *"Creio que foi em meados de **1946**. Fui levado pela polícia…"*
  - Eras no JA: 昭和19 (1944), 昭和3. Episódio da prisão — conferir o ano.

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
