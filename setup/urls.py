from django.contrib import admin
from django.urls import path, include # Não esqueça de importar o include!

urlpatterns = [
    path('admin/', admin.site.urls),
    # Tudo que começar com "api/" vai ser redirecionado para o nosso app
    path('api/', include('api.urls')), 
]