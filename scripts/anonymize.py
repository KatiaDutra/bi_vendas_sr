import os
import glob
import pandas as pd
import re

# ============================================================
# CONFIGURAÇÃO: um padrão de arquivo + a coluna onde o cliente
# aparece, para cada tipo de relatório que já conhecemos.
#
# "coluna_cliente" pode ser:
#   - um único índice de coluna (int)   -> formato "código - nome" numa célula só
#   - uma tupla (idx_codigo, idx_nome)  -> código e nome em colunas separadas
# ============================================================
TIPOS_DE_RELATORIO = [
    {
        "nome": "lucratividade",
        "padrao_arquivo": "*_vendas_analitico.xls*",
        "coluna_cliente": 4,          # célula única: "125 - ROKA..." (confirmado via diagnóstico_coluna.py)
        "coluna_empresa": (0, 0),     # linha 0, coluna 0: "Empresa: ..."
        "pasta_saida": "vendas",
    },
    {
        "nome": "positivacao",
        "padrao_arquivo": "*_positivacao.xls*",
        "coluna_cliente": (1, 3),     # código na coluna 1, nome na coluna 3
        "coluna_empresa": None,       # cabeçalho desse relatório é tratado via 'cabecalho_fixo' abaixo
        "pasta_saida": "positivacao",
        "cabecalho_fixo": [
            (0, 4, "EMPRESA DEMO LTDA"),
            (1, 4, "Endereço Demo - Cidade Demo - UF - CEP: 00000-000"),
            (2, 4, "Fone: (00) 00000-0000 - Fax: 00 0000-0000"),
            (3, 4, "CNPJ: 00.000.000/0001-00"),
        ],
    },
    {
        "nome": "vendedor_analitico",
        "padrao_arquivo": "*_vendedor_analitico.xls*",
        "coluna_cliente": 4,          # célula única, mas com formatos variados
        "coluna_empresa": (0, 0),
        "pasta_saida": "vendedor",
    },
]

# Regex único e mais flexível: reconhece um prefixo numérico
# (código sequencial OU CPF/CNPJ com pontos), seguido opcionalmente
# de hífen, seguido do nome. Cobre:
#   "125 - ROKA COMERCIO..."          -> codigo=125
#   "58.093.773 AMANDA SERPA..."      -> codigo=58.093.773
#   "ROKA COMERCIO..." (sem código)   -> não casa, tratado como nome puro
PADRAO_CLIENTE = re.compile(r'^([\d][\d.]*)\s*-?\s*(.+)$')

# Valores que NÃO são clientes de verdade e nunca devem ser mascarados
VALORES_IGNORADOS = {"A VISTA", "TOTAL", "", "CLIENTE", "CÓDIGO", "STATUS", "VALOR"}


def carrega_ou_cria_mapa(caminho_mapa):
    """Carrega o dicionário de mapeamento cliente->nome fictício já usado
    em execuções anteriores, para manter consistência entre meses."""
    if os.path.exists(caminho_mapa):
        df_mapa = pd.read_csv(caminho_mapa, dtype=str)
        mapa = dict(zip(df_mapa["chave"], df_mapa["nome_ficticio"]))
        contador = df_mapa["numero"].astype(int).max() + 1 if len(df_mapa) else 1
        return mapa, contador
    return {}, 1


def salva_mapa(caminho_mapa, mapa):
    linhas = []
    for chave, nome_ficticio in mapa.items():
        numero = int(re.search(r'(\d{4})$', nome_ficticio).group(1))
        linhas.append({"chave": chave, "nome_ficticio": nome_ficticio, "numero": numero})
    pd.DataFrame(linhas).to_csv(caminho_mapa, index=False)


def anonimizar_valor_cliente(texto, mapa, contador):
    """Recebe o texto bruto de uma célula de cliente e devolve a versão
    anonimizada, usando (e atualizando) o mapa de consistência global."""
    texto = str(texto).strip()
    if texto.upper() in VALORES_IGNORADOS or texto.lower() == "nan":
        return texto, contador

    match = PADRAO_CLIENTE.match(texto)
    if match:
        codigo, nome = match.group(1), match.group(2)
        chave = codigo  # código ou CPF viram a chave de consistência
    else:
        codigo, nome = None, texto
        chave = f"NOME::{nome.upper()}"  # sem código: usa o próprio nome como chave

    if chave not in mapa:
        mapa[chave] = f"CLIENTE ANONIMO {contador:04d}"
        contador += 1

    if codigo:
        return f"{codigo} - {mapa[chave]}", contador
    return mapa[chave], contador


