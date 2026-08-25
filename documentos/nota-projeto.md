---
tipo: projeto
categoria: acadêmico
disciplina: Engenharia de Software II (ES2)
universidade: Unesp Bauru
semestre: 2026-1
status: ativo
funcao-fernando: integrante
inicio: 2026-01
ultima-atualizacao: 2026-07-04
---

# RANK-IA

## Descrição

Aplicação web corporativa que utiliza Inteligência Artificial para montar **equipes otimizadas** com base em habilidades, competências e gaps dos colaboradores.

**Usuários**:
- **Gestor/RH**: acesso total (cadastro, config. da IA, validação, relatórios).
- **Colaborador**: consulta de competências, treinamentos e equipes.

## Integrantes

| Membro | RA | Papel |
|---|---|---|
| Fernando Hiroshi Murusaki | 241025851 | Integrante |
| Igor dos Reis Gomes | 241025265 | Integrante |
| Matheus Santos Magro | 231025335 | Integrante |
| Murilo Tomaz Gonzaga | 241024684 | Integrante |

## Arquitetura e metodologia

**Stack**: Node.js/TypeScript (Backend API)

**Arquitetura**: C4 (3 níveis)
- Nível 1: Diagrama de Contexto
- Nível 2: Diagrama de Containers
- Nível 3: Diagrama de Componentes

**Módulo central**: `src/equipes/`
- Entities: `Equipe.ts`, `Colaborador.ts`, `Competencia.ts`
- Services: `GerenciadorDeEquipes.ts`
- Repositories: `EquipeRepository.ts`
- Interfaces: `IEquipeRepository`, `IIAGeradoraService`, `INotificadorService`

**Padrões aplicados**:
- Dependency Inversion (abstrações em interfaces)
- Modularização por coesão (mudanças que afetam equipes ficam no mesmo módulo)

**Metodologia**: Scrumban (Scrum + Kanban, sprints de 2 semanas)

## Funcionalidades principais

- Geração automática de equipes com Coeficiente de Aproveitamento.
- Ajustes manuais que retroalimentam o modelo de IA.
- Sugestão de treinamentos baseados em gaps identificados.
- Relatórios de desempenho individual e coletivo.

## Documentação

Ver PDF: `grupo-8-rank-ia-es-ii.pdf` (projeto final de ES2).
