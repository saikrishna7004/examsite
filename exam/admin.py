from django.contrib import admin
from django.utils.timezone import localdate
from django.db import transaction

# Register your models here.

from .models import Question, Choice, UserData, QuestionAnswer, ExamData, ExamStatus, PaperModel, Subject

@transaction.atomic
def change_date(modeladmin, request, queryset):
    for examdata in queryset:
        examdata.date=localdate()
        examdata.save(update_fields=['date'])
change_date.short_description = 'Change Date to Today'


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question Description', {'fields': ['exam_id','question_id','question_text','answer_id']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('exam_id','short_question_text', 'question_id', 'answer_id')
    list_filter = ['exam_id']
    search_fields = ['exam_id', 'question_text']

class QuestionAnswerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question Answer Description', {'fields': ['user', 'question_id', 'answer_id', 'exam_id', 'ans_status']}),
    ]
    list_display= ('user', 'question_id', 'answer_id', 'exam_id', 'ans_status')
    list_filter = ['exam_id', 'user']
    search_fields = ['exam_id', 'user']

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
        ('ExamData Description', {'fields': ['title', 'start_time', 'end_time', 'total_time', 'type', 'exam_id', 'date']}),
    ]
    list_display = ('exam_id', 'title', 'date', 'type', 'start_time')
    list_filter = ['exam_id']
    search_fields = ['exam_id', 'title']
    actions = [change_date]

class ExamStatusAdmin(admin.ModelAdmin):
    fieldsets = [
        ('ExamStatus Description', {'fields': ['user_id', 'exam_id', 'status', 'time_left']}),
    ]
    list_display = ('user_id', 'exam_id', 'status', 'time_left')
    list_filter = ['exam_id', 'user_id']
    search_fields = ['exam_id', 'user_id']

class SubjectInline(admin.StackedInline):
    model = Subject
    extra = 3

class PaperModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('PaperModel Description', {'fields': ['type']}),
    ]
    inlines = [SubjectInline]
    list_display = ('type',)
    list_filter = ['type']
    search_fields = ['type']

admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
admin.site.register(UserData, UserDataAdmin)
admin.site.register(ExamData, ExamDataAdmin)
admin.site.register(ExamStatus, ExamStatusAdmin)
admin.site.register(PaperModel, PaperModelAdmin)