def anonimizar_pasta_raw():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_raw = os.path.join(diretorio_atual, "..", "data", "raw")
    pasta_processed = os.path.join(diretorio_atual, "..", "data", "processed")
    os.makedirs(pasta_processed, exist_ok=True)

    caminho_mapa = os.path.join(diretorio_atual, "clientes_mapeados.csv")
    mapa, contador = carrega_ou_cria_mapa(caminho_mapa)

    total_processados = 0

    for tipo in TIPOS_DE_RELATORIO:
        # recursive=True + "**" faz o Python procurar o padrão em QUALQUER
        # nível de subpasta dentro de pasta_raw, não só direto nela.
        caminho_busca = os.path.join(pasta_raw, "**", tipo["padrao_arquivo"])
        arquivos = sorted(glob.glob(caminho_busca, recursive=True))
        if not arquivos:
            print(f"[{tipo['nome']}] Nenhum arquivo encontrado com o padrão '{tipo['padrao_arquivo']}' (buscado em toda a árvore de data/raw).")
            continue

        print(f"\n[{tipo['nome']}] Encontrados {len(arquivos)} arquivo(s).")

        for caminho_arquivo in arquivos:
            nome_arquivo = os.path.basename(caminho_arquivo)
            print(f"  Processando: {nome_arquivo}...")
            try:
                df = pd.read_excel(caminho_arquivo, header=None)

                # Anonimiza o nome da empresa, se esse tipo de relatório tiver
                # uma posição conhecida e fixa para isso.
                if tipo["coluna_empresa"]:
                    lin, col = tipo["coluna_empresa"]
                    if lin < len(df) and col < len(df.columns) and pd.notna(df.iloc[lin, col]):
                        df.iloc[lin, col] = re.sub(
                            r'Empresa:.*', 'Empresa: EMPRESA DEMO LTDA', str(df.iloc[lin, col])
                        )

                # Alguns relatórios têm dados sensíveis da própria empresa
                # (nome da filial, endereço, telefone, CNPJ) espalhados em
                # células fixas específicas, não num texto "Empresa: ...".
                # Sobrescreve cada uma delas por um valor genérico.
                for lin, col, texto_fixo in tipo.get("cabecalho_fixo", []):
                    if lin < len(df) and col < len(df.columns):
                        df.iloc[lin, col] = texto_fixo

                # Anonimiza a(s) coluna(s) de cliente
                coluna_cliente = tipo["coluna_cliente"]
                if isinstance(coluna_cliente, tuple):
                    idx_codigo, idx_nome = coluna_cliente
                    for idx in range(len(df)):
                        valor_nome = df.iloc[idx, idx_nome]
                        if pd.isna(valor_nome) or str(valor_nome).strip() == "":
                            continue
                        # Pula linhas de cabeçalho da tabela (ex: a própria
                        # palavra "CLIENTE" usada como rótulo de coluna),
                        # antes de qualquer tentativa de anonimizar.
                        if str(valor_nome).strip().upper() in VALORES_IGNORADOS:
                            continue
                        # Junta código (se houver) + nome para reaproveitar a
                        # mesma lógica de anonimização usada nos outros formatos
                        codigo_valor = df.iloc[idx, idx_codigo]
                        texto_junto = f"{codigo_valor} {valor_nome}" if pd.notna(codigo_valor) else str(valor_nome)
                        anonimizado, contador = anonimizar_valor_cliente(texto_junto, mapa, contador)
                        # Recoloca só o nome anonimizado na coluna de nome,
                        # mantendo o código original na coluna de código
                        nome_ficticio = anonimizado.split(" - ")[-1]
                        df.iloc[idx, idx_nome] = nome_ficticio
                else:
                    idx_nome = coluna_cliente
                    for idx in range(len(df)):
                        valor = df.iloc[idx, idx_nome]
                        if pd.isna(valor):
                            continue
                        anonimizado, contador = anonimizar_valor_cliente(valor, mapa, contador)
                        df.iloc[idx, idx_nome] = anonimizado

                caminho_saida = os.path.join(
                    pasta_processed, tipo["pasta_saida"], nome_arquivo.replace(".xls", "_anonimizado.xlsx")
                )
                os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
                df.to_excel(caminho_saida, index=False, header=False)
                total_processados += 1
            except Exception as e:
                print(f"  Erro ao processar {nome_arquivo}: {e}")

    salva_mapa(caminho_mapa, mapa)
    print(f"\nConcluído! {total_processados} arquivo(s) anonimizado(s) salvos em 'data/processed'.")
    print(f"Mapa de consistência salvo em: {caminho_mapa}")


if __name__ == "__main__":
    anonimizar_pasta_raw()
