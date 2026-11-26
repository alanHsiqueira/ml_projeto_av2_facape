# Dicionário de Dados — G02

> E2 — auditoria inicial dos indicadores municipais SINISA para referência
> 2023 → 2024. Perfil e regra inicial de seleção dos preditores documentados.
> A licença específica das planilhas e a comparabilidade metodológica plena
> não foram confirmadas; ver decisões e limitações abaixo.

## 1. Identificação

| Campo | Valor |
| ----- | ----- |
| Fonte | SINISA — Ministério das Cidades, módulo Abastecimento de Água |
| Página oficial | [Resultados SINISA 2024 — referência 2023](https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa/resultados-sinisa); [Resultados SINISA 2025 — referência 2024](https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa/resultados-sinisa/resultados-sinisa-2025) |
| Downloads oficiais | [Planilhas de referência 2023](https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa/arquivos/SINISA_Resultados_Ref2023.zip); [planilhas de referência 2024](https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa/resultados-sinisa/SINISA_Resultados_Ref2024.zip) |
| Documentação | [Glossário de Indicadores de Água](https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa/resultados-sinisa/GlossriodeIndicadores_GUA_2024.pdf) e abas “Nota metodológica” dos arquivos |
| Consulta das páginas | 2026-11-25; reconferência das fontes oficiais em 2026-11-26 |
| Data original de download | Não registrada; confirmar com o grupo |
| Recorte | Brasil; filtro preliminar de IAG2013 numérico e entre 0 e 100% nos dois anos |
| Licença/termos | O rodapé do portal declara [CC BY-ND 3.0](https://creativecommons.org/licenses/by-nd/3.0/) para o conteúdo do site. Não foi identificada licença individual das planilhas nem confirmação de que a declaração geral se aplique aos XLSX. A [página de Dados Abertos do Ministério das Cidades](https://www.gov.br/cidades/pt-br/acesso-a-informacao/dados-abertos) descreve a política federal e o plano do Ministério, mas não identifica estas planilhas como publicadas sob uma licença específica. Não presumir CC BY, CC0 ou domínio público; não redistribuir arquivos originais ou bases derivadas até esclarecer os termos com o Ministério |
| Verificação dos termos | Páginas oficiais consultadas em 2026-11-25 e reconferidas em 2026-11-26; nenhum arquivo de licença separado foi localizado no ZIP recebido. A análise registra a incerteza, não constitui parecer jurídico |
| LGPD | Nos campos municipais examinados, não foi identificado dado de pessoa natural. Manter a análise agregada por município e excluir campos de identificação do prestador dos preditores; reavaliar se outras fontes forem combinadas |
| Arquivos locais | `data/raw/` (ignorado pelo Git; não versionar os XLSX) |

| Referência | Arquivo usado | Registros com código IBGE | Colunas de indicadores | SHA-256 |
| ---------- | ------------- | -----------------------: | --------------------: | ------- |
| 2023 | `SINISA_AGUA_Indicadores_Base Municipal_2023.xlsx` | 5.241 | 55 indicadores distintos em quatro abas | `39AD4D8B7433629F08A1FBCF7ADB1CD34D2966D5365EEE654F59145FDCD6FE64` |
| 2024 | `SINISA_AGUA_Indicadores_Base Municipal_2024_Retificação.xlsx` | 5.144 | 57 na aba “Indicadores de Gestão” | `262F74F515B6225B7C9C122576159AB45576AE15628AE67612D7CEE6C333623D` |

As quatro abas de 2023 contêm 75 ocorrências de colunas; cinco campos de
contexto se repetem entre abas. Após deduplicar esses campos, há 55 indicadores
distintos e cinco variáveis de contexto. O perfil por indicador, calculado nos
4.574 municípios pareados, está em
[`../reports/tables/perfil-preditores-ref2023.csv`](../reports/tables/perfil-preditores-ref2023.csv).
Os hashes acima foram recalculados com SHA-256 em 2026-11-26 e conferem com os
valores registrados.

## 2. Critério “não-toy”

| Critério | Situação | Evidência |
| -------- | -------- | --------- |
| (a) proveniência documentada | Atendido | Páginas, instituição, data de consulta, arquivos e hashes identificados acima |
| (b) volume e atributos | Atendido pelo critério de atributos | A amostra pareada tem 4.574 municípios (abaixo de 5.000), mas a base de 2023 contém 55 indicadores distintos (acima do mínimo alternativo de 40 atributos) |
| (c) alvo não trivial | Atendido com ressalva temporal | IAG2013 é calculado a partir de vários componentes; prevê-se 2024 com dados de 2023, sem usar atributos de 2024. As regras de não cálculo diferem entre anos, portanto não se afirma comparabilidade plena |
| (d) licença | Análise documentada; aplicabilidade não confirmada | O site declara CC BY-ND 3.0 para seu conteúdo, mas não foi localizada licença específica para as planilhas. Não redistribuir os arquivos; confirmar com o Ministério antes de publicar dados derivados |

O conjunto é tabular. A amostra efetiva fica abaixo de 5.000; o critério
alternativo de atributos é atendido pelos 55 códigos de indicadores distintos.
Reportar o tamanho real e não aumentar a contagem misturando níveis municipal,
prestador e regional.

## 3. Variáveis e estrutura do pareamento

| Campo | Tipo | Unidade | Faixa / disponibilidade | Descrição | Uso |
| ----- | ---- | ------- | ----------------------- | --------- | --- |
| Código IBGE | Identificador | código municipal | 7 dígitos; sem duplicatas na aba-alvo de cada ano | Chave para vincular referências e conferir municípios | Junção; excluir dos preditores |
| Município / UF | Categórica | — | Presente nos arquivos | Identificação e conferência do recorte | Controle de qualidade; eventual análise por subgrupo |
| Indicadores numéricos de 2023 | Numérica | Conforme glossário oficial | 55 códigos distintos; perfil por código no CSV, calculado nos 4.574 pares | Características disponíveis no ano de entrada | Candidatos segundo a regra inicial abaixo; revisar valores extremos e semântica na E3 |
| Indicadores com >20% de valores indisponíveis | Numérica | Conforme glossário oficial | IAG0005: 45,82%; IAG3001: 36,45%; IAG3002: 64,87%; IAG3007: 34,91% | Indicadores com alta indisponibilidade no perfil pareado | Excluir do conjunto inicial de candidatos; não imputar sem justificativa |
| Natureza jurídica / prestador / sigla | Categórica ou identificador | — | Três campos de contexto; nomes/siglas têm alta cardinalidade | Caracterização do prestador | Excluir dos preditores; manter somente para auditoria local |
| Capital / RM-RIDE | Categórica | — | Muitos brancos; semântica ainda não confirmada | Contexto geográfico | Excluir dos preditores até confirmar a codificação |
| IAG2013 — referência 2023 | Numérica | Percentual | 4.834 valores numéricos; 19 fora de 0–100%; 4.815 dentro da faixa | Perdas totais de água na distribuição em 2023 | Alvo defasado e baseline; pode ser preditor somente por ser do ano anterior |
| IAG2013 — referência 2024 | Numérica | Percentual | 5.110 valores numéricos; 34 sem valor numérico; todos entre 0 e 100% | Perdas totais de água na distribuição em 2024 | Alvo |

O indicador está na coluna `Z` da aba “Estruturais e Operacionais” de 2023 e
na coluna `AG` da aba “Indicadores de Gestão” de 2024. O pareamento usa código
IBGE, não o nome do município. Foram encontrados 4.591 códigos com valores
numéricos nos dois anos; removendo os 17 pares cujo alvo de 2023 está fora de
0–100%, restam **4.574 pares preliminares**. A regra exige alvo válido nos dois
anos, pois IAG2013 de 2023 também será usado para a referência de persistência.
Petrolina (IBGE 2611101) tem 30,17% em 2023 e 27,34% em 2024.

**Regra inicial de seleção:** considerar candidatos numéricos de 2023 com até
20% de valores ausentes/não calculados no perfil pareado. Isso resulta em 51
códigos candidatos: IFA0001, IFA0002, IFA1001–IFA1005, IFA2001–IFA2014,
IFA2016, IAG0001–IAG0004, IAG0006, IAG1001–IAG1004, IAG2001–IAG2016,
IAG2023, IAG3003, IAG3006 e IAG3008. IAG2013 de 2023 é o alvo defasado e
referência temporal, não dado do ano previsto. A regra não garante que cada
candidato entre no modelo: unidades, extremos e compatibilidade semântica
serão revisados antes da preparação.

Ficam fora dessa lista inicial IAG0005, IAG3001, IAG3002 e IAG3007 por excederem
20% de valores indisponíveis. Código IBGE é usado apenas para junção; município,
UF, natureza jurídica, nome/sigla do prestador, Capital e RM/RIDE são campos de
controle/contexto, não preditores nesta etapa. O CSV registra a aba de origem,
unidade, tipo, faixa observada e percentual indisponível por indicador. Valores
textuais que não puderam ser interpretados como numéricos são contabilizados
como indisponíveis; brancos de Capital/RM-RIDE não são tratados como nulos
numéricos, pois sua semântica precisa ser confirmada.

## 4. Variável-alvo

- **Nome/código:** IAG2013 — Perdas totais de água na distribuição.
- **Unidade:** percentual.
- **Definição operacional:** `[(GTA1001 + GTA1009 - GTA1207 - GTA1211 - GTA1203) / (GTA1001 + GTA1009)] × 100`.
- **Distribuição auditada:** 2023 tem 4.834 valores numéricos; 19 são negativos (mínimo observado: -60.117,39) e estão provisoriamente fora do pareamento por estarem fora da faixa percentual. 2024 tem 5.110 valores numéricos, todos entre 0 e 100%.
- **Por que não é trivial:** é um indicador calculado a partir de vários campos, não uma cópia de uma única coluna. O experimento será uma previsão de 2024 com atributos de 2023; não usar dados de 2024 como entrada.

As notas metodológicas das abas dos próprios arquivos confirmam a mesma fórmula
para IAG2013 nos dois anos. Porém, em 2023 também não se calcula o indicador
quando `GTA1203 > 5 × GTA1211`; a linha de IAG2013 em 2024 não apresenta essa
condição adicional. Portanto, **a igualdade da fórmula não comprova
comparabilidade plena da série**. A análise 2023→2024 fica delimitada como
exploratória, com uma única transição anual e possível diferença de população
elegível. Não interpretar o resultado como validação em anos futuros. Antes
de apresentar conclusões do modelo, o grupo deve levar essa ressalva ao
professor e, se os dados permitirem, comparar resultados sob critérios
alternativos de inclusão.

O filtro 0–100% é uma regra de plausibilidade para o percentual, não uma
correção dos registros. Em 2023 foram encontrados 19 valores negativos no
arquivo, dos quais 17 estão entre os códigos pareados; em 2024 os valores
numéricos observados ficaram entre 0 e 100%. Os casos fora de faixa não entram
na amostra preliminar, mas devem permanecer registrados como limitação e não
ser interpretados como erros corrigidos.

## 5. Qualidade e riscos

| Item verificado | Resultado | Ação |
| --------------- | --------- | ---- |
| Duplicatas | Nenhuma duplicata de código IBGE na aba-alvo de cada ano | Revalidar após combinar as abas de 2023 |
| Nulos / alvo não numérico | 407 de 5.241 em 2023; 34 de 5.144 em 2024. Entre preditores, IAG3002 tem 64,87% sem valor numérico | Excluir ausentes do pareamento do alvo; excluir IAG3002 inicialmente ou justificar uso |
| Valores fora de faixa | 19 valores negativos no alvo de 2023; nenhum fora de 0–100% em 2024 | Filtro de 0–100% provisório; investigar registros e comparar resultados com/sem esses casos |
| Extremos nos preditores | Há mínimos/máximos extremos em algumas colunas; faixas ainda não confrontadas indicador a indicador com as fórmulas oficiais | Investigar antes de transformar, limitar ou remover valores |
| Variáveis constantes | Nenhum dos 55 indicadores numéricos distintos ficou constante nos pares perfilados | Reavaliar após tratamento dos campos textuais e valores ausentes |
| Metadados repetidos | Cinco campos de contexto repetem-se nas quatro abas; Capital e RM/RIDE contêm muitos brancos | Deduplicar por código e confirmar se brancos indicam “não se aplica” |
| Inconsistência temporal | Uma transição observada (2023 → 2024); além da regra comum de numerador negativo, 2023 tem critério adicional `GTA1203 > 5 × GTA1211` | Análise exploratória; não alegar comparabilidade plena nem validação em anos futuros; reportar a diferença e avaliar sensibilidade antes das conclusões |
| Subnotificação / viés | Dados administrativos informados por prestadores; participação e cobertura podem variar | Descrever cobertura e ausência de informação; não interpretar como censo operacional completo |
| Dado pessoal identificável | Não foi identificado dado de pessoa natural nos campos municipais examinados; existem campos de município e prestador | Usar o recorte agregado; excluir identificadores de prestador dos preditores; reavaliar se novas fontes forem combinadas |

## 6. LGPD e reprodutibilidade

- **Dados pessoais:** nenhum dado de pessoa natural foi identificado nos campos examinados; códigos municipais e campos de identificação do prestador são mantidos apenas para conferência da fonte.
- **Estratégia:** manter o recorte agregado por município e excluir campos de identificação de preditores. Esta verificação não substitui revisão caso outras fontes sejam adicionadas.
- **Risco de reidentificação:** baixo nos indicadores agregados; reavaliar se outras fontes forem combinadas.
- **Base legal:** não se identificou tratamento de dado pessoal de pessoa natural no recorte atual; reavaliar se o escopo mudar.
- **Licença:** ver seção 1. A licença geral do site não foi presumida como licença dos arquivos de dados.
- **Hashes:** SHA-256 registrados na tabela da seção 1; recalcular se os arquivos forem substituídos por outra versão.
- **Verificação no Windows:** `Get-FileHash data/raw/<arquivo.xlsx> -Algorithm SHA256`
