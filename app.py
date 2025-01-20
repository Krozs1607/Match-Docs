import streamlit as st
import openai
import os
from docx import Document
def generate_combinations_with_openai(prompt):
    """Usa a API da OpenAI para gerar combinações de lanches."""
    try:
        resposta = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em criar sugestões de combinações de lanches com base em um limite calórico, nunca repita combinações de lanche, e preze por passar sugestões que sejam da mesma loja."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        resposta_dict = resposta.model_dump()
        return resposta_dict['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Erro ao gerar combinações: {e}"

def read_word_file(file):
    """Lê o conteúdo de um arquivo Word e retorna como string."""
    doc = Document(file)
    content = []
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            content.append(paragraph.text.strip())
    return "\n".join(content)

def calculate_daily_calories(weight, height, age, sex, workout_hours, goal):
    """Calcula a necessidade calórica diária."""
    if sex == "Masculino":
        bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
    else:
        bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)
    
    # Ajustar com base na atividade física
    if workout_hours == 0:
        activity_factor = 1.2
    elif workout_hours <= 1:
        activity_factor = 1.375
    elif workout_hours <= 3:
        activity_factor = 1.55
    elif workout_hours <= 5:
        activity_factor = 1.725
    else:
        activity_factor = 1.9

    calories = bmr * activity_factor

    # Ajuste com base no objetivo
    if goal == "Emagrecer":
        calories *= 0.85  # Déficit calórico
    elif goal == "Ganhar massa":
        calories *= 1.15  # Superávit calórico

    return calories

def main():
    # Configurar a API Key da OpenAI
    openai.api_key = "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"

    # Customizar o estilo
    st.markdown(
        """
        <style>
            body {
                background-color: #F6F6F6;
                color: #3A3A3A;
                font-family: Arial, sans-serif;
            }
            .stButton>button {
                background-color: #6AB04C;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
            }
            .stButton>button:hover {
                background-color: #45A049;
            }
        </style>
        """, unsafe_allow_html=True
    )

    st.title("🍏 Sugestão de Lanches Nutritivos por OpenAI")

    st.write("Descubra combinações de lanches com base no seu perfil nutricional e objetivo!")

    # Entradas do usuário
    weight = st.number_input("Seu peso (kg):", min_value=1.0, step=0.1)
    height = st.number_input("Sua altura (cm):", min_value=100.0, step=0.1)
    age = st.number_input("Sua idade:", min_value=1, step=1)
    sex = st.selectbox("Sexo:", ["Masculino", "Feminino"])
    workout_hours = st.slider("Quantas horas por semana você faz academia?", min_value=0, max_value=10, step=1)
    goal = st.selectbox("Qual é o seu objetivo?", ["Emagrecer", "Ganhar massa", "Manter peso"])

    if st.button("Calcular necessidade calórica e sugerir lanches"):
        if weight > 0 and height > 0 and age > 0:
            daily_calories = calculate_daily_calories(weight, height, age, sex, workout_hours, goal)
            snack_calories_limit = 0.3 * daily_calories

            st.write(f"🎯 Sua necessidade calórica diária estimada é **{daily_calories:.2f} kcal**.")
            st.write(f"🍔 Você pode consumir até **{snack_calories_limit:.2f} kcal** no lanche da tarde.")

            # Ler o arquivo Word diretamente do código
            word_file_path = "kcals.docx"  # Certifique-se de ter o arquivo no diretório correto

            try:
                word_content = read_word_file(word_file_path)

                # Criar prompt para a OpenAI
                prompt = (
                    "Com base na seguinte tabela de lanches extraída do documento: \n"
                    f"{word_content} \n"
                    f"Sugira combinações de lanches que somem no máximo {snack_calories_limit:.2f} calorias. "
                    "Garanta que os produtos sugeridos sejam da mesma loja e sem repetições. Indique o nome do combo, a loja e o total de calorias."
                )

                # Obter combinações da OpenAI
                combinations = generate_combinations_with_openai(prompt)

                st.write("## 🍽️ Combinações sugeridas pela OpenAI:")
                st.text(combinations)

            except FileNotFoundError:
                st.error("O arquivo 'kcals.docx' não foi encontrado. Certifique-se de que ele está no mesmo diretório do código.")

if __name__ == "__main__":
    main()
