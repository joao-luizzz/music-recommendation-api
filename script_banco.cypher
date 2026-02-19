// ============================================================================
// SCRIPT DE INICIALIZAÇÃO E POVOAMENTO DO BANCO DE DADOS NEO4J
// Projeto: Sistema de Recomendação de Músicas (DIO)
// Autor: João Luiz
// ============================================================================

// 1. Limpeza inicial do banco para evitar duplicatas em testes (CUIDADO: apaga tudo)
MATCH (n) DETACH DELETE n;

// 2. Criação de Constraints (Regras de Integridade e Performance)
CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (s:Song) REQUIRE s.titulo IS UNIQUE;

// ============================================================================
// CRIAÇÃO DOS NÓS (Entidades)
// ============================================================================

// 3. Criar Usuários
MERGE (eu:User {id: 'u1', nome: 'João Luiz', idade: 20, perfil: 'Pop/Eletrônica'});
MERGE (ana:User {id: 'u2', nome: 'Ana', idade: 22, perfil: 'Rocker/Eclética'});
MERGE (pedro:User {id: 'u3', nome: 'Pedro', idade: 21, perfil: 'Pop'});

// 4. Criar Artistas
MERGE (wkd:Artist {nome: 'The Weeknd'});
MERGE (mta:Artist {nome: 'Metallica'});
MERGE (dft:Artist {nome: 'Daft Punk'});

// 5. Criar Gêneros
MERGE (pop:Genre {nome: 'Pop'});
MERGE (rock:Genre {nome: 'Rock'});
MERGE (eletronica:Genre {nome: 'Eletrônica'});

// ============================================================================
// CRIAÇÃO DE MÚSICAS E RELACIONAMENTOS ESTRUTURAIS
// ============================================================================

// Músicas - The Weeknd
MERGE (s1:Song {titulo: 'Blinding Lights'})-[:CANTA_POR]->(wkd)
MERGE (s1)-[:DO_GENERO]->(pop)
MERGE (s1)-[:DO_GENERO]->(eletronica);

MERGE (s2:Song {titulo: 'Starboy'})-[:CANTA_POR]->(wkd)
MERGE (s2)-[:CANTA_POR]->(dft) // Feat
MERGE (s2)-[:DO_GENERO]->(pop);

// Músicas - Metallica
MERGE (s3:Song {titulo: 'Enter Sandman'})-[:CANTA_POR]->(mta)
MERGE (s3)-[:DO_GENERO]->(rock);

MERGE (s4:Song {titulo: 'Nothing Else Matters'})-[:CANTA_POR]->(mta)
MERGE (s4)-[:DO_GENERO]->(rock);

// Músicas - Daft Punk
MERGE (s5:Song {titulo: 'One More Time'})-[:CANTA_POR]->(dft)
MERGE (s5)-[:DO_GENERO]->(eletronica);

// ============================================================================
// SIMULAÇÃO DE INTERAÇÕES (O Grafo Social)
// ============================================================================

// Interações do usuário João Luiz
MATCH (u:User {nome: 'João Luiz'}), (s:Song {titulo: 'Blinding Lights'}) 
MERGE (u)-[:OUVIU {qtd: 15, ultima_vez: '2026-02-18'}]->(s);

MATCH (u:User {nome: 'João Luiz'}), (s:Song {titulo: 'Starboy'}) 
MERGE (u)-[:CURTIU]->(s);

// Interações da usuária Ana (Cria intersecção de gostos para o algoritmo)
MATCH (u:User {nome: 'Ana'}), (s:Song {titulo: 'Enter Sandman'}) 
MERGE (u)-[:CURTIU]->(s);

MATCH (u:User {nome: 'Ana'}), (s:Song {titulo: 'Starboy'}) 
MERGE (u)-[:OUVIU {qtd: 5, ultima_vez: '2026-02-15'}]->(s);

MATCH (u:User {nome: 'Ana'}), (s:Song {titulo: 'One More Time'}) 
MERGE (u)-[:CURTIU]->(s);


// ============================================================================
// CONSULTAS DE RECOMENDAÇÃO (Exemplos para avaliação do projeto)
// ============================================================================

/*
// Consulta 1: Filtragem Colaborativa ("Quem ouviu isso, também ouviu...")
MATCH (eu:User {nome: 'João Luiz'})-[:OUVIU|CURTIU]->(gosto_comum:Song)
MATCH (gosto_comum)<-[:OUVIU|CURTIU]-(vizinho:User)
WHERE vizinho.id <> eu.id
MATCH (vizinho)-[:OUVIU|CURTIU]->(recomendacao:Song)
WHERE NOT (eu)-[:OUVIU|CURTIU]->(recomendacao)
RETURN recomendacao.titulo AS Musica_Sugerida, count(vizinho) AS Forca_Recomendacao
ORDER BY Forca_Recomendacao DESC;

// Consulta 2: Baseada em Conteúdo (Mais músicas do mesmo artista)
MATCH (eu:User {nome: 'João Luiz'})-[:OUVIU|CURTIU]->(musica:Song)-[:CANTA_POR]->(artista:Artist)
MATCH (artista)<-[:CANTA_POR]-(nova_musica:Song)
WHERE NOT (eu)-[:OUVIU|CURTIU]->(nova_musica)
RETURN DISTINCT nova_musica.titulo AS Recomendacao, artista.nome AS Motivo;
*/