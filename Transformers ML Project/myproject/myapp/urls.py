# myproject/urls.py
from django.urls import path, include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('translate/', views.translate_page, name='translate_page'),
    path('summarize/', views.summarize_page, name='summarize_page'),  # Add this line for the summarize view
    path('qnsans/', views.qnsans_page, name='qnsans_page'),
   #path('game/', views.play_pictionary, name='play_pictionary'),  # Add this line for the Pictionary game
    path('game-page/', views.game_page, name='game_page'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
