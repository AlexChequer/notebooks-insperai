# CLAUDE.md — como trabalhar neste repositório

Os notebooks práticos das trilhas da InsperAI. **Um notebook por aula**, sendo o
par em código da página correspondente em
[trilhas-insperai](https://github.com/AlexChequer/trilhas-insperai).

A exceção são os **notebooks de revisão** (`aula-revisao-*.ipynb`), que fecham um
conjunto de aulas em vez de uma: eles não introduzem nada, revisitam o que já foi
dado. Valem todos os invariantes abaixo, menos o de continuidade de dataset — a
revisão volta ao exemplo pequeno da lousa, que é onde o aluno viu a conta na mão.

## A regra de ouro

**Um trainee que acabou de ler a página da aula tem que reconhecer o notebook
imediatamente.** Mesmo problema, mesmo dataset, mesma história — agora em código.

Consequências práticas disso:

- **O notebook não é um assunto novo.** Se a página explicou resíduos, custo e
  gradient descent, o notebook faz exatamente isso rodar. Nada de exercício avulso,
  nada de desafio paralelo, nada de conceito que a aula não deu.
- **Continuidade de dataset.** A Aula 2 continua no dado da Aula 1. O trainee gasta
  energia no conceito novo, não reaprendendo o contexto. Trocar de dataset só
  quando o conceito exigir (imagem, texto).
- **Perseguir o efeito, não a API.** O ponto da A2 não é "como se chama a função do
  sklearn", é ver o modelo melhorar quando o grau sobe. A biblioteca é meio.
- **Mostrar onde quebra.** Grau alto demais decora o ruído; escala errada trava o
  treino. O contraste é o que fixa o conceito.

## Antes de dizer que terminou

Todo notebook tem que **rodar de ponta a ponta, sem erro, do kernel limpo**:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace trainees/aula-XX-*.ipynb
```

E depois conferir as **saídas**, não só a ausência de exceção. Número que sai
diferente do que o texto ao lado promete é pior que erro: erro você vê, número
errado o trainee acredita.

## Os invariantes

1. **Tudo em pt-BR** — texto, nomes de variáveis, comentários, títulos de gráfico,
   rótulos de eixo, commits. Sem exceção, igual ao repositório do site.
2. **As saídas ficam commitadas.** O notebook precisa ser legível no GitHub sem
   rodar nada — é assim que ele serve de consulta depois da aula. Isso deixa o
   diff feio, e é um preço aceito de propósito. **Exceção: os notebooks de
   exercício** (ver a seção abaixo) vão sem saída nenhuma — metade das células
   depende de código que o trainee ainda não escreveu, e commitar uma sequência
   de `NotImplementedError` seria pior que não ter saída.
3. **A primeira célula resolve o caminho do dado sozinha.** Ela tenta
   `dados/imoveis.csv`, depois `../dados/imoveis.csv`, e por último a URL bruta do
   GitHub. São os três casos reais: Jupyter aberto na raiz, Jupyter aberto na pasta
   do notebook, e Colab. Não simplifique isso para um caminho só — já quebrou.
4. **Badge do Colab no topo de todo notebook**, apontando para o caminho dele na
   `main`. É o caminho principal de acesso dos trainees.
5. **O dado enxuto mora em `dados/`.** Nada de `fetch_openml` dentro do notebook: é
   lento, depende de rede e já falhou em sala. A conversão do dataset original está
   documentada no README.

## Notebooks de exercício

A partir da Aula 3 existe um segundo tipo: em vez de o código vir pronto, **o
trainee implementa**. A decisão e o porquê estão no [Log de Decisões] do repo do
site; aqui fica a mecânica.

**A forma.** Cada exercício são três células, nesta ordem:

1. **Enunciado** (markdown): a matemática *antes* da tarefa. Deduza a fórmula,
   não a entregue pronta — a sigmoid sai do log-odds, a cross-entropy sai da
   verossimilhança. É o que separa "implementar" de "transcrever".
2. **A função** (código): assinatura, docstring com formatos de entrada e saída,
   `### SEU CÓDIGO AQUI ###  (≈ N linhas)` e um `raise NotImplementedError`.
   O `raise` é o que impede o `Run all` — não tire.
3. **O teste** (código): uma chamada a `verificar()`, que imprime ✓/✗ por caso e
   mostra o número que veio contra o esperado. Todas as falhas de uma vez, nunca
   `assert` que para na primeira.

Depois do teste, um `<details><summary>Resposta do Exercício N</summary>` com a
implementação **e o porquê** — o erro comum, a decisão escondida, a armadilha
numérica. Quem acertou também lê.

**O `<details>` é fonte de verdade, não só texto.** O portão extrai dele o
primeiro bloco ```` ```python ````, injeta na lacuna e roda o notebook. Mude o
formato e o portão para de funcionar.

**Escrever bom teste é o trabalho de verdade.** Um teste que só confere um valor
não ensina nada. Os que valem: comparar gradiente analítico com **diferenças
finitas**; conferir **formato** de saída antes de valor; testar o caso
**degenerado** (denominador zero, sigmoid saturada); e ancorar num número que o
enunciado prometeu.

**O portão deles é outro**, porque estes não rodam de ponta a ponta como saem:

```bash
uv run python scripts/verificar_exercicios.py trainees/aula-03-classificacao.ipynb
```

Ele preenche as lacunas com os gabaritos, executa tudo e falha se alguma célula
estourar **ou** se algum `verificar()` imprimir um ✗. Isso prova três coisas de
uma vez: o gabarito está certo, os testes passam com ele, e o enunciado é
implementável como está escrito. Rode sempre — ele já pegou um valor esperado
que eu tinha chutado errado e um teste que afirmava algo falso sobre float64.

## A anatomia de um notebook

Na ordem, como nos dois que existem:

1. Título, badge do Colab, link para a página da aula, e o que vai ser feito.
2. Célula de setup: imports e carga do dado.
3. As seções, na **mesma ordem da página**, com markdown explicando antes de cada
   bloco de código.
4. 🔬 **Desafio**: 2 ou 3 exercícios no fim, cada um com a resposta dentro de um
   `<details><summary>Resposta</summary>` — que o GitHub e o Colab renderizam
   recolhido.
5. "O que ficou": os 4 ou 5 pontos da aula, e o link para o próximo notebook.

Blocos de "🔬 Experimente" no meio do texto, convidando a mexer num número e rodar
de novo, são bem-vindos — é o equivalente ao slider da página.

## Tom

O mesmo do site: escreva para alguém lendo **sem professor**. Explique o porquê,
não só o quê. Comentário no código registra a decisão, não repete o que a linha faz.

Evite tratar o leitor como quem já sabe: "repare que", "guarde essa imagem", "é o
tropeço mais comum" fazem mais efeito que "trivialmente, temos".

## O que nunca fazer

- **Não invente conteúdo pedagógico.** A fonte é a página da aula no site. Se a
  página não cobre, pergunte ao Alex — não preencha.
- **Não commite `.env`** nem credencial nenhuma. Ver `.gitignore`.
- **Não deixe número no texto sem conferir na saída.** Se o markdown diz "o RMSE é
  56", rode e confirme que é 56.
- **Não use `eval`** nem executar string arbitrária em notebook de aula.

## Commits

Formato convencional, em pt-BR, no imperativo — igual ao repositório do site:

```
feat: notebook da aula 3 (classificação)
fix: caminho do dado quebrava no Colab
docs: README explica de onde vem o dataset
```
