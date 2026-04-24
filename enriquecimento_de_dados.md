1. Colunas de DESCRIPTION (Tabelas Clínicas)
Em quase todas as tabelas (conditions, medications, procedures, observations), existe uma coluna de texto livre chamada DESCRIPTION.
* Enriquecimento via LLM: Você pode pedir ao modelo para classificar a gravidade da doença, explicar o termo em linguagem leiga para o paciente, ou agrupar medicamentos em "Classes Terapêuticas" (ex:
    "Lisinopril" -> "Anti-hipertensivo").
* Exemplo de Prompt: "Dado o diagnóstico 'Diabetes Mellitus tipo 2', qual é a gravidade típica e quais são os 3 principais riscos para o paciente?"

2. Colunas de ADDRESS, CITY e STATE (Tabela patients)
Estas colunas trazem dados geográficos que, por si só, dizem pouco sobre a saúde.
* Enriquecimento (SDoH - Determinantes Sociais de Saúde): Um LLM pode cruzar essas informações (se alimentado com contexto externo ou ferramentas de busca) para estimar o IDH da região, acesso a áreas verdes,
    ou se o paciente vive em um "deserto alimentar" (longe de mercados com comida fresca).
* Nova Feature: Social_Vulnerability_Index.

3. Colunas REASONDESCRIPTION (Tabela medications e procedures)
Esta coluna explica por que algo foi feito.
* Enriquecimento (Análise de Causalidade): Você pode usar um LLM para verificar a aderência ao protocolo. Por exemplo: "O medicamento X é comumente prescrito para a razão Y?".
* Nova Feature: Protocol_Alignment_Score (uma nota de 0 a 1 indicando se o tratamento é o padrão ouro para aquela condição).

4. Criação de Narrativas Clínicas (Summarization)
O maior ganho com LLMs aqui é o "Patient Journey Summary".
* Como fazer: Você concatena as descrições dos encontros, condições e medicamentos de um paciente em ordem cronológica e pede ao LLM: "Gere um resumo clínico de 3 parágrafos sobre a evolução deste paciente nos
    últimos 2 anos".
* Utilidade: Isso transforma linhas frias de CSV em um "relatório de passagem de plantão" que um médico entenderia instantaneamente.

5. Embeddings para Busca Semântica
Em vez de usar apenas o texto, você pode passar a coluna DESCRIPTION por um modelo de Embedding (como os da OpenAI, Titan ou Llama).
* Utilidade: Isso permite que você encontre "Pacientes Similares" não apenas por códigos idênticos, mas por contexto clínico. Um paciente com "Dificuldade respiratória" será mapeado para perto de um com
    "Dispneia", mesmo que os termos sejam diferentes no CSV.

Exemplo Prático de Nova Coluna Enriquecida:

┌─────────────────────────────┬──────────────────────────────────────────┬───────────────────────────────────────┐
│ Coluna Original (Condition) │ Feature Enriquecida por LLM (Risk_Level) │ Feature Enriquecida (System_Affected) │
├─────────────────────────────┼──────────────────────────────────────────┼───────────────────────────────────────┤
│ "Acute Bronchitis"          │ Baixo                                    │ Respiratório                          │
│ "Myocardial Infarction"     │ Crítico                                  │ Cardiovascular                        │
│ "Prediabetes"               │ Médio                                    │ Endócrino                             │
└─────────────────────────────┴──────────────────────────────────────────┴───────────────────────────────────────┘