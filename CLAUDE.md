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
   diff feio, e é um preço aceito de propósito.
3. **A primeira célula resolve o caminho do dado sozinha.** Ela tenta
   `dados/imoveis.csv`, depois `../dados/imoveis.csv`, e por último a URL bruta do
   GitHub. São os três casos reais: Jupyter aberto na raiz, Jupyter aberto na pasta
   do notebook, e Colab. Não simplifique isso para um caminho só — já quebrou.
4. **Badge do Colab no topo de todo notebook**, apontando para o caminho dele na
   `main`. É o caminho principal de acesso dos trainees.
5. **O dado enxuto mora em `dados/`.** Nada de `fetch_openml` dentro do notebook: é
   lento, depende de rede e já falhou em sala. A conversão do dataset original está
   documentada no README.

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
