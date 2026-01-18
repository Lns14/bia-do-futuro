# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Para que serve no FinGuard? |
|---------|---------|---------------------|
| `perfil_investidor.json` | JSON | Personalizar as explicações sobre as dúvidas e necessidades de aprendizado do cliente. |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente e usar essas informações de forma didática. |

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

Planilha de gastos (data/planilha_gastos.csv):
nome,data,tipo_pagamento,categoria,valor
Aluguel,2025-09-15,Pix,Contas,R$800,00
Internet,2025-09-05,Cartão de débito,Contas,R$100,00
Uber,2025-09-30,Cartão de crédito,Transporte,R$200,00
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

```
