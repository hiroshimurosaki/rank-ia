# RANK-IA

Aplicação web corporativa que utiliza Inteligência Artificial para montar **equipes
otimizadas** com base em habilidades, competências e *gaps* dos colaboradores.

Projeto da disciplina **Engenharia de Software II (ES2)** — UNESP Bauru, Departamento de
Computação. O projeto nasceu no semestre 4 (Engenharia de Software I) e continua no
semestre 5 (ES2).

## Integrantes

| Membro | RA |
|---|---|
| Fernando Hiroshi Murusaki | 241025851 |
| Igor dos Reis Gomes | 241025265 |
| Matheus Santos Magro | 231025335 |
| Murilo Tomaz Gonzaga | 241024684 |

## Organização do repositório

```
rank-ia/
├── projeto/          # Documentação do projeto final em LaTeX (ES2 – 2026)
│   ├── documentacao-rank-ia.tex   # fonte principal (título e autores já preenchidos)
│   ├── documentacao-rank-ia.pdf   # PDF gerado a partir do .tex
│   ├── refs.bib
│   ├── images/
│   ├── template-original.tex     # template original do modelo, sem alterações
│   └── template-original.pdf     # PDF de referência do template
├── apresentacoes/    # Slides e pitch do RANK-IA (semestres 4 e 5)
└── documentos/       # PDFs entregues em ES1/ES2, diagrama C4 e nota do projeto
```

## Compilar a documentação

Requer uma distribuição LaTeX (ex.: [MiKTeX](https://miktex.org/) ou TeX Live)
com `pdflatex` e `bibtex` no `PATH`.

```bash
cd projeto
pdflatex -interaction=nonstopmode -aux-directory=build documentacao-rank-ia.tex
bibtex build/documentacao-rank-ia
pdflatex -interaction=nonstopmode -aux-directory=build documentacao-rank-ia.tex
pdflatex -interaction=nonstopmode -aux-directory=build documentacao-rank-ia.tex
```

A flag `-aux-directory=build` (MiKTeX) manda todo o lixo de compilação
(`.aux`, `.log`, `.bbl`, `.out`, `.toc`...) para `projeto/build/`, que já está
no `.gitignore`, em vez de espalhar esses arquivos junto do `.tex`. O PDF
final continua sendo gerado direto em `projeto/documentacao-rank-ia.pdf`. Com
TeX Live, o equivalente é `-output-directory=build`, mas nesse caso o PDF
também vai parar em `build/` e precisa ser copiado de volta.

> Antes da entrega final, trocar `\orientacoestrue` por `\orientacoesfalse` no início do
> `documentacao-rank-ia.tex` para ocultar as orientações do template.
