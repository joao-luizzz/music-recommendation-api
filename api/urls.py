from django.urls import path
from .views import RecomendacaoMusicaView, home_spotify # Importe a nova função aqui!

urlpatterns = [
    # Rota que você já estava usando (JSON)
    path('recomendacoes/<str:nome_usuario>/', RecomendacaoMusicaView.as_view(), name='recomendacoes'),
    
    # NOVA ROTA para o visual estilo Spotify
    path('player/<str:nome_usuario>/', home_spotify, name='player'), 
]