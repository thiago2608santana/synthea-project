# Análise de Dados de Saúde - Projeto Synthea

Este repositório contém scripts e análises focadas no processamento e exploração de dados sintéticos de pacientes gerados pelo projeto [Synthea](https://synthea.mitre.org). O objetivo é demonstrar técnicas de engenharia de dados (joins complexos), Análise Exploratória de Dados (EDA) e propor metodologias para enriquecimento de dados de saúde usando LLMs.

## 📂 Estrutura do Projeto

* `main.py`: Script Python responsável pela engenharia de dados. Ele lê os múltiplos arquivos CSV brutos (pacientes, consultas, diagnósticos, medicamentos, etc.) e realiza os cruzamentos (joins) adequados para consolidar tudo em uma única Tabela Mestre (`master_table.csv`).
* `EDA_Synthea.ipynb`: Jupyter Notebook contendo a Análise Exploratória de Dados. Inclui limpeza de dados, análise descritiva e visualizações (ex: Distribuição de Despesas de Saúde).
* `description.md`: Dicionário de dados detalhado, descrevendo o propósito de cada tabela do Synthea (Patients, Encounters, Conditions, etc.) e suas respectivas chaves de ligação.
* `enriquecimento_de_dados.md`: Documento de concepção arquitetural com propostas e casos de uso de como Modelos de Linguagem (LLMs) podem ser aplicados para enriquecer os dados brutos (ex: Resumo da Jornada do Paciente, Determinantes Sociais de Saúde, Busca Semântica).
* `synthea_sample_data/`: Diretório (ignorado no versionamento) destinado a armazenar os arquivos CSV brutos do Synthea que alimentam o pipeline.

## 🚀 Como Executar

### Pré-requisitos
* Python 3.8+
* Pandas
* Matplotlib e Seaborn (para o Notebook)

### 1. Preparação dos Dados
Certifique-se de que os arquivos de dados do Synthea (ex: `patients.csv`, `encounters.csv`, `conditions.csv`, etc.) estão dentro da pasta `synthea_sample_data/`.

### 2. Geração da Tabela Mestre
Para processar os dados brutos e gerar a tabela consolidada, execute o script principal:
```bash
python main.py
```
Isso irá cruzar todas as informações e gerar o arquivo `master_table.csv` na pasta de dados.

### 3. Análise Exploratória
Para visualizar as análises e gráficos:
Abra o arquivo `EDA_Synthea.ipynb` no Jupyter Notebook, VS Code ou ambiente de sua preferência e execute as células.

## 💡 Destaques da Análise
* **Engenharia de Dados em Saúde:** Demonstração de como estruturar bancos de dados relacionais complexos em um formato tabular (Flattening), ligando diagnósticos e prescrições ao histórico do paciente.
* **Inteligência Artificial na Saúde:** O arquivo de enriquecimento descreve metodologias avançadas para extrair valor clínico de campos textuais abertos (como descrições de diagnósticos) usando LLMs.
