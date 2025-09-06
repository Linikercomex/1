import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys

# --- Configuração ---
caminho_planilha = 'ncm.csv'
nome_coluna_ncm = 'codigo_ncm'
nome_coluna_descricao = 'descricao_oficial'

# --- Carregamento e Treinamento do Modelo ---
try:
    ncm_df = pd.read_csv(caminho_planilha, sep=';')
except FileNotFoundError:
    print("Erro: Planilha não encontrada.")
    sys.exit()
except KeyError as e:
    print(f"Erro: Coluna {e} não encontrada. Verifique o cabeçalho.")
    sys.exit()

vectorizer = TfidfVectorizer()
ncm_matrix = vectorizer.fit_transform(ncm_df[nome_coluna_descricao])

# --- Função de Análise ---
def encontrar_ncm(descricao_usuario):
    descricao_limpa = descricao_usuario.lower()
    usuario_vetor = vectorizer.transform([descricao_limpa])
    similaridade = cosine_similarity(usuario_vetor, ncm_matrix)
    
    indices = similaridade.argsort()[0][::-1][:5]
    
    resultados = []
    for i in indices:
        resultados.append({
            'ncm': str(ncm_df.loc[i, nome_coluna_ncm]),
            'descricao': ncm_df.loc[i, nome_coluna_descricao],
            'similaridade': similaridade[0][i]
        })
    return resultados

# --- Execução de Exemplo ---
if __name__ == "__main__":
    descricao_teste = "aparelho de ar condicionado para veículo"
    resultados_finais = encontrar_ncm(descricao_teste)
    
    for r in resultados_finais:

        print(f"NCM: {r['ncm']} | Similaridade: {r['similaridade']:.2f} | Descrição: {r['descricao']}")

