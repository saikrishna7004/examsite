from django.contrib import admin
from django.urls import path, include
from exam import views

urlpatterns = [
    path('', views.index, name="index"),
    path('examInstructions/', views.examInstructions, name="index"),
    path('examInstructions/answer/', views.answer, name="answer"),
    path('examInstructions/answertext/', views.answertext, name="answertext"),
    path('examInstructions/delete/', views.delete, name="delete"),
    path('examInstructions/deletetext/', views.deletetext, name="deletetext"),
    path('results/', views.results, name="results"),
    path('results/evaluate/', views.evaluatedesc, name="evaluatedesc"),
    path('results/evaluate/save/', views.savemarks, name="savemarks"),
    path('results/evaluate/done/', views.doneEvaluate, name="doneevaluating"),
    path('results/evaluate/<int:exam_id>', views.evaluatelist, name="evaluatelist"),
    path('results/evaluate/<int:exam_id>/<int:user_id>', views.evaluateview, name="evaluateview"),
    path('results/students/', views.studentresults, name="studentresults"),
    path('results/students/<int:exam_id>', views.studentresultsview, name="studentresultsview"),
    path('results/generate/', views.generateResults, name="resultsgenerate"),
    path('results/generate/<int:exam_id>', views.generateResultsView, name="resultsgeneratewithid"),
    path('results/<int:exam_id>/', views.resultView, name="resultView"),
    path('results/<int:exam_id>/details', views.resultdetails, name="resultDetails"),
    path('all/', views.examListTurnOn, name="exam list turn on"),
    path('turnon/<int:exam_id>', views.examTurnOn, name="turn on"),
    path('turnoff/<int:exam_id>', views.examTurnOff, name="turn off"),
    path('results/rollback/<int:exam_id>', views.rollbackResults, name="roll back results"),
    path('upload/', views.upload, name="upload"),
    path('create/', views.create, name="create"),
    path('maths/', views.matheditor, name="maths"),
    path('submit/', views.submit, name="submit"),
    path('test/', views.test, name="test"),
]

admin.site.site_header = "Exam Site Admin"
admin.site.site_title = "Exam Site Admin Portal"
admin.site.index_title = "Welcome to Exam Site Portal"
