from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('entrylist', views.entry_list, name='entry_list'),
    path('entrylist/<int:pk>/', views.entry_list_with_selected, name='entry_list_with_selected'),
    path('entry/<int:pk>/', views.entry_detail, name='entry_detail'),
    path('newentry', views.new_entry, name='new_entry'),
    path('entry/<int:pk>/edit/', views.edit_entry, name='edit_entry'),
    path('entry/<int:pk>/delete/', views.delete_entry, name='delete_entry')
]