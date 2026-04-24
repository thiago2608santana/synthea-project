Os dados são provenientes de uma simulação feita pelo projeto Synthea.
Segue a url do projeto: https://synthea.mitre.org

1. Patients (Pacientes)
Esta tabela contém os dados demográficos e de identificação.
* Id: Identificador único universal do paciente (UUID).
* BIRTHDATE / DEATHDATE: Datas de nascimento e óbito (se aplicável).
* MARITAL: Estado civil (M=Casado, S=Solteiro).
* RACE / ETHNICITY: Dados sociodemográficos para análise de equidade em saúde.
* GENDER: Sexo biológico (M/F).
* HEALTHCARE_EXPENSES / COVERAGE: Total acumulado gasto em saúde e quanto foi coberto por planos ao longo da vida.

2. Encounters (Encontros/Consultas)
Representa cada interação do paciente com o sistema de saúde.
* Id: Identificador único da consulta.
* START / STOP: Quando a consulta começou e terminou.
* ENCOUNTERCLASS: O tipo da consulta (ex: wellness para rotina, emergency para urgência, ambulatory para ambulatório, inpatient para internação).
* BASE_ENCOUNTER_COST: O custo administrativo base da consulta.
* TOTAL_CLAIM_COST: O valor total cobrado (incluindo procedimentos e exames realizados nela).

3. Conditions (Condições/Diagnósticos)
Registra os problemas de saúde, doenças ou diagnósticos confirmados.
* START / STOP: Quando a doença foi diagnosticada e quando foi curada/resolvida (se estiver em branco, a condição é crônica ou atual).
* CODE: Código clínico (geralmente no padrão SNOMED-CT).
* DESCRIPTION: Nome amigável da doença (ex: "Diabetes Mellitus", "Hypertension").

4. Observations (Observações/Exames)
É a tabela mais volumosa. Contém medições, sinais vitais e resultados de exames laboratoriais.
* DATE: Quando a medição foi feita.
* CATEGORY: Tipo da observação (ex: vital-signs, laboratory, social-history).
* DESCRIPTION: O que foi medido (ex: "Body Height", "Glucose", "Body Mass Index").
* VALUE / UNITS: O valor numérico e a unidade de medida (ex: 70 / kg).

5. Medications (Medicamentos)
Registra as prescrições de remédios.
* START / STOP: Período em que o paciente deve tomar o medicamento.
* CODE / DESCRIPTION: Código (padrão RxNorm) e nome do remédio (ex: "Amoxicillin 250mg").
* REASONCODE / REASONDESCRIPTION: O motivo (doença) pelo qual o remédio foi passado (liga-se à tabela Conditions).
* BASE_COST / TOTALCOST: Custos da medicação.

6. Procedures (Procedimentos)
Registra cirurgias, exames físicos complexos ou terapias.
* DATE: Quando o procedimento foi realizado.
* DESCRIPTION: Nome do procedimento (ex: "Colonoscopy", "Suture of wound").
* BASE_COST: Custo direto do procedimento.

7. Providers & Organizations (Médicos e Instituições)
* Providers: Dados sobre os profissionais (médicos, enfermeiros). Inclui a SPECIALITY (Especialidade).
* Organizations: Dados sobre o local físico (Hospitais, Clínicas). Contém o REVENUE (faturamento total daquela unidade).

8. Payers (Pagadores)
Dados sobre as seguradoras ou sistemas públicos (ex: Medicare, Medicaid ou seguradoras privadas). Permite analisar quem está financiando o sistema de saúde.

9. Claims (Sinistros/Reivindicações)
Esta é a tabela financeira que consolida tudo. Ela mostra quanto de dinheiro foi solicitado para pagamento, quanto foi negado e quais diagnósticos justificaram aquela cobrança.

---

Resumo das Chaves de Ligação (ID's):
* Se você quiser saber quem é a pessoa: Use PATIENT (liga com patients.csv).
* Se você quiser saber quando/onde aconteceu: Use ENCOUNTER (liga com encounters.csv).
* Se você quiser saber por que foi feito: Use REASONCODE (liga com a coluna CODE de conditions.csv).