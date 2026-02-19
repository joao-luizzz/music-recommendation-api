import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# 1. Carrega as variáveis escondidas no arquivo .env
load_dotenv()

# 2. Configurações de Conexão
URI = os.getenv("NEO4J_URI")
USUARIO = "neo4j"
SENHA = os.getenv("NEO4J_PASSWORD")

# 3. A Query de Filtragem Colaborativa
QUERY_RECOMENDACAO = """
MATCH (eu:User {nome: $nome_usuario})-[:OUVIU|CURTIU]->(gosto_comum:Song)
MATCH (gosto_comum)<-[:OUVIU|CURTIU]-(vizinho:User)
WHERE vizinho.id <> eu.id
MATCH (vizinho)-[:OUVIU|CURTIU]->(recomendacao:Song)
WHERE NOT (eu)-[:OUVIU|CURTIU]->(recomendacao)
RETURN recomendacao.titulo AS Musica_Sugerida, count(vizinho) AS Forca_Recomendacao
ORDER BY Forca_Recomendacao DESC
"""

def buscar_recomendacoes(nome_usuario):
    # Inicializa o driver de conexão
    try:
        driver = GraphDatabase.driver(URI, auth=(USUARIO, SENHA))
    except Exception as e:
        print(f"Erro ao conectar no Neo4j: {e}")
        return []

    # Abre a sessão e roda a query
    with driver.session() as session:
        print(f"Buscando recomendações para: {nome_usuario}...\n")
        resultados = session.run(QUERY_RECOMENDACAO, nome_usuario=nome_usuario)
        
        recomendacoes = []
        for registro in resultados:
            recomendacoes.append({
                "musica": registro["Musica_Sugerida"],
                "forca": registro["Forca_Recomendacao"]
            })
            
    driver.close()
    return recomendacoes

# 4. Executando o script
if __name__ == "__main__":
    # Usando o usuário que criamos lá no seu script Cypher
    meu_nome = "João Luiz" 
    
    minhas_recomendacoes = buscar_recomendacoes(meu_nome)
    
    if minhas_recomendacoes:
        print("🎧 Aqui estão suas recomendações baseadas no que pessoas parecidas ouvem:")
        for item in minhas_recomendacoes:
            print(f"- {item['musica']} (Relevância: {item['forca']})")
    else:
        print("Ainda não temos dados suficientes para te recomendar algo novo.")