# G02 — Previsão de perdas de água em municípios brasileiros

> Projeto AV2 de Machine Learning · FACAPE 2026.2  
> Pasta: `grupos/grupo-02-perdas-agua-ods6` · E2: auditoria inicial concluída, com ressalvas

## Integrantes

| Nome | Matrícula | Papel |
| ---- | --------- | ----- |
| Alan Herculino Siqueira | 25782 | A definir pelo grupo |
| Davi Cordeiro Gomes | 25794 | A definir pelo grupo |
| Henderson Silva | 25883 | A definir pelo grupo |
| Bruno Barros da Silva | 25932 | A definir pelo grupo |

## 1. ODS, meta e problema

- **ODS:** 6 — Água potável e saneamento.
- **Meta:** 6.4 — aumentar a eficiência do uso da água e contribuir para o
  enfrentamento da escassez hídrica.
- **Tema:** previsão de perdas de água em redes de distribuição de municípios
  brasileiros por meio de Machine Learning.
- **Problema:** avaliar se indicadores municipais de um ano permitem prever o
  percentual de perdas de água no ano seguinte, sujeito à compatibilidade
  metodológica da série histórica.
- **Público/beneficiário:** equipes responsáveis pelo abastecimento e gestores
  municipais de saneamento.

## 2. Decisão

> “Se o modelo indicar uma previsão de perdas de água acima de um limite
> previamente definido, a equipe responsável pelo abastecimento poderá priorizar
> uma avaliação técnica do sistema em até 30 dias.”

- **Custo do falso positivo:** priorizar avaliação de um sistema que não esteja
  entre os de maior perda, utilizando recursos que poderiam ser direcionados a
  outro local.
- **Custo do falso negativo:** atrasar a avaliação de um sistema com perdas
  elevadas.
- **Métrica principal:** MAE, em pontos percentuais se compatível com a unidade
  oficial do alvo. A acurácia não se aplica à regressão.
- A previsão é apoio à triagem, não diagnóstico nem decisão automática. O
  limite de alerta será definido após auditar o alvo e discutir o critério de
  priorização.

## 3. Dados e licença

- **Fonte:** SINISA — módulo Abastecimento de Água, Bases Municipais com anos
  de referência 2023 e 2024.
- **Instituição:** Ministério das Cidades.
- **Portal de referência 2023:** https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa/resultados-sinisa
- **Portal de referência 2024:** https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa/resultados-sinisa/resultados-sinisa-2025
- **Produtos de água:** [planilhas SINISA referência 2023](https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa/arquivos/SINISA_Resultados_Ref2023.zip) e [planilhas SINISA referência 2024](https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa/resultados-sinisa/SINISA_Resultados_Ref2024.zip).
- **Consulta das páginas:** 2026-11-25; reconferência das fontes oficiais em 2026-11-26. A data original de download dos arquivos ainda precisa ser confirmada pelo grupo.
- **Licença/termos de uso:** o rodapé do portal declara CC BY-ND 3.0 para o conteúdo do site ([licença](https://creativecommons.org/licenses/by-nd/3.0/)); não foi localizada licença específica das planilhas nem confirmação de que a declaração geral se aplique a elas. O grupo não redistribuirá os arquivos originais ou bases derivadas enquanto isso não for esclarecido. Detalhes e limitações no dicionário de dados.
- **Volume observado:** 5.241 municípios na aba-alvo de 2023 e 5.144 em 2024; 4.574 pares preliminares com IAG2013 numérico e entre 0–100% nos dois anos. A base de 2023 tem 55 indicadores distintos, atendendo ao critério alternativo de pelo menos 40 atributos; a amostra pareada fica abaixo de 5.000 registros.
- **Alvo:** IAG2013 — Perdas totais de água na distribuição, em percentual. A fórmula, cobertura e limitações metodológicas estão registradas no dicionário de dados.
- **Dados pessoais:** não identificamos campos de pessoa natural nas planilhas
  municipais de indicadores examinadas. Campos de identificação do município
  e do prestador não serão usados como preditores.
- Detalhes da auditoria estão registrados em
  [`docs/dicionario-de-dados.md`](docs/dicionario-de-dados.md).
- O perfil inicial das variáveis de 2023 está em
  [`reports/tables/perfil-preditores-ref2023.csv`](reports/tables/perfil-preditores-ref2023.csv).

## 4. Como reproduzir

O pipeline e o ambiente reprodutível serão concluídos em etapas posteriores.
Após a implementação, as instruções serão:

```bash
python3 -m venv .venv
python -m pip install -r requirements.txt
python -m src.pipeline --config configs/base.yaml
```

O comando Docker será documentado e validado na E6. O pipeline ainda não foi
implementado nem executado; portanto, tempo de execução e saídas ainda não
estão disponíveis.

## 5. Resultados principais

Ainda não há resultados de modelos. A avaliação planejada é de regressão, com
MAE como métrica principal e comparação com uma referência que repete a perda
observada no ano anterior. O par 2023→2024 será tratado como exploratório:
embora a fórmula do alvo seja a mesma, as notas metodológicas têm critérios de
não cálculo diferentes. Não se afirma comparabilidade plena nem generalização
para outros anos; a ressalva está detalhada no dicionário de dados.

## 6. Limitações iniciais

- A cobertura municipal, os anos disponíveis e a comparabilidade metodológica
  limitam a interpretação: há apenas uma transição anual e uma diferença nos
  critérios de não cálculo do alvo entre as referências.
- Indicadores agregados não descrevem necessariamente as condições de cada
  trecho da rede nem identificam a causa das perdas.
- Uma previsão não substitui inspeção, medição local ou avaliação por
  profissionais responsáveis.
- A licença específica das planilhas não foi localizada; não redistribuir os
  arquivos ou assumir que a licença geral do site se aplica a eles.

## 7. Uso responsável

- **Não usar para:** decisão automática, penalização de municípios ou
  prestadores, nem como diagnóstico definitivo da rede.
- **Dados pessoais:** a auditoria inicial não identificou dados de pessoa
  natural nas planilhas municipais; reavaliar se outras fontes forem usadas.
- **Desempenho por subgrupo:** será avaliado após identificar cobertura
  suficiente, por exemplo, entre regiões e períodos; não há resultados nesta
  etapa.
- **Uso de IA generativa:** assistente de IA foi usado como apoio para organizar
  e redigir os documentos iniciais. O grupo deve revisar as decisões e validar
  todas as informações sobre dados e metodologia.

## Estrutura desta pasta

```text
grupo-02-perdas-agua-ods6/
├── README.md
├── configs/base.yaml
├── data/raw/                 # não versionar os dados brutos
├── src/                      # carregamento, preparação, modelos e avaliação
├── notebooks/                # EDA e experimentos
├── experiments/runs.csv
├── reports/                  # tabelas e figuras geradas
├── article/                  # artigo IMRaD
├── slides/                   # apresentação
└── docs/
    ├── proposta.md
    ├── dicionario-de-dados.md
    └── decisoes-tecnicas.md
```
