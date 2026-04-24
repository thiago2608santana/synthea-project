import pandas as pd
import os

def main():
    # Caminho para o diretório de dados
    data_dir = './synthea_sample_data/'

    # Função auxiliar para carregar os CSVs com segurança
    def load_csv(filename):
        path = os.path.join(data_dir, filename)
        if os.path.exists(path):
            print(f"Carregando {filename}...")
            return pd.read_csv(path, low_memory=False)
        else:
            print(f"Aviso: Arquivo {filename} não encontrado.")
            return pd.DataFrame()

    # 1. Carregamento dos Dados
    patients = load_csv('patients.csv')
    encounters = load_csv('encounters.csv')
    conditions = load_csv('conditions.csv')
    medications = load_csv('medications.csv')
    observations = load_csv('observations.csv')
    procedures = load_csv('procedures.csv')
    providers = load_csv('providers.csv')
    organizations = load_csv('organizations.csv')
    payers = load_csv('payers.csv')
    print("\nIniciando o cruzamento (joins) das tabelas...")

    # 2. Base da Tabela Mestre: Pacientes
    # Renomeamos 'Id' para 'PATIENT' para facilitar as ligações futuras
    master_df = patients.rename(columns={'Id': 'PATIENT'})

    # 3. Join com Encontros (Consultas/Internações)
    if not encounters.empty:
        # Renomeamos 'Id' de encontros para 'ENCOUNTER'
        encounters = encounters.rename(columns={'Id': 'ENCOUNTER'})
        master_df = pd.merge(master_df, encounters, on='PATIENT', how='left', suffixes=('', '_encounter'))

    # 4. Join com Entidades Relacionadas ao Encontro
    # Profissionais (Médicos)
    if not providers.empty and 'PROVIDER' in master_df.columns:
        providers = providers.rename(columns={'Id': 'PROVIDER'})
        master_df = pd.merge(master_df, providers, on='PROVIDER', how='left', suffixes=('', '_provider'))

    # Organizações (Hospitais/Clínicas)
    if not organizations.empty and 'ORGANIZATION' in master_df.columns:
        organizations = organizations.rename(columns={'Id': 'ORGANIZATION'})
        master_df = pd.merge(master_df, organizations, on='ORGANIZATION', how='left', suffixes=('', '_org'))

    # Seguradoras / Planos de Saúde
    if not payers.empty and 'PAYER' in master_df.columns:
        payers = payers.rename(columns={'Id': 'PAYER'})
        master_df = pd.merge(master_df, payers, on='PAYER', how='left', suffixes=('', '_payer'))

    # 5. Join com Dados Clínicos (Tabelas de um-para-muitos)
    # Dicionário com o nome das tabelas clínicas
    clinical_tables = {
        'condition': conditions,
        'medication': medications,
        'procedure': procedures,
        # 'observation': observations # Comentado intencionalmente: Observations costuma ser GIGANTE (exames, sinais vitais). Descomente com cautela.
    }

    for name, df in clinical_tables.items():
        if not df.empty:
            print(f"Fazendo join com {name}s...")

            # Quase todas as tabelas clínicas usam PATIENT e ENCOUNTER como chaves de ligação.
            join_keys = []
            if 'PATIENT' in df.columns and 'PATIENT' in master_df.columns:
                join_keys.append('PATIENT')
            if 'ENCOUNTER' in df.columns and 'ENCOUNTER' in master_df.columns:
                join_keys.append('ENCOUNTER')

            if join_keys:
                master_df = pd.merge(master_df, df, on=join_keys, how='left', suffixes=('', f'_{name}'))

    # 6. Finalização e Exportação
    print(f"\nFormato final da Tabela Mestre (Linhas, Colunas): {master_df.shape}")

    output_file = os.path.join(data_dir, 'master_table.csv')
    print(f"Salvando tabela mestre em: {output_file}")

    # Exporta para CSV. Pode demorar alguns minutos dependendo do tamanho da memória RAM
    master_df.to_csv(output_file, index=False)
    print("Processo concluído com sucesso!")


if __name__ == "__main__":
    main()
