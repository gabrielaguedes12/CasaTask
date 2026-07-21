# CasaTask 🏠

Sistema de organização de tarefas domésticas para famílias, com lógica de rodízio automático e ranking de participação. Primeiro projeto de uma trilha de três aplicações voltadas para consolidar fundamentos de Python, SQL e arquitetura de APIs — evoluindo em complexidade a cada etapa.

> **Trilha de projetos:** CasaTask (básico) → App de Planejamento de Casamento (intermediário) → Sistema de Gestão para Marmitaria (avançado)

## O problema

Dividir tarefas domésticas de forma justa entre os moradores de uma casa é algo que normalmente é feito de cabeça, sem histórico e sem transparência — o que gera a sensação recorrente de "eu sempre faço mais". O CasaTask resolve isso guardando um histórico real de quem fez o quê e quando, permitindo visualizar a distribuição de esforço ao longo do tempo.

## Objetivo do projeto

Construir uma API funcional do zero, aplicando:
- Modelagem de banco de dados relacional
- Boas práticas de organização de código (separação em camadas)
- Consultas SQL com agregação (JOIN, GROUP BY, COUNT)
- Fundamentos de Python orientado a objetos (classes, herança)
- Conceitos de API REST (verbos HTTP, validação de dados)

## Arquitetura

O projeto segue uma **arquitetura em camadas**, onde cada arquivo tem uma responsabilidade única e só se comunica com a camada adjacente:

```
Router (recebe a requisição HTTP)
   ↓
Schema (valida o formato dos dados de entrada/saída)
   ↓
Model (representa a estrutura da tabela no banco)
   ↓
Database (gerencia a conexão com o SQLite)
```

Essa separação evita que regras de negócio, validação e acesso ao banco fiquem misturados no mesmo lugar — o que facilita manutenção e, futuramente, a integração com um frontend em React sem precisar alterar a lógica da API.

```
casatask/
├── app/
│   ├── main.py            # ponto de entrada, registra os routers
│   ├── database.py        # conexão com o banco SQLite
│   ├── models.py          # tabelas do banco (SQLAlchemy)
│   ├── schemas.py         # validação de entrada/saída (Pydantic)
│   └── routers/
│       ├── pessoas.py     # endpoints de pessoas
│       └── tarefas.py     # endpoints de tarefas, atribuições e ranking
├── database/
│   └── casatask.db        # arquivo do banco SQLite
└── requirements.txt
```

## Modelagem do banco de dados

Três tabelas, com relacionamento 1:N entre elas:

**pessoas**
| campo | tipo | descrição |
|---|---|---|
| id | INTEGER (PK) | identificador único |
| nome | TEXT | nome da pessoa |

**tarefas**
| campo | tipo | descrição |
|---|---|---|
| id | INTEGER (PK) | identificador único |
| nome | TEXT | ex: "lavar louça" |
| frequencia | TEXT | ex: "diaria", "semanal" |

**atribuicoes** (tabela de histórico — registra quem fez o quê e quando)
| campo | tipo | descrição |
|---|---|---|
| id | INTEGER (PK) | identificador único |
| tarefa_id | INTEGER (FK) | referência a `tarefas.id` |
| pessoa_id | INTEGER (FK) | referência a `pessoas.id` |
| data | DATE | data da atribuição |
| concluida | BOOLEAN | se a tarefa foi feita |

## Stack técnica

- **Python 3** — linguagem principal
- **FastAPI** — framework da API, com documentação automática integrada
- **SQLAlchemy** — ORM para modelar e consultar o banco
- **Pydantic** — validação de dados de entrada e saída
- **SQLite** — banco de dados relacional (leve, sem necessidade de servidor)

## Endpoints principais

| Método | Rota | Descrição |
|---|---|---|
| POST | `/pessoas/` | Cadastra uma nova pessoa |
| GET | `/pessoas/` | Lista todas as pessoas |
| POST | `/tarefas/` | Cadastra uma nova tarefa |
| GET | `/tarefas/` | Lista todas as tarefas |
| POST | `/tarefas/atribuicoes` | Atribui uma tarefa a uma pessoa em uma data |
| PUT | `/tarefas/atribuicoes/{id}/concluir` | Marca uma atribuição como concluída |
| GET | `/tarefas/ranking` | Retorna o ranking de tarefas concluídas por pessoa |

O endpoint de ranking é o ponto central do projeto do ponto de vista de SQL: ele equivale à seguinte consulta:

```sql
SELECT pessoas.nome, COUNT(atribuicoes.id) AS total_concluidas
FROM atribuicoes
JOIN pessoas ON atribuicoes.pessoa_id = pessoas.id
WHERE atribuicoes.concluida = true
GROUP BY pessoas.nome
ORDER BY total_concluidas DESC;
```

## Como rodar o projeto

```bash
# Clonar o repositório
git clone <url-do-repo>
cd casatask

# Criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux

# Instalar dependências
pip install -r requirements.txt

# Rodar o servidor
uvicorn app.main:app --reload
```

A API estará disponível em ``, e a documentação interativa em ``.

## O que aprendi construindo esse projeto

- Diferença entre importação absoluta e relativa em pacotes Python, e como isso afeta a execução de um projeto estruturado em múltiplos módulos
- Como o SQLAlchemy traduz classes Python em tabelas e consultas SQL, através do padrão ORM (Object-Relational Mapping)
- Separação de responsabilidades entre validação de dados (Pydantic) e persistência de dados (SQLAlchemy) — dois problemas que parecem iguais, mas não são
- Como escrever agregações SQL (JOIN + GROUP BY) tanto via ORM quanto em SQL puro
- Fundamentos de API REST: verbos HTTP, status codes, e o ciclo completo de uma requisição

## Próximos passos da trilha

- **Projeto 2 (intermediário):** App de planejamento de casamento — introduz modelagem mais complexa (orçamento, fornecedores, convidados), relatórios financeiros e views SQL
- **Projeto 3 (avançado):** Sistema de gestão para uma marmitaria real — introduz controle de estoque, precificação, previsão de demanda e um caso de uso de negócio real em produção
