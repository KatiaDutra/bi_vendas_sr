# bi_vendas_sr

Projeto de Business Intelligence e análise de vendas desenvolvido com Power BI, Power Query e Python.

# Painel de Análise de Vendas, Margem de Lucro e Positivação (2020 – 2026)

## Visão Geral do Projeto

Este projeto consiste no desenvolvimento de uma solução completa de **Business Intelligence (BI)**, construída do zero para uma empresa do setor de comércio. O objetivo principal é transformar dados brutos, extraídos de relatórios operacionais do sistema ERP, em um painel interativo no Power BI que apoie a tomada de decisão estratégica.

O histórico de dados abrange as operações realizadas de **janeiro de 2020 a julho de 2026**.

O projeto é desenvolvido como parte do Trabalho de Conclusão de Curso (TCC) do curso de Tecnologia em Sistemas para Internet (TSI).

---

## Status do Projeto

| Etapa | Situação |
|---|---|
| Extração dos relatórios do ERP | ✅ Concluída |
| Anonimização dos dados (LGPD) com Python | ✅ Concluída |
| ETL no Power Query (Lucratividade e Positivação) | ✅ Concluída |
| Modelagem de dados (Star Schema) | ✅ Concluída |
| Medidas em DAX | ✅ Concluída |
| Construção do dashboard visual | 🔄 Em andamento |
| Documentação final | 🔄 Em andamento |

---

## Tecnologias e Ferramentas Utilizadas

- **Python**: automação da anonimização em lote dos dados sensíveis (LGPD) e pré-processamento.
- **Power Query (M)**: extração, limpeza, transformação e carga (ETL) de 79 relatórios consolidados por pasta.
- **Power BI**: modelagem de dados (Star Schema), criação de medidas em DAX e construção do dashboard interativo.
- **Git & GitHub**: versionamento de código, controle de alterações e documentação do projeto.

---

## Fontes de Dados

Os dados utilizados vêm de dois grupos de relatórios do ERP:

- **Lucratividade**: vendas por nota fiscal e produto, com faturamento, custo e margem de lucro.
- **Positivação**: clientes atendidos por vendedor e canal de venda, permitindo medir a cobertura da carteira de clientes.

---

## Tratamento de Dados e LGPD

Para garantir a segurança das informações comerciais e o cumprimento da Lei Geral de Proteção de Dados (LGPD):

1. Os relatórios brutos, no formato `.xls`, foram armazenados em um diretório local e protegidos pelo `.gitignore`.
2. Foi desenvolvido um script Python (`scripts/anonymize.py`) que percorre todos os arquivos brutos, substitui a razão social dos clientes por códigos fictícios padronizados (`CLIENTE ANONIMO XXXX`), mantendo a consistência do ID, e anonimiza o nome da empresa.
3. Os dados anonimizados resultantes foram salvos no diretório `data/processed/` para consumo no Power BI.

---

## Modelagem de Dados

O modelo foi construído no formato **Star Schema (esquema estrela)**, com as tabelas fato **fVendas** (Lucratividade) e **fPositivacao** ligadas às tabelas dimensão **dCalendario**, **dProduto** e **dVendedor**. Essa estrutura facilita os filtros cruzados no dashboard e melhora o desempenho das medidas em DAX.

---

## Regras de Negócio

Durante a análise, algumas regras foram definidas junto à realidade da empresa:

- **Canais de venda**: as vendas são classificadas em três canais: **Televendas** (equipe de vendedores internos), **Loja** (loja física) e **Site** (vendas online).
- **Cliente em mais de um canal**: a política da empresa permite que um mesmo cliente compre tanto pelos vendedores de televendas quanto na loja física. Por isso, um cliente pode aparecer positivado em mais de um vendedor ou canal no mesmo período.
- **Cliente "A VISTA"**: o cliente genérico de vendas à vista (código 22) é contado como cliente na positivação.
- **Ticket médio**: cada nota fiscal (combinação de número e série) é contada como uma venda no cálculo do ticket médio.

---

## Estrutura do Repositório

```
bi_vendas_sr/
│
├── data/
│   ├── raw/           # Relatórios originais do ERP (protegido no .gitignore)
│   └── processed/     # Dados anonimizados consumidos pelo Power BI
│
├── scripts/
│   └── anonymize.py   # Script Python de anonimização em lote (79 arquivos)
│
├── pbix/
│   └── dashboard_vendas.pbix  # Arquivo principal do Power BI
│
└── README.md          # Documentação do projeto
```

---

## Indicadores e Métricas (KPIs)

**Vendas e lucratividade**
- Faturamento total (R$)
- Volume de unidades vendidas
- Ticket médio por venda (por nota fiscal)
- Lucratividade e margem de lucro por produto e categoria
- Curva ABC de produtos

**Positivação e canais**
- Quantidade de clientes positivados
- Positivação por vendedor e por canal (Televendas, Loja e Site)
- Participação de cada canal no faturamento

**Análise temporal**
- Evolução temporal e comparativos (YoY / MoM)

---

## Autora

Desenvolvido por **Kátia Dutra**.

- [LinkedIn](http://www.linkedin.com/in/katia-dutra-ss)
- [GitHub](https://github.com/KatiaDutra)

