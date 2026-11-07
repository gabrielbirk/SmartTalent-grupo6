## Sobre o Projeto
Este repositório contém o pipeline de engenharia e tratamento de dados desenvolvido para um case de manufatura. O projeto utiliza um dataset público extraído do Kaggle (*Manufacturing Defect Dataset*), com o objetivo de analisar a eficiência operacional da linha de montagem, validar a integridade física dos registros e investigar o impacto de métricas de manutenção e custos na taxa de defeitos industriais.

## Como Rodar o Projeto do Zero

### Pré-requisitos
- Python 3.10 ou superior
- Git instalado

### Passo a Passo
1. **Clonar o repositório:**
   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd <NOME_DA_PASTA_DO_PROJETO>
   ```

2. **Criar e ativar o ambiente virtual:**
    ```bash
    Linux/macOS:
    python3 -m venv .venv
    source .venv/bin/activate
    
    Windows (PowerShell):
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

3. **Instalar as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Executar o pipeline:**
    ```bash
    python src/pipeline.py
    ```

## Regras de Negócio e Tratamento de Dados 
O pipeline executa validações de qualidade e integridade analítica sobre o dataset:
1. Validação de Limites Físicos: Verificação e remoção de inconformidades operacionais impossíveis (ex: taxas de inatividade > 100% ou eficiência energética <= 0).
2. Normalização de Escala (Custo Unitário): Criação da métrica UnitCost (ProductionCost / ProductionVolume) para normalizar o investimento financeiro e permitir a comparação justa entre lotes de tamanhos heterogêneos.
3. Detecção e Remoção Defensiva de Outliers (IQR): Aplicação do método estatístico do Intervalo Interquartil (IQR) com fator 1.5 sobre a métrica de custo unitário, identificando e filtrando 284 lotes atípicos. Essa remoção blinda as análises futuras contra ruídos severos (ex: falhas catastróficas e retrabalhos atípicos), focando a base na operação padrão da fábrica.