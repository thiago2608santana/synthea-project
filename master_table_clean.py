from pyspark.sql import SparkSession
import pyspark.sql.functions as F

def main():
    # Inicializa ou obtém a sessão Spark ativa
    spark = SparkSession.builder.getOrCreate()

    # 1. Carregamento dos Dados
    input_table = 'synthea.master_table.master_table'
    print(f"Carregando a tabela mestre inicial de: {input_table}")
    df = spark.read.table(input_table)
    
    # Exibe informações iniciais do dataset
    print(f'Shape inicial do DataFrame: ({df.count()}, {len(df.columns)})')

    # 2. Verificar idas ao hospital antes da morte
    # Agrupa por paciente e conta os encontros únicos ocorridos antes ou no dia do óbito (se houver óbito)
    print("Calculando quantidade de encontros antes do óbito...")
    df_contagem = df.groupBy('PATIENT').agg(
        F.countDistinct(
            F.when(
                F.col('DEATHDATE').isNull() | (F.to_date(F.col('START')) <= F.col('DEATHDATE')),
                F.col('ENCOUNTER')
            )
        ).alias('ENCOUNTER_BEFORE_DEATH')
    )

    df = df.join(df_contagem, on='PATIENT', how='left')

    # 3. Cálculo da idade e criação da coluna AGE
    print("Calculando a idade (AGE)...")
    df = df.withColumn('AGE', F.floor(F.datediff(F.current_date(), F.col('BIRTHDATE')) / 365))

    # 4. Cálculo de tempo decorrido nos encontros (duração)
    print("Calculando tempo decorrido dos encontros (minutos/horas)...")
    df = df.withColumn('ELAPSED_TIME_MINUTES', (F.col('STOP').cast('long') - F.col('START').cast('long')) / 60)
    df = df.withColumn('ELAPSED_TIME_HOURS', (F.col('STOP').cast('long') - F.col('START').cast('long')) / 3600)

    # 5. Tratar a coluna de morte (IS_DEAD) e remover DEATHDATE
    print("Criando flag de óbito (IS_DEAD)...")
    df = df.withColumn('IS_DEAD', F.when(F.col('DEATHDATE').isNull(), 0).otherwise(1))
    df = df.drop('DEATHDATE')

    # 6. Filtrar colunas relevantes e limpar nulos
    print("Filtrando colunas selecionadas para a limpeza...")
    df_clean = df.select(
        'PATIENT', 'ENCOUNTER', 'RACE', 'GENDER', 'BIRTHPLACE', 'HEALTHCARE_EXPENSES',
        'HEALTHCARE_COVERAGE', 'INCOME', 'START', 'STOP', 'DESCRIPTION', 'REASONDESCRIPTION', 'SPECIALITY',
        'DESCRIPTION_procedure', 'ENCOUNTER_BEFORE_DEATH', 'AGE', 'ELAPSED_TIME_MINUTES', 'ELAPSED_TIME_HOURS', 'IS_DEAD'
    )

    # 7. Agrupar os dados por paciente para obter a visão final consolidada
    print("Consolidando dados por paciente (groupBy)...")
    df_final = df_clean.groupBy('PATIENT').agg(
        F.countDistinct('ENCOUNTER').alias('DISTINCT_ENCOUNTERS'),
        F.first('RACE').alias('RACE'),
        F.first('GENDER').alias('GENDER'),
        F.first('BIRTHPLACE').alias('BIRTHPLACE'),
        F.round(F.first('HEALTHCARE_EXPENSES'), 2).alias('HEALTHCARE_EXPENSES'),
        F.round(F.first('HEALTHCARE_COVERAGE'), 2).alias('HEALTHCARE_COVERAGE'),
        F.first('INCOME').alias('INCOME'),
        F.first('ENCOUNTER_BEFORE_DEATH').alias('ENCOUNTER_BEFORE_DEATH'),
        F.first('AGE').alias('AGE'),
        F.round(F.sum('ELAPSED_TIME_MINUTES'), 2).alias('ELAPSED_TIME_MINUTES'),
        F.round(F.sum('ELAPSED_TIME_HOURS'), 2).alias('ELAPSED_TIME_HOURS'),
        F.max('IS_DEAD').alias('IS_DEAD')
    )

    # Exibe amostra dos dados finais
    print("\nAmostra dos dados finais consolidados:")
    df_final.show(5, truncate=False)

    # 8. Exportação da Tabela Mestre Limpa
    catalog_output = 'synthea.master_table.master_table_clean'
    print(f"\nSalvando tabela mestre limpa no catálogo: {catalog_output}")

    # Cria o schema (database) caso não exista antes de salvar a tabela
    spark.sql("CREATE SCHEMA IF NOT EXISTS synthea.master_table")

    # Exporta para o catálogo usando Spark (formato Delta por padrão)
    df_final.write.mode('overwrite').saveAsTable(catalog_output)
    print('Processo concluído com sucesso!')

if __name__ == '__main__':
    main()
