import pandas as pd

# 1. Comandos Iniciais
# cria variavel e lê o arquivo CSV
df = pd.read_csv('data/manufacturing_defect_dataset.csv')
# exibe primeiras linhas
print(df.head(20))
# verifica se possui valores nulos
print(f'Valores nulos: \n{df.isnull().sum()}')
# verifica se possui linhas duplicadas
print(f'Total de linhas duplicadas: \n{df.duplicated().sum()}')
# verifica resumo estatístico:
print(f'Resumo estatístico: \n{df.describe()}')

# verifica se possui valores negativos nas colunas de horas manutenção, volume produção e custo produção
print(df[(
    df['MaintenanceHours'] < 0) |
     (df['ProductionVolume'] < 0) |
     (df['ProductionCost'] < 0)][['MaintenanceHours', 'ProductionVolume', 'ProductionCost']])

# 2. Validação de Regras de Negócio / Limites Físicos
print('\n *** VALIDAÇÃO DE REGRAS DE NEGÓCIO ***')
# verifica se possui percentual de inatividade maior que 100%
downtime_invalido = df[df['DowntimePercentage'] > 100]
print(f'Quantidade de linhas com Downtime maior que 100%: {len(downtime_invalido)}')
# verifica se possui eficiência energética menor ou igual a zero
eficiencia_invalida = df[df['EnergyEfficiency'] <= 0]
print(f'Quantidade de linhas com Eficiência Energética menor ou igual a zero: {len(eficiencia_invalida)}')

# Análise Exploratória Avançada: Detecção de Outliers de Custo Unitário
# cria uma nova coluna no dataframe chamada UnitCost para custo unitário
df['UnitCost'] = df['ProductionCost'] / df['ProductionVolume']

# calcula os quartis para Custo Unitário
q1 = df['UnitCost'].quantile(0.25)
q3 = df['UnitCost'].quantile(0.75)
# subtrai o valor do primeiro quartil do terceiro quartil
iqr = q3 - q1 # IQR = Intervalo Interquartil

# define limite inferior e superior para outliers
limite_inferior = q1 - 1.5 * iqr # pega o Q1 e subtrai 1.5x o IQR para achar o limite inferior
limite_superior = q3 + 1.5 * iqr # pega o Q3 e soma 1.5x o IQR para achar o limite superior

# filtra os outliers de custo unitário
outliers_custo = df[(df['UnitCost'] < limite_inferior) | (df['UnitCost'] > limite_superior)] # separa lotes que estouraram os limites de custo para baixo ou para cima
print(f"Quantidade de lotes com anomalias de custo unitário: {len(outliers_custo)}")

# aplica filtro para manter apenas os lotes dentro do limite saudável de custo
df_clean = df[(df['UnitCost'] >= limite_inferior) & (df['UnitCost'] <= limite_superior)].copy()

print(f'Total de linhas na base original: {len(df)}')
print(f'Total de linhas na base pós tratamento de custos: {len(df_clean)}')