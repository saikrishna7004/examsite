from django.contrib import admin
from django.urls import path, include
from exam import views

urlpatterns = [
    path('', views.index, name="index"),
    path('examInstructions/', views.examInstructions, name="index"),
    path('examInstructions/answer/', views.answer, name="answer"),
    path('examInstructions/delete/', views.delete, name="delete"),
    path('results/<int:exam_id>/', views.results, name="results"),
    path('create/', views.create, name="create"),
    path('maths/', views.matheditor, name="maths"),
]

admin.site.site_header = "Exam Site Admin"
admin.site.site_title = "Exam Site Admin Portal"
admin.site.index_title = "Welcome to Exam Site Portal"
