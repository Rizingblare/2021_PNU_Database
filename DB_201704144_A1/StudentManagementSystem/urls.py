from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('create/', views.create, name='create'),
    path('edit/',views.edit, name='edit'),
    path('delete/',views.delete, name='delete'),
    path('create/createTodo/',views.createTodo),
    path('edit/editTodo/',views.editTodo),
]