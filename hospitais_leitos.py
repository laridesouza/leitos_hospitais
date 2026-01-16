# %% 
import pandas as pd 

df = pd.read_csv("data\Leitos_2025.csv", sep=';', encoding='latin-1')
df.head()
# %%
df.columns

# %%

colunas = ["REGIAO", "UF", "MUNICIPIO", "NOME_ESTABELECIMENTO", "TP_GESTAO", "LEITOS_EXISTENTES", "LEITOS_SUS", "UTI_TOTAL_EXIST", "UTI_TOTAL_SUS", "UTI_ADULTO_EXIST", "UTI_ADULTO_SUS"]

leitos = df[colunas].copy()
leitos.head()
# %%

# criando dicionário para tipos de gestão
mapa_tp_gestao = {
    "M": "Municipal",
    "E": "Estadual",
    "D": "Dupla",
    "S": "Sem Gestão"
}

# criando uma nova coluna com o dicionário aplicado 

leitos["TP_GESTAO_DESC"] = leitos["TP_GESTAO"].map(mapa_tp_gestao)
# %%

# ordenando colunas do dataframe
colunas_ordenadas = [
    "REGIAO", "UF", "MUNICIPIO",
    "NOME_ESTABELECIMENTO",
    "TP_GESTAO", "TP_GESTAO_DESC",
    "LEITOS_EXISTENTES", "LEITOS_SUS",
    "UTI_TOTAL_EXIST", "UTI_TOTAL_SUS",
    "UTI_ADULTO_EXIST", "UTI_ADULTO_SUS"
]

leitos = leitos[colunas_ordenadas]
leitos.head()
# %%

leitos.info() # informações básicas do dataset
leitos.describe() # estatísticas descritivas dataset 

# %% 
# checagem de dados

# leitos SUS maiores que leitos existentes
(leitos["LEITOS_SUS"] > leitos["LEITOS_EXISTENTES"]).sum()

# UTI total maior que leitos existentes
(leitos["UTI_TOTAL_EXIST"] > leitos["LEITOS_EXISTENTES"]).sum()


#UTI SUS maior que UTI total
(leitos["UTI_TOTAL_SUS"] > leitos["UTI_TOTAL_EXIST"]).sum()

# %% 

# criando indicadores

# indicador de hospital com UTI
leitos["TEM_UTI"] = (leitos["UTI_TOTAL_EXIST"] > 0).astype(int)
leitos["TEM_UTI"].value_counts(normalize=True)

# % de leitos SUS
leitos["PERC_LEITOS_SUS"] = (
    leitos["LEITOS_SUS"] / leitos["LEITOS_EXISTENTES"]
).fillna(0)

# % de UTIs no total de leitos
leitos["PERC_TOTAL_UTI"] = (
    leitos["UTI_TOTAL_EXIST"] / leitos["LEITOS_EXISTENTES"]
).fillna(0)

# % de UTIs SUS
leitos["PERC_UTI_SUS"] = (
    leitos["UTI_TOTAL_SUS"] / leitos["UTI_TOTAL_EXIST"]
).fillna(0)

# hospitais SUS dependente
leitos["ALTA_DEP_SUS"] = (leitos["PERC_LEITOS_SUS"] >= 0.8).astype(int)

# porte do hospital 
def classificar_porte(leitos):
    if leitos <= 50:
        return "Pequeno"
    elif leitos <= 150:
        return "Médio"
    else:
        return "Grande"

leitos["PORTE_HOSPITAL"] = leitos["LEITOS_EXISTENTES"].apply(classificar_porte)
# %%

leitos.to_csv("data\leitos_hospitais.csv", index=False)

