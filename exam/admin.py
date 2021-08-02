from django.contrib import admin

# Register your models here.

from .models import Question, Choice, UserData, QuestionAnswer, ExamData, ExamStatus

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question Description', {'fields': ['exam_id','question_id','question_text','answer_id']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('exam_id','question_text', 'question_id', 'answer_id')
    list_filter = ['exam_id']
    search_fields = ['exam_id', 'question_text']

class QuestionAnswerInline(admin.StackedInline):
    model = QuestionAnswer
    extra = 1

class UserDataAdmin(admin.ModelAdmin):
    fieldsets = [
        ('UserData Description', {'fields': ['user_name', 'user_id']}),
    ]
    inlines = [QuestionAnswerInline]
    list_display = ('user_name', 'user_id')
    list_filter = ['user_id']
    search_fields = ['user_id', 'user_name']

class ExamDataAdmin(admin.ModelAdmin):
    fieldsets = [
        ('ExamData Description', {'fields': ['title', 'start_time', 'end_time', 'total_time', 'exam_id', 'date']}),
    ]
    list_display = ('exam_id', 'title', 'date', 'start_time')
    list_filter = ['exam_id']
    search_fields = ['exam_id', 'title']

class ExamStatusAdmin(admin.ModelAdmin):
    fieldsets = [
        ('ExamStatus Description', {'fields': ['user_id', 'exam_id', 'status', 'time_left']}),
    ]
    list_display = ('user_id', 'exam_id', 'status', 'time_left')
    list_filter = ['exam_id', 'user_id']
    search_fields = ['exam_id', 'user_id']


admin.site.register(Question, QuestionAdmin)
admin.site.register(UserData, UserDataAdmin)
admin.site.register(ExamData, ExamDataAdmin)
admin.site.register(ExamStatus, ExamStatusAdmin)
