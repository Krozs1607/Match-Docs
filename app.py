import streamlit as st
import pandas as pd
import openai
import os

def generate_combinations_with_openai(prompt):
    """Usa a API da OpenAI para gerar combinações de lanches."""
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em criar sugestões de combinações de lanches com base em um limite calórico."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Erro ao gerar combinações: {e}"

def main():
    # Configurar a API Key da OpenAI
    openai.api_key = os.getenv("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")

    st.title("Sugestão de Lanches Fast-Food por OpenAI")

    st.write("Insira a quantidade de calorias que você pode consumir diariamente e veja as sugestões de combos que se encaixam no seu limite calórico para o lanche da tarde!")

    # Upload da tabela de lanches
    uploaded_file = st.file_uploader("Faça o upload da tabela de lanches (CSV com colunas 'Loja', 'Nome' e 'Calorias')", type="csv")

    if uploaded_file:
        # Carregar tabela de lanches
        lanches_df = pd.read_csv(uploaded_file)

        # Exibir a tabela carregada
        st.write("Tabela de Lanches:")
        st.dataframe(lanches_df)

        # Entrada: calorias diárias
        daily_calories = st.number_input("Digite a quantidade de calorias que você pode consumir por dia:", min_value=1, step=1)

        if daily_calories > 0:
            # Calcular 35% das calorias diárias
            snack_calories_limit = 0.35 * daily_calories
            st.write(f"Você pode consumir até **{snack_calories_limit:.2f} kcal** no lanche da tarde.")

            # Criar prompt para a OpenAI
            prompt = (
                "Com base na seguinte tabela de lanches com loja, nome e calorias: \n"
                f"{lanches_df.to_string(index=False)} \n"
                f"Sugira combinações de lanches que somem no máximo {snack_calories_limit:.2f} calorias. Indique o nome do combo, a loja e o total de calorias."
            )

            # Obter combinações da OpenAI
            combinations = generate_combinations_with_openai(prompt)

            st.write("## Combinações sugeridas pela OpenAI:")
            st.text(combinations)

if __name__ == "__main__":
    main()
