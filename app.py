import streamlit as st
import pdfplumber
import openai

# Configure sua chave de API do OpenAI
openai.api_key = "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"

def extrair_texto_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        texto = ""
        for pagina in pdf.pages:
            texto += pagina.extract_text()
    return texto

def extrair_info_com_gpt(texto):
    # Chama a API OpenAI para extrair as informações do texto
    resposta = openai.chat.completions.create(
        model="gpt-4",  # ou gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "Você é um assistente que ajuda a extrair informações de boletos."},
            {"role": "user", "content": f"Extraia as informações do seguinte texto: {texto}"}
        ],
        max_tokens=500,
        temperature=0
    )

    # Usando model_dump() para acessar os dados da resposta
    resposta_dict = resposta.model_dump()
    
    # Retorna o conteúdo extraído
    return resposta_dict['choices'][0]['message']['content'].strip()

# Função Streamlit para o site
def main():
    st.title("Extrator de Informações de Boleto")
    
    # Carregar o arquivo PDF do boleto
    uploaded_file = st.file_uploader("Carregue seu boleto em PDF", type=["pdf"])
    
    if uploaded_file is not None:
        # Extração do texto do PDF
        texto_pdf = extrair_texto_pdf(uploaded_file)
        if texto_pdf:
            st.write("Texto extraído do boleto:")
            st.text_area("Texto extraído", texto_pdf, height=300)
            
            # Processar o texto extraído com o GPT
            info_extraida = extrair_info_com_gpt(texto_pdf)
            
            st.subheader("Informações Extraídas:")
            st.write(info_extraida)
        else:
            st.error("Não foi possível extrair texto do PDF.")
            
if __name__ == "__main__":
    main()
