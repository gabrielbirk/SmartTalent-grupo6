## Sobre o Projeto

Este repositório contém o projeto de análise de dados desenvolvido em grupo durante o programa **Smart Talent**, uma iniciativa do Instituto Caldeira em parceria com a John Deere.

O objetivo do projeto é analisar indicadores operacionais de manufatura, investigando possíveis associações entre condições de produção, manutenção, custos, eficiência energética e níveis de defeitos.

A análise busca responder à seguinte pergunta de negócio:

**Quais condições operacionais estão associadas a maiores níveis de defeitos na manufatura e como se relacionam com custos e eficiência?**

Para desenvolver o projeto, foi utilizado um dataset público e sintético disponibilizado no Kaggle. Portanto, os resultados representam exclusivamente os dados desse conjunto e não informações reais da operação industrial da John Deere.

## Dataset

- **Fonte:** [Kaggle — Predicting Manufacturing Defects Dataset](https://www.kaggle.com/datasets/rabieelkharoua/predicting-manufacturing-defects-dataset)
- **Total de registros:** 3.240
- **Total de colunas originais:** 17
- **Formato original:** CSV

Os dados contêm informações relacionadas à produção, manutenção, consumo de energia, custos, qualidade e ocorrência de defeitos.

## Tecnologias e Ferramentas

- **Databricks:** ambiente de desenvolvimento e processamento dos dados.
- **Python:** linguagem utilizada no desenvolvimento do pipeline.
- **PySpark:** processamento, transformação e análise dos dados.
- **Spark SQL:** acesso e manipulação das tabelas no Databricks.
- **Matplotlib:** criação das visualizações.
- **Git e GitHub:** versionamento e compartilhamento do projeto.

## Estrutura do Repositório

```text
SmartTalent-grupo6/
│
├── src/
│   └── pipeline.py
│
├── pipeline.ipynb
├── modelo_baseline.ipynb
├── modelo.joblib
├── README.md
├── requirements.txt
└── .gitignore
```

- `src/pipeline.py`: contém as funções responsáveis pelo carregamento, validação, transformação e análise dos dados, além da geração dos gráficos.
- `pipeline.ipynb`: notebook Databricks utilizado para executar o pipeline, documentar as etapas e apresentar os resultados.
- `modelo_baseline.ipynb`: treinamento e avaliação do modelo de Machine Learning.
- `modelo.joblib`: modelo treinado e salvo para reutilização.
- `README.md`: documentação do projeto.
- `requirements.txt`: arquivo de referência das dependências Python.
- `.gitignore`: define os arquivos e diretórios que não devem ser enviados ao repositório.

## Metodologia e Tratamento dos Dados

O processamento foi organizado em etapas, seguindo uma abordagem de análise e transformação dos dados.

### 1. Carregamento dos dados

Os dados são carregados diretamente da tabela disponibilizada no Databricks:

`workspace.default.manufacturing_defect_dataset`

### 2. Verificação da qualidade dos dados

Foram realizadas verificações para identificar possíveis problemas de qualidade, incluindo:

- Valores nulos por coluna;
- Registros duplicados;
- Horas de manutenção negativas;
- Volume de produção menor ou igual a zero;
- Custos de produção negativos;
- Percentuais de inatividade fora do intervalo de 0 a 100;
- Valores de eficiência energética menores ou iguais a zero;
- Classificações de defeitos diferentes de 0 ou 1.

As verificações realizadas não identificaram inconsistências nas regras de qualidade avaliadas. Considerando a natureza sintética e a homogeneidade do dataset, optou-se por preservar a totalidade dos registros, sem remoções ou correções.

Os valores atípicos identificados pelo método IQR também foram mantidos e sinalizados por uma coluna indicadora, permitindo análises específicas sem perda de informações.

### 3. Criação de indicadores derivados

Foram criadas duas métricas para aprofundar a análise:

- **UnitCost:** custo de produção dividido pelo volume produzido, permitindo comparar o custo médio por unidade.
- **EnergyPerUnit:** consumo de energia dividido pelo volume produzido, permitindo avaliar o consumo energético por unidade produzida.

### 4. Identificação de outliers

Foi utilizado o método do Intervalo Interquartil (IQR), com fator 1,5, para identificar valores atípicos na métrica `UnitCost`.

Foram identificados 284 registros classificados como outliers, aproximadamente 8,77% da base analisada.

Esses registros foram preservados, sem exclusão automática, e identificados por meio da coluna `IsUnitCostOutlier`.

A decisão permite manter informações potencialmente relevantes para investigações sobre situações operacionais atípicas.

### 5. Análise comparativa

Os registros foram agrupados conforme a classificação `DefectStatus`:

- `0`: baixo nível de defeitos;
- `1`: alto nível de defeitos.

Foram calculadas médias de indicadores relacionados à taxa de defeitos, qualidade, manutenção, volume de produção, custo unitário e consumo de energia por unidade.

### 6. Visualizações e análises exploratórias

Foram desenvolvidas visualizações e análises para investigar relações entre os indicadores operacionais, de qualidade, custos e eficiência energética, organizadas em três frentes:

- **Frente 1 — Qualidade e defeitos:** comparação da taxa média de defeitos e das horas médias de manutenção entre os grupos classificados com baixo e alto nível de defeitos.
- **Frente 2 — Eficiência operacional:** análise da relação entre volume de produção, custo total, custo unitário e consumo de energia por unidade, incluindo comparações por faixas de volume de produção.
- **Frente 3 — Custos e energia:** investigação da relação entre custo unitário e consumo de energia por unidade, além da comparação entre custo total de produção e consumo total de energia.

Também foi utilizada uma matriz de correlação de Pearson para investigar associações lineares entre os indicadores selecionados.

## Principais Resultados

A análise identificou diferenças entre os grupos classificados com baixo e alto nível de defeitos.

| Indicador | Baixo nível (0) | Alto nível (1) |
|---|---:|---:|
| Total de registros | 517 | 2.723 |
| Taxa média de defeitos | 2,01 | 2,89 |
| Qualidade média | 85,44 | 79,13 |
| Horas médias de manutenção | 6,79 | 12,37 |
| Volume médio de produção | 470,87 | 563,27 |
| Custo unitário médio | 36,28 | 31,26 |
| Energia por unidade | 8,72 | 7,59 |

Os registros classificados com alto nível de defeitos apresentaram maior taxa média de defeitos, menor pontuação média de qualidade e maior quantidade média de horas de manutenção.

Também foi observado que esse grupo apresentou maior volume médio de produção, menor custo unitário médio e menor consumo de energia por unidade.

Esses resultados indicam associações entre determinados indicadores operacionais e os níveis de defeitos. Entretanto, por se tratar de uma análise descritiva de dados sintéticos, não é possível estabelecer relações de causa e efeito.

### Eficiência operacional, custos e energia

Na análise por faixas de volume de produção, observou-se que o custo total médio permaneceu relativamente estável, enquanto o custo unitário médio diminuiu de 65,68 na faixa de menor volume para 14,11 na faixa de maior volume.

Comportamento semelhante foi observado no consumo de energia: o consumo total médio permaneceu relativamente estável, enquanto o consumo de energia por unidade diminuiu de 16,05 para 3,32 entre as mesmas faixas.

Essas reduções nos indicadores unitários devem ser interpretadas com cautela, pois tanto o custo unitário quanto o consumo de energia por unidade são calculados utilizando o volume de produção como denominador. Portanto, os resultados não comprovam, isoladamente, ganhos reais de eficiência ou economia de escala.

Na matriz de correlação de Pearson, foram identificadas associações negativas entre volume de produção e custo unitário (-0,726), e entre volume de produção e consumo de energia por unidade (-0,708). Também foi observada uma associação positiva entre custo unitário e consumo de energia por unidade (0,724).

Entretanto, a correlação entre custo total de produção e consumo total de energia foi praticamente inexistente (-0,007). Da mesma forma, não foram identificadas correlações lineares expressivas entre a taxa de defeitos (DefectRate) e os indicadores selecionados.

### Modelo baseline de Machine Learning

Foi desenvolvido um modelo inicial de classificação utilizando **Random Forest**, com o objetivo de identificar registros classificados com alto nível de defeitos (`DefectStatus = 1`).

**Configuração do experimento:**
- Algoritmo: Random Forest (`n_estimators=100`).
- Variável-alvo: `DefectStatus`.
- Variáveis preditoras: 14 indicadores operacionais, de produção, qualidade, manutenção e energia.
- Divisão dos dados: 80% para treinamento e 20% para teste, com estratificação das classes.

**Resultados no conjunto de teste:**
- Precisão da classe 1: **84,8%**.
- Recall da classe 1: **98,5%**.
- Acurácia: **84,0%**.

A precisão indica que, entre os registros previstos como defeituosos, 84,8% realmente pertenciam à classe 1. O recall indica que o modelo identificou 98,5% dos registros que realmente pertenciam a essa classe.

**Limitações:** o modelo ainda apresenta dificuldade para identificar a classe 0, reconhecendo corretamente apenas 7 dos 103 registros dessa classe no teste. Além disso, o conjunto de dados não possui identificadores de máquina, linha de produção ou período, impossibilitando a separação por grupos recomendada para evitar vazamento de dados. Por isso, foi utilizada uma divisão aleatória estratificada, e os resultados devem ser considerados exploratórios, não uma validação definitiva para uso industrial.

## Como Executar o Projeto

A execução do projeto é realizada no ambiente Databricks.

### Pré-requisitos

- Acesso a um workspace Databricks.
- Repositório conectado ao Databricks por meio de Git Folder.
- Arquivo CSV original do dataset disponível para carregamento.

### Passo a passo

**1. Preparação dos dados**

1. Baixe o arquivo CSV do dataset na plataforma Kaggle.
2. Acesse o workspace Databricks.
3. No menu, selecione a opção **Data Ingestion**.
4. Faça o upload do arquivo CSV e configure a importação para disponibilizar os dados em uma tabela.
5. Utilize o nome de tabela esperado pelo projeto: `workspace.default.manufacturing_defect_dataset`.

**2. Execução do projeto**

1. Abra o Git Folder do repositório `SmartTalent-grupo6`.
2. Selecione a branch `dev`.
3. Abra o notebook `pipeline`.
4. Execute a célula responsável pela importação do pipeline:

```python
from src.pipeline import executar_pipeline
```

5. Execute o pipeline utilizando a tabela de origem:

```python
resultados = executar_pipeline(
    spark,
    "workspace.default.manufacturing_defect_dataset"
)
```

6. Ao final da execução, serão apresentados os resultados das verificações de qualidade, a análise de outliers, a tabela resumida e os gráficos.

O notebook também apresenta as etapas individuais da análise, com explicações, códigos e interpretações dos resultados.