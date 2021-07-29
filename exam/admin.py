from django.contrib import admin

# Register your models here.

from .models import Question, Choice, UserData, QuestionAnswer

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

admin.site.register(Question, QuestionAdmin)
admin.site.register(UserData, UserDataAdmin)