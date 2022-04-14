from django.contrib import admin
from django.utils.timezone import localdate
from django.db import transaction

# Register your models here.

from .models import DescAnswer, Question, Choice, Result, UserData, QuestionAnswer, ExamData, ExamStatus, PaperModel, Subject

@transaction.atomic
def change_date(modeladmin, request, queryset):
    for examdata in queryset:
        examdata.date=localdate()
        examdata.save(update_fields=['date'])
change_date.short_description = 'Change Date to Today'

@transaction.atomic
def turn_on(modeladmin, request, queryset):
    for examdata in queryset:
        examdata.date=localdate()
        examdata.status = True
        examdata.save(update_fields=['date', 'status'])
turn_on.short_description = 'Turn on Test'

@transaction.atomic
def turn_off(modeladmin, request, queryset):
    for examdata in queryset:
        examdata.status = True
        examdata.save(update_fields=['status'])
turn_off.short_description = 'Turn off Test'


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
        ('ExamData Description', {'fields': ['title', 'start_time', 'end_time', 'total_time', 'type', 'exam_id', 'date', "status"]}),
    ]
    list_display = ('exam_id', 'title', 'date', 'type', 'start_time', 'status')
    list_filter = ['exam_id']
    search_fields = ['exam_id', 'title']
    actions = [change_date, turn_on, turn_off]

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

class ResultAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Result Description', {'fields': ['user_id', 'exam_id', 'correct', 'wrong', 'unattempted', 'correct_marks', 'wrong_marks', 'total']}),
    ]
    list_display = ('user_id', 'exam_id', 'correct', 'wrong', 'unattempted', 'total')
    list_filter = ['user_id', 'exam_id']
    search_fields = ['user_id', 'exam_id']

admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
admin.site.register(DescAnswer)
admin.site.register(Result, ResultAdmin)
admin.site.register(UserData, UserDataAdmin)
admin.site.register(ExamData, ExamDataAdmin)
admin.site.register(ExamStatus, ExamStatusAdmin)
admin.site.register(PaperModel, PaperModelAdmin)
