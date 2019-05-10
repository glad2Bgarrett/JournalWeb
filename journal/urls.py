from django.urls import path
from . import views


urlpatterns = [
    path('', views.entry_list, name='entry_list'),
    path('entry/<int:pk>/', views.entry_detail, name='entry_detail')
]