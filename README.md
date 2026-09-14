# Notebooks — InsperAI

O par prático das trilhas do site [trilhas-insperai](https://trilhas-insperai.vercel.app).
Cada notebook é a **aplicação em código do que foi dado naquela aula**: mesmo
exemplo, mesmo dado, mesma história — agora rodando.

A página da aula explica e deixa você mexer nos gráficos. O notebook mostra as
mesmas contas em Python, com dado de verdade.

## Trilha de Trainees

| Aula | Notebook | Abrir |
|---|---|---|
| 0 · O seu primeiro notebook | [`aula-00-primeiro-notebook.ipynb`](trainees/aula-00-primeiro-notebook.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AlexChequer/notebooks-insperai/blob/main/trainees/aula-00-primeiro-notebook.ipynb) |
| 1 · Intro a ML + Regressão Linear | [`aula-01-regressao-linear.ipynb`](trainees/aula-01-regressao-linear.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AlexChequer/notebooks-insperai/blob/main/trainees/aula-01-regressao-linear.ipynb) |
| 2 · Escalando o Modelo | [`aula-02-escalando-o-modelo.ipynb`](trainees/aula-02-escalando-o-modelo.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AlexChequer/notebooks-insperai/blob/main/trainees/aula-02-escalando-o-modelo.ipynb) |

As demais entram conforme forem ficando prontas.

## Trilha de ML/DL Avançado

| Aula | Notebook | Abrir |
|---|---|---|
| 1 · EDA Avançada | [`aula-01-eda-avancada.ipynb`](ml-avancado/aula-01-eda-avancada.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AlexChequer/notebooks-insperai/blob/main/ml-avancado/aula-01-eda-avancada.ipynb) |

As demais entram conforme forem ficando prontas.

## Como usar

**No Colab (recomendado, e não precisa instalar nada).** Clique no badge da aula.
O notebook abre no navegador e o dado é baixado deste repositório na primeira
célula. Funciona no laptop, no tablet e até no celular.

Se você nunca abriu um notebook, **comece pelo da Aula 0**: ele ensina a mecânica
(célula, kernel, ordem de execução, como ler um erro), não depende de dado nenhum e
serve de teste do ambiente para quem fez o setup local.

**Na sua máquina**, com [uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/AlexChequer/notebooks-insperai.git
cd notebooks-insperai
uv sync
uv run jupyter lab
```

O caminho local é o mesmo que a Aula 0 do site ensina a montar.

> Os notebooks estão **com as saídas salvas**: dá para ler tudo aqui pelo GitHub,
> com gráficos e números, sem rodar nada. Para refazer do zero, use
> *Kernel → Restart & Run All*.

## O dado

`dados/imoveis.csv` — **1.460 imóveis reais** vendidos em Ames, Iowa, entre 2006 e
2010. É o dataset *Ames Housing*, que vem do
[OpenML](https://www.openml.org/d/42165) e é o mesmo usado em meio mundo de curso
de ML.

O arquivo aqui é uma versão enxuta: só as colunas que as aulas usam, com os nomes
em português e as unidades convertidas para o que a gente usa no Brasil.

| coluna | o que é | origem |
|---|---|---|
| `metragem_m2` | área construída, em m² | `GrLivArea` (pés²) × 0,0929 |
| `terreno_m2` | área do terreno, em m² | `LotArea` (pés²) × 0,0929 |
| `quartos` | quartos acima do solo | `BedroomAbvGr` |
| `banheiros` | banheiros completos | `FullBath` |
| `vagas_garagem` | vagas na garagem | `GarageCars` |
| `qualidade` | nota geral de acabamento, de 1 a 10 | `OverallQual` |
| `idade_anos` | idade do imóvel na venda | `YrSold − YearBuilt` |
| `preco_mil` | preço de venda, em **milhares de dólares** | `SalePrice` ÷ 1000 |

Ele é lido direto da pasta quando você roda local, e da URL bruta do GitHub quando
você roda no Colab — a primeira célula cuida disso sozinha. (A Aula 0 é a exceção:
ela fabrica o próprio dado com NumPy, para rodar em qualquer lugar sem depender de
arquivo nem de rede.)

`dados/titanic.csv` — os 891 passageiros do Titanic, como o Seaborn distribui. Usado
nas Aulas 1 e 2 de ML/DL Avançado.

`dados/diamonds.csv.gz` — os 53.940 diamantes do dataset clássico `diamonds`, também
do Seaborn, comprimido em gzip (de ~2,6 MB para ~550 KB — `pd.read_csv` lê gzip sem
precisar descompactar antes). Usado na Aula 1 de ML/DL Avançado.

Os dois seguem o mesmo padrão do `imoveis.csv`: lidos da pasta local quando existe, e
da URL bruta do GitHub como último recurso (Colab, ou clone parcial).

## Estrutura

```
notebooks-insperai/
├── dados/
│   ├── imoveis.csv           # Ames Housing — trilha de trainees
│   ├── titanic.csv           # Titanic (Seaborn) — ml-avancado, Aulas 1 e 2
│   └── diamonds.csv.gz       # diamonds (Seaborn), gzip — ml-avancado, Aula 1
├── trainees/                 # um notebook por aula da trilha de trainees
│   ├── aula-00-primeiro-notebook.ipynb
│   ├── aula-01-regressao-linear.ipynb
│   └── aula-02-escalando-o-modelo.ipynb
├── ml-avancado/               # um notebook por aula da trilha de ML/DL Avançado
│   └── aula-01-eda-avancada.ipynb
├── pyproject.toml            # as dependências, para o uv
├── CLAUDE.md                 # como trabalhar neste repositório
└── README.md
```

## Contribuindo

Este repositório é material didático: a ideia é **clonar e rodar**, não commitar.
Achou um erro, um número que não bate ou uma explicação confusa? Abra uma
[issue](https://github.com/AlexChequer/notebooks-insperai/issues) — é a forma mais
útil de ajudar.
