# bi_vendas_sr
Projeto de Business Intelligence e análise de vendas desenvolvido com Power BI, Power Query e Python.

# Painel de Análise de Vendas e Margem de Lucro (2020 - 2026)

## Visão Geral do Projeto
Este projeto consiste no desenvolvimento de uma solução completa de **Business Intelligence (BI)** do zero para uma empresa do setor de comércio. O objetivo principal é transformar dados brutos extraídos de relatórios operacionais do sistema ERP em um painel interativo no Power BI para tomada de decisão estratégica.

O histórico de dados abrange as operações realizadas de **Janeiro de 2020 a Julho de 2026**.

---

## Tecnologias e Ferramentas Utilizadas
* **Python**: Automação do processo de anonimização em lote dos dados sensíveis (LGPD) e pré-processamento.
* **Power Query (M)**: Extração, Limpeza, Transformação e Carga (ETL) de 79 relatórios consolidados por pasta.
* **Power BI**: Modelagem de dados (Star Schema), criação de medidas em DAX e construção do dashboard interativo.
* **Git & GitHub**: Versionamento de código, controle de alterações e documentação do projeto.

---

## Tratamento de Dados e LGPD
Para garantir a segurança das informações comerciais e o cumprimento da Lei Geral de Proteção de Dados (LGPD):
1. Os relatórios brutos no formato `.xls` foram armazenados em um diretório local e protegidos pelo `.gitignore`.
2. Foi desenvolvido um script Python (`scripts/anonymize.py`) que percorre todos os arquivos brutos, substitui o nome da razão social dos clientes por códigos fictícios padronizados (`CLIENTE ANONIMO XXXX`) mantendo a consistência do ID, e anonimiza o nome da empresa.
3. Os dados anonimizados resultantes foram salvos no diretório `data/processed/` para consumo no Power BI.

---

## Estrutura do Repositório
```text
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

Indicadores e Metricas Planejadas (KPIs)
Faturamento Total (R$)

Volume de Unidades Vendidas

Ticket Médio por Venda

Lucratividade e Margem de Lucro por Produto e Categoria

Curva ABC de Produtos

Evolução Temporal e Comparativos (YoY / MoM)

Autora
Desenvolvido por Kátia Dutra.

LinkedIn (adicione seu link)

GitHub
