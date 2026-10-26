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
| Construção do dashboard visual (4 páginas) | ✅ Concluída |
| Documentação | ✅ Concluída |
| Disponibilização para os usuários | ⏳ Planejada |

---

## Tecnologias e Ferramentas Utilizadas

- **Python**: automação da anonimização em lote dos dados sensíveis (LGPD) e pré-processamento.
- **Power Query (M)**: extração, limpeza, transformação e carga (ETL) de 158 relatórios (79 meses de Lucratividade e 79 de Positivação), consolidados por pasta.
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
3. Os nomes dos vendedores também são anonimizados (`VENDEDOR XX`, a partir do código do vendedor no ERP). LOJA e SITE são mantidos, pois representam canais de venda e não pessoas.
4. Os dados anonimizados resultantes foram salvos no diretório `data/processed/` para consumo no Power BI.

---

## Modelagem de Dados

O modelo foi construído no formato **Star Schema (esquema estrela)**, com as tabelas fato **fVendas** (Lucratividade) e **fPositivacao** ligadas às tabelas dimensão **dCalendario**, **dProduto** e **dVendedor**. Essa estrutura facilita os filtros cruzados no dashboard e melhora o desempenho das medidas em DAX.

A tabela **dCalendario** é gerada em DAX e termina automaticamente no último mês com vendas registradas, de modo que novos meses incluídos no projeto passam a aparecer no calendário e no filtro de datas sem ajustes manuais.

---

## Páginas do Dashboard

O painel possui quatro páginas, todas com um filtro de intervalo de datas sincronizado entre elas:

1. **Visão Geral**: faturamento, margem, ticket médio e clientes positivados, evolução mensal do faturamento, vendas por canal e Top 5 produtos.
2. **Lucratividade**: lucro, margem e custo, margem por grupo de produtos e uma matriz com o detalhamento por produto e a classificação da Curva ABC.
3. **Positivação e Canais**: clientes positivados, vendas e quantidade de vendas, clientes atendidos por vendedor e participação de cada canal nas vendas.
4. **Análise Temporal**: comparação do período selecionado com o mesmo período do ano anterior (YoY) e variação mês a mês (MoM).

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
│   └── anonymize.py   # Script Python de anonimização em lote (clientes, empresa e vendedores)
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

## Como Atualizar com Novos Meses

1. Exportar do ERP os relatórios de Lucratividade e Positivação do mês, com os mesmos filtros dos anteriores.
2. Nomear os arquivos no padrão `AAAA-MM_vendas_analitico.xls` e `AAAA-MM_positivacao.xls` e salvá-los em `data/raw/`.
3. Executar `python scripts/anonymize.py` (o arquivo local `scripts/clientes_mapeados.csv` garante que os códigos fictícios dos clientes se mantenham entre os meses).
4. Abrir o `dashboard_vendas.pbix` e clicar em **Atualizar**.

---

## Autora

Desenvolvido por **Kátia Dutra**.

- [LinkedIn](http://www.linkedin.com/in/katia-dutra-ss)
- [GitHub](https://github.com/KatiaDutra)

