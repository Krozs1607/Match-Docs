import streamlit as st
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import openai

# Configure sua chave de API do OpenAI
openai.api_key = "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"

# Função para extrair texto de um PDF com OCR (para PDFs escaneados)
def extrair_texto_pdf_com_ocr(pdf_file):
    imagens = convert_from_path(pdf_file)  # Converte as páginas para imagens
    texto = ""
    for imagem in imagens:
        texto += pytesseract.image_to_string(imagem)  # Extrai o texto da imagem usando OCR
    return texto

# Função para extrair texto do PDF com pdfplumber (para PDFs com texto acessível)
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
        # Tente extrair texto com pdfplumber
        texto_pdf = extrair_texto_pdf(uploaded_file)
        
        # Se não conseguiu extrair texto, tente com OCR
        if not texto_pdf.strip():
            st.warning("Não foi possível extrair texto com pdfplumber. Tentando OCR...")
            texto_pdf = extrair_texto_pdf_com_ocr(uploaded_file)

        if texto_pdf.strip():
            st.write("Texto extraído do boleto:")
            st.text_area("Texto extraído", texto_pdf, height=300)
            
            # Processar o texto extraído com o GPT
            info_extraida = extrair_info_com_gpt(texto_pdf)
            
            st.subheader("Informações Extraídas:")
            st.write(info_extraida)
        else:
            st.error("Não foi possível extrair texto do PDF, nem com OCR.")
            
if __name__ == "__main__":
    main()
