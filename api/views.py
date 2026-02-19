import os
from django.shortcuts import render 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Carrega as senhas do .env
load_dotenv()

class RecomendacaoMusicaView(APIView):
    def get(self, request, nome_usuario):
        nome_usuario = nome_usuario.title() 
        URI = os.getenv("NEO4J_URI")
        USUARIO = "neo4j"
        SENHA = os.getenv("NEO4J_PASSWORD")

        # CORRIGIDO: Ordem correta do MATCH e WHERE
        QUERY_RECOMENDACAO = """
        MATCH (eu:User {nome: $nome_usuario})-[:OUVIU|CURTIU]->(gosto_comum:Song)
        MATCH (gosto_comum)<-[:OUVIU|CURTIU]-(vizinho:User)
        WHERE vizinho.id <> eu.id
        MATCH (vizinho)-[:OUVIU|CURTIU]->(recomendacao:Song)
        WHERE NOT (eu)-[:OUVIU|CURTIU]->(recomendacao)
        RETURN recomendacao.titulo AS Musica_Sugerida, 
               count(vizinho) AS Forca_Recomendacao, 
               recomendacao.capa_url AS Capa
        ORDER BY Forca_Recomendacao DESC
        """

        try:
            driver = GraphDatabase.driver(URI, auth=(USUARIO, SENHA))
            with driver.session() as session:
                resultados = session.run(QUERY_RECOMENDACAO, nome_usuario=nome_usuario)
                
                recomendacoes = []
                for registro in resultados:
                    recomendacoes.append({
                        "musica": registro["Musica_Sugerida"],
                        "relevancia": registro["Forca_Recomendacao"],
                        "capa_url": registro["Capa"]
                    })
                    
            driver.close()

            return Response({
                "usuario_consultado": nome_usuario,
                "total_recomendacoes": len(recomendacoes),
                "recomendacoes": recomendacoes
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"erro_na_conexao": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Função do Player Visual
def home_spotify(request):
    URI = os.getenv("NEO4J_URI")
    USUARIO = "neo4j"
    SENHA = os.getenv("NEO4J_PASSWORD")
    nome_alvo = "João Luiz" 

    QUERY = """
    MATCH (eu:User {nome: $nome})-[:OUVIU|CURTIU]->(gosto_comum:Song)
    MATCH (gosto_comum)<-[:OUVIU|CURTIU]-(vizinho:User)
    WHERE vizinho.id <> eu.id
    MATCH (vizinho)-[:OUVIU|CURTIU]->(recomendacao:Song)
    WHERE NOT (eu)-[:OUVIU|CURTIU]->(recomendacao)
    RETURN recomendacao.titulo AS Musica, 
           count(vizinho) AS Forca, 
           recomendacao.capa_url AS Capa
    ORDER BY Forca DESC
    """

    try:
        driver = GraphDatabase.driver(URI, auth=(USUARIO, SENHA))
        with driver.session() as session:
            resultados = session.run(QUERY, nome=nome_alvo)
            
            lista_final = []
            for registro in resultados:
                lista_final.append({
                    "musica": registro["Musica"],
                    "relevancia": registro["Forca"],
                    # Fallback visual caso não tenha capa no banco
                    "capa_url": registro["Capa"] if registro["Capa"] else "https://via.placeholder.com/300/1DB954/FFFFFF?text=Sem+Capa"
                })
        driver.close()

        contexto = {
            'dados': {
                'usuario_consultado': nome_alvo,
                'total_recomendacoes': len(lista_final),
                'recomendacoes': lista_final
            }
        }
        return render(request, 'api/index.html', contexto)

    except Exception as e:
        return render(request, 'api/index.html', {'dados': {'erro': str(e)}})