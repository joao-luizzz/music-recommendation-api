# 🎵 Music Recommendation Engine & API (Neo4j + Django)

Este projeto é um sistema completo de recomendação de músicas que utiliza **Bancos de Dados Orientados a Grafos** para identificar padrões de consumo e sugerir novas faixas através de uma **API REST**.

---

## 🚀 Tecnologias Utilizadas
- **Neo4j AuraDB (Cloud):** Armazenamento e processamento de grafos.
- **Python 3.10+:** Linguagem core do projeto.
- **Django & Django REST Framework (DRF):** Camada de API e lógica de backend.
- **Cypher Query Language:** Consultas complexas em grafos.

---

## 🏗️ Arquitetura do Sistema
Diferente de sistemas baseados em SQL (relacionais), este motor utiliza a conexão direta entre nós para realizar recomendações em milissegundos, sem a necessidade de JOINS custosos.



### Modelagem do Grafo (Nodes & Edges):
- **User (id, nome):** Os ouvintes.
- **Song (titulo):** As faixas musicais.
- **Artist (nome):** Os criadores.
- **Relacionamentos:** `(:User)-[:OUVIU]->(:Song)`, `(:Song)-[:CANTA_POR]->(:Artist)`.

---

## 🧠 Algoritmo de Recomendação
A API utiliza **Filtragem Colaborativa**. A lógica identifica usuários com gostos similares ao usuário consultado e recomenda músicas que esses "vizinhos" curtem, mas que o usuário alvo ainda não ouviu.

```cypher
MATCH (eu:User {nome: $nome_usuario})-[:OUVIU|CURTIU]->(gosto_comum:Song)
MATCH (gosto_comum)<-[:OUVIU|CURTIU]-(vizinho:User)
WHERE vizinho.id <> eu.id
MATCH (vizinho)-[:OUVIU|CURTIU]->(recomendacao:Song)
WHERE NOT (eu)-[:OUVIU|CURTIU]->(recomendacao)
RETURN recomendacao.titulo AS Musica_Sugerida, count(vizinho) AS Forca_Recomendacao

## 🎨 Interface Visual (Spotify Clone)
Além da API JSON, o projeto conta com uma interface Front-end construída com **Django Templates** e **Tailwind CSS**.

Para acessar a vitrine visual de recomendações, acesse a rota do player passando o nome do usuário:
👉 `http://127.0.0.1:8000/api/player/João Luiz/`
👉 `http://127.0.0.1:8000/api/player/Ana/`