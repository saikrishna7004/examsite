from django.db import models

# Create your models here.

class Question(models.Model):

    question_id = models.IntegerField()
    question_text = models.CharField(max_length=1000)
    answer_id = models.IntegerField()
    exam_id = models.IntegerField()

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse("Question_detail", kwargs={"pk": self.pk})

class Choice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    choice_id = models.IntegerField()

    def __str__(self):
        return self.choice_text
