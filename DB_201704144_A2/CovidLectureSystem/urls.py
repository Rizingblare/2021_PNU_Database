from django.urls import path
from CovidLectureSystem import views

urlpatterns = [
    path('', views.display, name='index'),

    path('addStu/', views.addStu, name='addStu'),
    path('addProf/', views.addProf, name='addProf'),
    path('addCnt/', views.addCnt, name='addCnt'),
    path('addCovid/', views.addCovid, name='addCovid'),

    path('clearStu/', views.clearStu, name='clearStu'),
    path('clearProf/', views.clearProf, name='clearProf'),
    path('clearCnt/', views.clearCnt, name='clearCnt'),
    path('clearCovid/', views.clearCovid, name='clearCovid'),
]