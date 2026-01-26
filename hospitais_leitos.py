# %%
import pandas as pd

# leitura dos dados
df = pd.read_csv(
    "data/Leitos_2025.csv",
    sep=";",
    encoding="latin-1"
)

# seleção de colunas relevantes
colunas = [
    "REGIAO", "UF", "MUNICIPIO", "NOME_ESTABELECIMENTO",
    "TP_GESTAO", "LEITOS_EXISTENTES", "LEITOS_SUS",
    "UTI_TOTAL_EXIST", "UTI_TOTAL_SUS",
    "UTI_ADULTO_EXIST", "UTI_ADULTO_SUS"
]

leitos = df[colunas].copy()

# dicionário para tipos de gestão
mapa_tp_gestao = {
    "M": "Municipal",
    "E": "Estadual",
    "D": "Dupla",
    "S": "Sem Gestão"
}

# criação da coluna descritiva
leitos["TP_GESTAO_DESC"] = leitos["TP_GESTAO"].map(mapa_tp_gestao)

# ordenação das colunas
colunas_ordenadas = [
    "REGIAO", "UF", "MUNICIPIO",
    "NOME_ESTABELECIMENTO",
    "TP_GESTAO", "TP_GESTAO_DESC",
    "LEITOS_EXISTENTES", "LEITOS_SUS",
    "UTI_TOTAL_EXIST", "UTI_TOTAL_SUS",
    "UTI_ADULTO_EXIST", "UTI_ADULTO_SUS"
]

leitos = leitos[colunas_ordenadas]

# checagens básicas de consistência
leitos["LEITOS_SUS"] = leitos["LEITOS_SUS"].clip(lower=0)
leitos["UTI_TOTAL_EXIST"] = leitos["UTI_TOTAL_EXIST"].clip(lower=0)
leitos["UTI_TOTAL_SUS"] = leitos["UTI_TOTAL_SUS"].clip(lower=0)

# classificação do porte do hospital
def classificar_porte(qtd_leitos):
    if qtd_leitos <= 50:
        return "Pequeno"
    elif qtd_leitos <= 150:
        return "Médio"
    else:
        return "Grande"

leitos["PORTE_HOSPITAL"] = leitos["LEITOS_EXISTENTES"].apply(classificar_porte)

# exportação do arquivo tratado
leitos.to_csv("data\Leitos_2025_tratado", index=False)


