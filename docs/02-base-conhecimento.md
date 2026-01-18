# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Para que serve no FinGuard? |
|---------|---------|---------------------|
| `perfil_investidor.json` | JSON | Personalizar as explicações sobre as dúvidas e necessidades de aprendizado do cliente. |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente e usar essas informações de forma didática. |
| `limites.json` | JSON | Contém os limites de gastos definidos pelo cliente por categoria ou tipo de despesa. Esses dados são utilizados para monitorar a proximidade ou o ultrapassamento dos limites estabelecidos. O agente analisa o padrão de gastos do cliente para gerar alertas preventivos e explica, de forma didática, como o estouro do limite pode impactar o planejamento financeiro. |

---

## Estratégia de Integração

### Como os dados são carregados?

Arquivos carregados via código.

```

### Como os dados são usados no prompt?

Para simplificar, podemos simplesmente "injetar" os dados em nosso prompt, garantindo que o Agente tenha o melhor contexto possível.

```text
TRANSACOES DO CLIENTE (data/transacoes.csv):
data,descricao,categoria,valor,tipo
2025-10-01,Salário,receita,5000.00,entrada
2025-10-02,Aluguel,moradia,1200.00,saida
2025-10-03,Supermercado,alimentacao,450.00,saida
2025-10-05,Netflix,lazer,55.90,saida
2025-10-07,Farmácia,saude,89.00,saida
2025-10-10,Restaurante,alimentacao,120.00,saida
2025-10-12,Uber,transporte,45.00,saida
2025-10-15,Conta de Luz,moradia,180.00,saida
2025-10-20,Academia,saude,99.00,saida
2025-10-25,Combustível,transporte,250.00,saida

Limites de gastos (data/limites.json):
[
  {
    "alerta": "Gastos com transporte (Uber, 99, etc)",
    "limite": "10% da receita mensal",
    "data_limite": "até dia 20 de cada mês"
  },
  {
    "alerta": "Gastos com alimentação fora de casa",
    "limite": "15% da receita mensal",
    "data_limite": "até dia 25 de cada mês"
  },
  {
    "alerta": "Gastos com lazer",
    "limite": "8% da receita mensal",
    "data_limite": "até dia 28 de cada mês"
  },
  {
    "alerta": "Gastos no cartão de crédito",
    "limite": "30% da receita mensal",
    "data_limite": "até o fechamento da fatura"
  }
]

```

---

## Exemplo de Contexto Montado

O exemplo de contexto montado abaixo, se baiseia nos dados originais da base de conhecimento, mas os sintetiza deixando apenas as informações mais relevantes, otimizando assim o consumo de tokens. 

```
RESUMO DE GASTOS:
- Moradia: R$ 800
- Alimentação: R$ 570
- Transporte: R$ 200
- Saúde: R$ 180
- Lazer: R$ 55,90
- Total de saídas: R$ 2.488,90

RESUMO DE LIMITES DEFINIDOS PELO CLIENTE:

- Transporte: limite de 10% da receita mensal, com data de referência até o dia 20 de cada mês
- Alimentação fora de casa: limite de 15% da receita mensal, com data de referência até o dia 25 de cada mês
- Lazer: limite de 8% da receita mensal, com data de referência até o dia 28 de cada mês
- Cartão de crédito: limite de 30% da receita mensal, considerando o fechamento da fatura

```
