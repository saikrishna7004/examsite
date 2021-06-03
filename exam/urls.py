from django.contrib import admin
from django.urls import path, include
from exam import views

urlpatterns = [
    path('', views.index, name="index"),
    path('examInstructions/', views.examInstructions, name="index"),
    path('examInstructions/answer/', views.answer, name="answer"),
    path('results/<int:exam_id>/', views.results, name="results"),
]
