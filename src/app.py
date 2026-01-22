import pandas as pd
import requests
import streamlit as st
import json

URL = "http://localhost:11434/api/generate"
MODELO = "qwen2.5:3b"

# Acesso aos dados do usuário
transacoes = pd.read_csv(r"C:\Users\livia\OneDrive\Documentos\FinGuard\data\transacoes.csv")
with open(r"C:\Users\livia\OneDrive\Documentos\FinGuard\data\perfil_investidor.json", 'r', encoding='utf-8') as f:
    perfil = json.loads(f.read())
with open(r"C:\Users\livia\OneDrive\Documentos\FinGuard\data\limites.json", 'r', encoding='utf-8') as f:
    limites = json.loads(f.read())

# Contexto para ser usado no prompt
contexto = f"""
Perfil do investidor:
{json.dumps(perfil, indent=2)}
"""

# Função que consolida os gastos e verifica os limites
def calcular_todos_limites(transacoes, limites):
    receita = limites.get("receita_mensal", 0)
    resultados = []

    # Converte a coluna de datas
    transacoes["data"] = pd.to_datetime(transacoes["data"])
    transacoes["mes"] = transacoes["data"].dt.to_period("M").astype(str)


    for item in limites.get("limites", []):
        categoria = item.get("categoria")
        regra = item.get("regra", {})

        # Agrupa por mês e soma os gastos por categoria
        gastos_categoria = (
            transacoes
                .groupby(["mes", "descricao", "categoria"])["valor"]
                .sum()
                .reset_index()
        )


        for _, row in gastos_categoria.iterrows():
            mes = row["mes"]
            total_gasto = row["valor"]
            descrição = row["descricao"]
            if row["categoria"] == categoria:
                tipo = regra.get("tipo")
                valor_regra = regra.get("valor", 0)
                if tipo == "percentual_da_receita":
                    valor_limite = receita * valor_regra
                else:
                    valor_limite = None
                resultados.append({
                    "mes": mes,
                    "categoria": categoria,
                    "descrição": descrição,
                    "tipo_limite": tipo,
                    "limite_definido": valor_regra,
                    "limite_em_reais": round(valor_limite, 2) if valor_limite is not None else None,
                    "total_gasto": round(total_gasto, 2),
                    "ultrapassou": bool(valor_limite is not None and total_gasto > valor_limite)
                })
            else:
                resultados.append({
                    "mes": mes,
                    "categoria": row["categoria"],
                    "descrição": descrição,
                    "tipo_limite": None,
                    "limite_definido": "Sem limite definido",
                    "limite_em_reais": "Sem limite definido",
                    "total_gasto": round(total_gasto, 2),
                    "ultrapassou": False
                })

    return resultados


resultado_limites = calcular_todos_limites(transacoes, limites)

# Gera um resumo dos limites para que o agente tire conclusões
def gerar_resumo_limites(resultado_limites):
    resumo = []

    for item in resultado_limites:
        if item["ultrapassou"]:
            status = "ULTRAPASSOU O LIMITE"
        elif item["limite_em_reais"] == "Sem limite definido" and item["ultrapassou"] == False:
            status = "SEM LIMITE DEFINIDO"
        else:
            status = "DENTRO DO LIMITE"

        resumo.append({
            "mes": item["mes"],
            "categoria": item["categoria"],
            "descrição": item["descrição"],
            "total_gasto": item["total_gasto"],
            "limite_em_reais": item["limite_em_reais"],
            "status": status
        })

    return resumo

resumo_limites = gerar_resumo_limites(resultado_limites)

# System prompt
system_prompt = f"""
Você é o FinGuard, um assistente financeiro pessoal consultivo, amigável e didático.

Seu papel é ajudar o cliente a entender seus gastos, acompanhar limites e tomar decisões financeiras mais conscientes, exclusivamente com base nos dados fornecidos.

OBJETIVO

Ajudar o cliente a:

- compreender como seu dinheiro está sendo usado
- visualizar padrões simples de gastos
- refletir sobre possíveis ajustes, sem impor decisões

ESCOPO E LIMITAÇÕES (OBRIGATÓRIO)

- Nunca julgue os gastos do cliente.
- Não faça suposições além dos dados fornecidos.
- Não realize cálculos financeiros nem recalculagens.
- Utilize apenas os dados presentes no contexto, mas sempre dê sugestão ou pergunte se o usuário precisa de mais ajuda.
- Não estime valores, médias ou projeções.
- Quando faltar informação, responda exatamente:
  “Não tenho essa informação nos dados, desculpe.”

DADOS JÁ CALCULADOS
- Nunca refaça contas.

COMPORTAMENTO CONSULTIVO (OBRIGATÓRIO)

Ao responder:

- Identifique claramente o tema da pergunta.
- Traga os dados exatos que respondem à dúvida.
- Explique o que esses dados mostram, de forma simples.
- Se possível, destaque um padrão ou ponto de atenção, somente se já estiver explícito nos dados.
- Sugira uma ação prática opcional, alinhada ao perfil do investidor:

  use expressões como:

  - “se fizer sentido para você”
  - “caso queira acompanhar melhor”
  - “uma opção seria”

FINALIZE SEMPRE:

- CONFIRMANDO SE O CLIENTE ENTENDEU
- OFERECENDO AJUDA ADICIONAL OU UMA PRÓXIMA PERGUNTA POSSÍVEL

RESTRIÇÕES DE SEGURANÇA

- Nunca exponha dados sensíveis.
- Nunca fale sobre outros clientes.
- Se solicitado, responda apenas:
  “Não tenho acesso a senhas e não posso compartilhar informações de outros clientes.”

Perguntas fora de finanças pessoais:
“Meu papel é te ajudar a entender e controlar suas finanças. Posso te apoiar nisso 😊”

LINGUAGEM E TOM

- Clara e acessível
- Sem termos técnicos desnecessários
- Sem julgamentos
- Tom acolhedor, educativo e respeitoso

Evite respostas de uma única frase e sempre busque agregar valor com explicações e sugestões práticas.
"""

# Função para integrar com o ollama
def perguntar(msg):
    prompt = f"""
    INSTRUÇÕES FIXAS (OBRIGATÓRIO SEGUIR):
      {system_prompt}

    PERFIL DO USUÁRIO:
    {contexto}

    RESUMO FINANCEIRO CONSOLIDADO (VERDADE FINAL):
    Os status abaixo já estão definidos.
    Nunca interprete valores.
    Nunca contradiga o status informado.
    
    {json.dumps(resumo_limites, indent=2, ensure_ascii=False)}
      
    PERGUNTA DO CLIENTE:
    {msg}"""

    response =requests.post(URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return response.json()["response"]

# Interface
st.title("💸 FinGuard - Seu Assistente Financeiro Pessoal")
pergunta = st.chat_input("Sua dúvida sobre suas finanças:")
if pergunta:
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").text(perguntar(pergunta))
