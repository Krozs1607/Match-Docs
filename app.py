import openai
import streamlit as st

# Configure sua API Key
openai.api_key = "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"


def extrair_info_com_gpt(texto):
    prompt = f"""
    Extraia as seguintes informações de um boleto:
    - Nome do Beneficiário
    - Data de Vencimento
    - Valor Total
    
    Texto do boleto:
    {texto}
    """
    response = openai.chat.completions.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    resposta_dict = resposta.model_dump()
    return resposta_dict['choices'][0].text.strip()

st.title("Leitor de Boletos com GPT")
uploaded_file = st.file_uploader("Faça upload do boleto (PDF ou imagem)", type=["pdf", "png", "jpg"])

if uploaded_file:
    # Simule um OCR para extrair texto (ou use o texto extraído diretamente se o boleto tiver texto acessível)
    texto_extraido = "Texto simulado do boleto: Nome do Beneficiário: João Silva, Data de Vencimento: 10/12/2024, Valor: R$ 150,00"
    
    # Use o GPT para extrair informações
    info_extraida = extrair_info_com_gpt(texto_extraido)
    st.text("Informações Extraídas:")
    st.write(info_extraida)
