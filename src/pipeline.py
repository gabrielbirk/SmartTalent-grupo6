# 1. IMPORTAÇÃO DAS BIBLIOTECAS
from pyspark.sql import functions as F
import matplotlib.pyplot as plt

# 2. LEITURA DOS DADOS
def carregar_dados(spark, nome_tabela):
    # carrega os dados diretamente de uma tabela do Databricks
    df = spark.table(nome_tabela)

    print("Dataset carregado com sucesso!")
    print(f"Total de registros: {df.count()}")
    print(f"Total de colunas: {len(df.columns)}")
    return df

# 3. VERIFICAÇÃO DA QUALIDADE DOS DADOS
def verificar_qualidade(df):
    print("\n========== QUALIDADE DOS DADOS ==========")

    # verificação de valores nulos
    print("\nValores nulos por coluna:")
    for coluna in df.columns:
        quantidade = df.filter(F.col(coluna).isNull()).count()
        print(f"{coluna}: {quantidade}")

    # verificação de registros duplicados
    total_original = df.count()
    total_unicos = df.dropDuplicates().count()
    duplicados = total_original - total_unicos
    print(f"\nTotal de registros duplicados: {duplicados}")

    # verificação de valores inválidos
    regras_validacao = {
        "MaintenanceHours negativas":
            F.col("MaintenanceHours") < 0,
        "ProductionVolume menor ou igual a zero":
            F.col("ProductionVolume") <= 0,
        "ProductionCost negativa":
            F.col("ProductionCost") < 0,
        "DowntimePercentage fora do intervalo de 0 a 100":
            (F.col("DowntimePercentage") < 0) |
            (F.col("DowntimePercentage") > 100),
        "EnergyEfficiency menor ou igual a zero":
            F.col("EnergyEfficiency") <= 0,
        "DefectStatus diferente de 0 ou 1":
            ~F.col("DefectStatus").isin(0, 1)
    }

    print("\nVerificação das regras de validade:")
    for descricao, condicao in regras_validacao.items():
        quantidade = df.filter(condicao).count()
        print(f"{descricao}: {quantidade}")

# 4. TRANSFORMAÇÃO DOS DADOS
def criar_indicadores(df):

    # cria indicadores derivados para as análises do projeto
    df_silver = (
        df
        .withColumn(
            "UnitCost",
            F.when(
                F.col("ProductionVolume") > 0,
                F.col("ProductionCost") / F.col("ProductionVolume")
            )
        )
        .withColumn(
            "EnergyPerUnit",
            F.when(
                F.col("ProductionVolume") > 0,
                F.col("EnergyConsumption") / F.col("ProductionVolume")
            )
        )
    )
    return df_silver

# 5. IDENTIFICAÇÃO DE OUTLIERS

def identificar_outliers(df):
    
    # identifica valores atípicos de custo unitário pelo método IQR. Os registros são preservados. Uma coluna indicadora identifica os valores acima ou abaixo dos limites
    quartis = df.approxQuantile("UnitCost", [0.25, 0.75], 0.01)

    q1 = quartis[0]
    q3 = quartis[1]
    iqr = q3 - q1

    limite_inferior = q1 - (1.5 * iqr)
    limite_superior = q3 + (1.5 * iqr)

    df_silver = df.withColumn(
        "IsUnitCostOutlier",
        F.when(
            (F.col("UnitCost") < limite_inferior) |
            (F.col("UnitCost") > limite_superior),
            1
        ).otherwise(0)
    )

    quantidade_outliers = df_silver.filter(
        F.col("IsUnitCostOutlier") == 1
    ).count()

    print("\n========== ANÁLISE DE OUTLIERS ==========")
    print(f"Primeiro quartil (Q1): {q1:.2f}")
    print(f"Terceiro quartil (Q3): {q3:.2f}")
    print(f"Intervalo interquartil (IQR): {iqr:.2f}")
    print(f"Limite inferior: {limite_inferior:.2f}")
    print(f"Limite superior: {limite_superior:.2f}")
    print(f"Quantidade de outliers: {quantidade_outliers}")
    print("Os registros foram preservados.")
    print("=========================================")
    return df_silver

# 6. TABELA RESUMIDA POR NÍVEL DE DEFEITOS
def criar_tabela_resumo(df):

    # calcula indicadores médios separados por DefectStatus
    tabela_resumo = (
        df.groupBy("DefectStatus")
        .agg(
            F.count("*").alias("TotalRegistros"),
            F.round(
                F.avg("DefectRate"), 2
            ).alias("TaxaDefeitoMedia"),

            F.round(
                F.avg("QualityScore"), 2
            ).alias("QualidadeMedia"),

            F.round(
                F.avg("MaintenanceHours"), 2
            ).alias("HorasManutencaoMedia"),

            F.round(
                F.avg("ProductionVolume"), 2
            ).alias("VolumeProducaoMedio"),

            F.round(
                F.avg("UnitCost"), 2
            ).alias("CustoUnitarioMedio"),

            F.round(
                F.avg("EnergyPerUnit"), 2
            ).alias("EnergiaPorUnidadeMedia")
        )
        .orderBy("DefectStatus")
    )
    return tabela_resumo

# 7. CRIAÇÃO DOS GRÁFICOS

def criar_graficos(tabela_resumo):

    # gera os gráficos de taxa de defeitos e horas de manutenção
    dados = tabela_resumo.toPandas()
    categorias = ["Baixo nível de defeitos", "Alto nível de defeitos"]

    # Gráfico 1: Taxa média de defeitos
    valores_defeitos = dados["TaxaDefeitoMedia"]
    plt.figure(figsize=(9, 5))
    plt.bar(categorias, valores_defeitos)
    plt.title("Registros com alto nível de defeitos apresentam maior taxa média")
    plt.xlabel("Classificação de defeitos")
    plt.ylabel("Taxa média de defeitos")

    for i, valor in enumerate(valores_defeitos):
        plt.text(i, valor + 0.03, str(valor), ha="center")

    plt.tight_layout()
    plt.show()

    # Gráfico 2: Horas médias de manutenção
    valores_manutencao = dados["HorasManutencaoMedia"]
    plt.figure(figsize=(9, 5))
    plt.bar(categorias, valores_manutencao)
    plt.title("Registros com alto nível de defeitos apresentam mais horas de manutenção")
    plt.xlabel("Classificação de defeitos")
    plt.ylabel("Média de horas de manutenção")

    for i, valor in enumerate(valores_manutencao):
        plt.text(i, valor + 0.15, str(valor), ha="center")

    plt.tight_layout()
    plt.show()

# 8. EXECUÇÃO COMPLETA DO PIPELINE

def executar_pipeline(spark, nome_tabela):
    # executa todas as etapas do pipeline e retorna os resultados

    # Leitura
    df = carregar_dados(spark, nome_tabela)

    # Verificação da qualidade
    verificar_qualidade(df)

    # Criação dos indicadores
    df_silver = criar_indicadores(df)

    # Identificação de outliers
    df_silver = identificar_outliers(df_silver)

    # Tabela resumida
    tabela_resumo = criar_tabela_resumo(df_silver)

    print("\n========== TABELA RESUMIDA ==========")
    tabela_resumo.show(truncate=False)

    # Gráficos
    criar_graficos(tabela_resumo)

    print("\nPipeline executado com sucesso!")

    return {
        "dados_originais": df,
        "dados_processados": df_silver,
        "tabela_resumo": tabela_resumo
    }