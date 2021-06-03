from django.contrib import admin

# Register your models here.

from .models import Question, Choice

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

admin.site.register(Question, QuestionAdmin)