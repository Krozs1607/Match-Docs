import streamlit as st
import pdfplumber
from pdf2image import convert_from_bytes  # Use convert_from_bytes
import pytesseract
from io import BytesIO
import openai

# Função para extrair texto usando OCR
def extrair_texto_pdf_com_ocr(uploaded_file):
    try:
        # Converte o arquivo PDF para bytes
        file_bytes = uploaded_file.read()
        
        # Converte o PDF em imagens usando pdf2image
        imagens = convert_from_bytes(file_bytes)  # Usando convert_from_bytes
        texto = ""
        
        for imagem in imagens:
            # Usando pytesseract para extrair o texto das imagens
            texto += pytesseract.image_to_string(imagem)
        
        return texto
    except Exception as e:
        return f"Erro ao tentar converter o PDF com OCR: {e}"

# Função para extrair texto diretamente do PDF (caso o texto seja acessível)
def extrair_texto_pdf_com_pdfplumber(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            texto = ""
            for pagina in pdf.pages:
                texto += pagina.extract_text()
            return texto
    except Exception as e:
        return f"Erro ao tentar extrair o texto do PDF com pdfplumber: {e}"

# Função principal
def main():
    st.title("Extração de Informações de Boletos")
    
    uploaded_file = st.file_uploader("Carregue um arquivo PDF", type=["pdf"])
    
    if uploaded_file is not None:
        st.write("Processando o PDF...")
        
        # Tente extrair o texto do PDF usando pdfplumber
        texto_extraido = extrair_texto_pdf_com_pdfplumber(uploaded_file)
        
        if not texto_extraido:
            # Caso pdfplumber não consiga, tente com OCR
            st.write("Não foi possível extrair texto com pdfplumber. Tentando OCR...")
            texto_extraido = extrair_texto_pdf_com_ocr(uploaded_file)
        
        # Exibe o texto extraído
        st.text_area("Texto extraído", texto_extraido, height=300)

        # Use o GPT para processar as informações extraídas
        if texto_extraido:
            info_extraida = extrair_info_com_gpt(texto_extraido)
            st.write("Informações extraídas:")
            st.write(info_extraida)

# Função para extrair informações específicas usando GPT
def extrair_info_com_gpt(texto_extraido):
    prompt = f"Extraia as informações de um boleto a partir deste texto: {texto_extraido}"
    openai.api_key = "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"

    # Chamada à API do OpenAI (substitua sua chave API aqui)
    response = openai.ChatCompletion.create(
        model="gpt-4",  # ou gpt-4 dependendo da sua chave
        messages=[{"role": "system", "content": "Você é um assistente de extração de dados de boletos."},
                  {"role": "user", "content": prompt}],
    )

    resposta_dict = response['choices'][0]['message']['content'].strip()
    return resposta_dict

# Rodando a aplicação Streamlit
if __name__ == "__main__":
    main()
