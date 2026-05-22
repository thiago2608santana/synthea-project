from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder.getOrCreate()

    # Função auxiliar para carregar as tabelas via PySpark
    def load_table(table_name):
        catalog_path = f"synthea.{table_name}.{table_name}"
        try:
            print(f"Carregando {catalog_path} via PySpark...")
            return spark.table(catalog_path)
        except Exception as e:
            print(f"Aviso: Tabela {catalog_path} não encontrada. Erro: {e}")
            return None

    # Função auxiliar para realizar o join e adicionar sufixos nas colunas duplicadas
    def join_with_suffix(left_df, right_df, join_keys, right_suffix):
        overlapping_cols = set(left_df.columns).intersection(set(right_df.columns)) - set(join_keys)
        for col in overlapping_cols:
            right_df = right_df.withColumnRenamed(col, f"{col}{right_suffix}")
        return left_df.join(right_df, on=join_keys, how='left')

    # 1. Carregamento dos Dados
    patients = load_table('patients')
    encounters = load_table('encounters')
    conditions = load_table('conditions')
    medications = load_table('medications')
    observations = load_table('observations')
    procedures = load_table('procedures')
    providers = load_table('providers')
    organizations = load_table('organizations')
    payers = load_table('payers')
    print("\nIniciando o cruzamento (joins) das tabelas...")

    if patients is None:
        print("Erro: Tabela base (patients) não encontrada.")
        return

    # 2. Base da Tabela Mestre: Pacientes
    # Renomeamos 'Id' para 'PATIENT' para facilitar as ligações futuras
    master_df = patients.withColumnRenamed('Id', 'PATIENT')

    # 3. Join com Encontros (Consultas/Internações)
    if encounters is not None:
        # Renomeamos 'Id' de encontros para 'ENCOUNTER'
        encounters = encounters.withColumnRenamed('Id', 'ENCOUNTER')
        master_df = join_with_suffix(master_df, encounters, ['PATIENT'], '_encounter')

    # 4. Join com Entidades Relacionadas ao Encontro
    # Profissionais (Médicos)
    if providers is not None and 'PROVIDER' in master_df.columns:
        providers = providers.withColumnRenamed('Id', 'PROVIDER')
        master_df = join_with_suffix(master_df, providers, ['PROVIDER'], '_provider')

    # Organizações (Hospitais/Clínicas)
    if organizations is not None and 'ORGANIZATION' in master_df.columns:
        organizations = organizations.withColumnRenamed('Id', 'ORGANIZATION')
        master_df = join_with_suffix(master_df, organizations, ['ORGANIZATION'], '_org')

    # Seguradoras / Planos de Saúde
    if payers is not None and 'PAYER' in master_df.columns:
        payers = payers.withColumnRenamed('Id', 'PAYER')
        master_df = join_with_suffix(master_df, payers, ['PAYER'], '_payer')

    # 5. Join com Dados Clínicos (Tabelas de um-para-muitos)
    # Dicionário com o nome das tabelas clínicas
    clinical_tables = {
        'condition': conditions,
        'medication': medications,
        'procedure': procedures,
        # 'observation': observations # Comentado intencionalmente: Observations costuma ser GIGANTE (exames, sinais vitais). Descomente com cautela.
    }

    for name, df in clinical_tables.items():
        if df is not None:
            print(f"Fazendo join com {name}s...")

            # Quase todas as tabelas clínicas usam PATIENT e ENCOUNTER como chaves de ligação.
            join_keys = []
            if 'PATIENT' in df.columns and 'PATIENT' in master_df.columns:
                join_keys.append('PATIENT')
            if 'ENCOUNTER' in df.columns and 'ENCOUNTER' in master_df.columns:
                join_keys.append('ENCOUNTER')

            if join_keys:
                master_df = join_with_suffix(master_df, df, join_keys, f'_{name}')

    # 6. Finalização e Exportação
    print(f"\nFormato final da Tabela Mestre (Linhas, Colunas): ({master_df.count()}, {len(master_df.columns)})")

    catalog_output = 'synthea.master_table.master_table'
    print(f"Salvando tabela mestre no catálogo: {catalog_output}")

    # Cria o schema (database) caso não exista antes de salvar a tabela
    spark.sql("CREATE SCHEMA IF NOT EXISTS synthea.master_table")

    # Exporta para o catálogo usando Spark (formato Delta por padrão)
    master_df.write.mode('overwrite').saveAsTable(catalog_output)
    
    print('Processo concluído com sucesso!')

if __name__ == '__main__':
    main()
