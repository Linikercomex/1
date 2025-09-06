import streamlit as st
import pandas as pd
from analisador_ncm import encontrar_ncm

# --- Configuração da Página ---
st.set_page_config(page_title="NCM Master - Liniker.comex", layout="wide")
st.title("🔎 Analisador de NCM, fácil e rápido.")
st.subheader("Encontre a classificação fiscal de um produto.")

# --- Entrada do Usuário ---
st.markdown("---")
descricao_produto = st.text_input("Digite a descrição do 'produto' e clique em Analisar NCM:", help="Ex: 'cavalos'")

# --- Lógica de Exibição ---
if st.button("Analisar NCM"):
    if descricao_produto:
        with st.spinner("Analisando..."):
            resultados = encontrar_ncm(descricao_produto)

        st.success("Análise concluída!")
        st.write("### NCMs Mais Prováveis")

        # Formata os resultados para uma tabela amigável
        df_resultados = pd.DataFrame(resultados)

        # Adiciona uma coluna de Similaridade formatada em porcentagem
        df_resultados['similaridade'] = df_resultados['similaridade'].apply(lambda x: f"{x:.2%}")

        # Renomeia as colunas para uma apresentação mais clara
        df_resultados.rename(columns={
            'ncm': 'NCM',
            'descricao': 'Descrição Oficial',
            'similaridade': 'Similaridade'
        }, inplace=True)

        st.table(df_resultados)

    else:
        st.warning("Por favor, digite a descrição de um produto para iniciar a análise.")

# --- Rodapé ---
st.markdown("---")

st.markdown("Projeto desenvolvido por **@Liniker.comex** para simulação, para casos reais contactar um despachante aduaneiro.")
