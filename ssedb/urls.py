from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_form, name='create_form'),
    path('show/all/', views.show_all, name='show_all'),
    path('show/<int:x0_id>/', views.show_one, name='show_one'),
    path('show/', views.show, name='show'),
    path('form/ssev5', views.ssev5_form, name='ssev5_form'),
    path('ssev5_engine/', views.ssev5_engine, name='ssev5_engine'),
]
