import openai

# Configure sua API Key
openai.api_key = "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"

def extrair_info_com_gpt(texto):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # ou gpt-3.5-turbo, dependendo da sua necessidade
        messages=[
            {"role": "system", "content": "Você é um assistente que ajuda a extrair informações de boletos."},
            {"role": "user", "content": f"Extraia as informações do seguinte texto: {texto}"}
        ],
        max_tokens=200,
        temperature=0
    )
    return response['choices'][0]['message']['content']

# Simule um texto para teste
texto_simulado = "Nome do Beneficiário: João Silva, Data de Vencimento: 10/12/2024, Valor: R$ 150,00"
info_extraida = extrair_info_com_gpt(texto_simulado)
print(info_extraida)
