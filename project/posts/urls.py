from django.urls import path
from core.views import home
from . import views

app_name = "posts"

urlpatterns = [
    path("home/", home, name="home"),  # Usa la vista 'home' importada
    path('<int:match_id>/', views.post_detail, name='post_detail'),
]