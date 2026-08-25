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
│   ├── projeto-final.tex   # fonte principal (título e autores já preenchidos)
│   ├── refs.bib
│   ├── images/
│   └── template-original.pdf   # PDF de referência do template
├── apresentacoes/    # Slides e pitch do RANK-IA (semestres 4 e 5)
├── documentos/       # PDF do projeto final, documento de ES2 e nota do projeto
└── material-aula/    # Material da disciplina ES2
    ├── slides/           # Slides teóricos das aulas
    ├── exemplos/         # Exemplos de código vistos em aula
    ├── exercicios/       # Exercícios (ex.: padrão Decorador)
    └── scraper/          # Script de extração de slides + saída
```

## Compilar a documentação

```bash
cd projeto
pdflatex projeto-final.tex
bibtex projeto-final
pdflatex projeto-final.tex
pdflatex projeto-final.tex
```

> Antes da entrega final, trocar `\orientacoestrue` por `\orientacoesfalse` no início do
> `projeto-final.tex` para ocultar as orientações do template.
