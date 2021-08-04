from django.contrib import admin
from django.urls import path, include
from exam import views

urlpatterns = [
    path('', views.index, name="index"),
    path('examInstructions/', views.examInstructions, name="index"),
    path('examInstructions/answer/', views.answer, name="answer"),
    path('examInstructions/delete/', views.delete, name="delete"),
    path('results/', views.results, name="results"),
    path('results/<int:exam_id>/', views.resultView, name="resultView"),
    path('upload/', views.upload, name="upload"),
    path('create/', views.create, name="create"),
    path('maths/', views.matheditor, name="maths"),
    path('test/', views.test, name="test"),
]

admin.site.site_header = "Exam Site Admin"
admin.site.site_title = "Exam Site Admin Portal"
admin.site.index_title = "Welcome to Exam Site Portal"
