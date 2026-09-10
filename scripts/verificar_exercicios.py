"""Portão dos notebooks de exercício.

Um notebook de exercício não roda de ponta a ponta como sai: as funções levantam
`NotImplementedError` até o trainee implementar — que é justamente o que impede o
"Run all e pronto". Isso conflita com o invariante 2 do CLAUDE.md, então o portão
muda de forma em vez de deixar de existir.

O que este script faz: para cada célula com `### SEU CÓDIGO AQUI ###`, pega o
primeiro bloco ```python do próximo `<details>` (o gabarito), substitui, e roda o
notebook inteiro. Depois confere que nenhuma célula estourou e que **toda** saída
de `verificar()` diz ✓.

Isso garante três coisas de uma vez: o gabarito está certo, os testes passam com
ele, e o enunciado é implementável do jeito que está escrito. O notebook
publicado continua sendo o com as lacunas — a versão preenchida é temporária e
morre aqui dentro.

    uv run python scripts/verificar_exercicios.py trainees/aula-03-classificacao.ipynb
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

MARCA = "### SEU CÓDIGO AQUI ###"
BLOCO_PY = re.compile(r"```python\n(.*?)```", re.DOTALL)


def primeiro_gabarito(celulas, inicio: int) -> tuple[str, int]:
    """O primeiro bloco ```python do próximo <details> depois de `inicio`."""
    for i in range(inicio + 1, len(celulas)):
        c = celulas[i]
        if c.cell_type != "markdown" or "<details>" not in c.source:
            continue
        m = BLOCO_PY.search(c.source)
        if not m:
            raise SystemExit(f"<details> da célula {i} não tem bloco ```python")
        return m.group(1).rstrip("\n"), i
    raise SystemExit(f"nenhum <details> depois da célula {inicio}")


def preencher(nb) -> int:
    """Troca cada lacuna pelo gabarito. Devolve quantas trocou."""
    trocas = 0
    for i, c in enumerate(nb.cells):
        if c.cell_type != "code" or MARCA not in c.source:
            continue
        gabarito, _ = primeiro_gabarito(nb.cells, i)

        linhas, saida, trocou = c.source.splitlines(), [], False
        for linha in linhas:
            if MARCA in linha:
                saida.append(gabarito)
                trocou = True
            elif trocou and "raise NotImplementedError" in linha:
                continue  # a linha que o trainee apagaria
            else:
                saida.append(linha)
        c.source = "\n".join(saida)
        trocas += 1
    return trocas


def conferir_saidas(nb) -> list[str]:
    """Todo `verificar()` tem que ter impresso ✓ e nenhum ✗."""
    problemas = []
    vistos = 0
    for i, c in enumerate(nb.cells):
        if c.cell_type != "code":
            continue
        texto = "".join(
            "".join(o.get("text", "")) for o in c.get("outputs", []) if o.output_type == "stream"
        )
        if "✗" in texto:
            falhas = [ln for ln in texto.splitlines() if "✗" in ln]
            problemas.append(f"célula {i}:\n    " + "\n    ".join(falhas))
        if "✓" in texto and ": passou nos" in texto:
            vistos += 1
    if not vistos:
        problemas.append("nenhuma bateria de verificar() rodou — o notebook mudou de forma?")
    else:
        print(f"  {vistos} baterias de teste, todas verdes")
    return problemas


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("notebook", type=Path)
    args = ap.parse_args()

    nb = nbformat.read(args.notebook, as_version=4)
    trocas = preencher(nb)
    if not trocas:
        print(f"{args.notebook}: nenhuma lacuna encontrada — não é notebook de exercício.")
        return 0
    print(f"{args.notebook.name}: {trocas} lacunas preenchidas com o gabarito, executando...")

    with tempfile.TemporaryDirectory() as tmp:
        preenchido = Path(tmp) / args.notebook.name
        nbformat.write(nb, preenchido)
        cliente = NotebookClient(nb, timeout=600, kernel_name="python3",
                                 resources={"metadata": {"path": str(args.notebook.parent.parent)}})
        try:
            cliente.execute()
        except CellExecutionError as erro:
            print(f"\n✗ uma célula estourou:\n{erro}", file=sys.stderr)
            return 1

    problemas = conferir_saidas(nb)
    if problemas:
        print("\n✗ testes falharam com o gabarito:\n" + "\n".join(problemas), file=sys.stderr)
        return 1

    print(f"\n✓ {args.notebook.name}: gabarito completo, roda limpo e passa em todos os testes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
