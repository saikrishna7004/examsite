from django.db import models
from django.dispatch import receiver
from django.db.models import signals
from django.template.defaultfilters import truncatewords
from django.urls import reverse
from django.contrib.auth.models import User

from home.models import UserVerifyData

# Create your models here.

class Question(models.Model):

	question_id = models.IntegerField(unique=True)
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
	
	@property
	def short_question_text(self):
		return truncatewords(self.question_text, 6)	

class Choice(models.Model):

	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=100)
	choice_id = models.IntegerField(unique=True)

	def __str__(self):
		return self.choice_text

class UserData(models.Model):

	user_name = models.CharField(max_length=50)
	user_id = models.IntegerField(unique=True)

	class Meta:
		verbose_name = "UserData"
		verbose_name_plural = "UserDatas"

	def __str__(self):
		return self.user_name

	def get_absolute_url(self):
		return reverse("User_detail", kwargs={"pk": self.pk})

class QuestionAnswer(models.Model):
	
	ANS_STATUS_CHOICES = (
		('aamfr','Answered and Marked for Review'),
		('ans', 'Answered and Saved'),
	)
	
	user = models.ForeignKey(UserData, on_delete=models.CASCADE)
	question_id = models.IntegerField()
	answer_id = models.IntegerField()
	exam_id = models.IntegerField()
	ans_status = models.CharField(max_length=10, choices=ANS_STATUS_CHOICES, default="aamfr")

	def __str__(self):
		return "Question id: "+str(self.question_id)+", Answer_id: "+str(self.answer_id)

class ExamData(models.Model):
	
	title = models.CharField(max_length=50)
	start_time = models.CharField(max_length=10)
	end_time = models.CharField(max_length=10)
	total_time = models.CharField(max_length=10)
	exam_id = models.IntegerField(unique=True)
	type = models.CharField(max_length=10, default="custom-21")
	date = models.DateField()
	status = models.BooleanField(default=False)

	class Meta:
		verbose_name = "ExamData"
		verbose_name_plural = "ExamDatas"

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("Exam_detail", kwargs={"pk": self.pk})

class ExamStatus(models.Model):
	
	STATUS_CHOICES = (
		('completed','Completed'),
		('started', 'Started'),
	)
	
	user_id = models.IntegerField()
	exam_id = models.IntegerField()
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="started")
	time_left = models.CharField(max_length=20)
	
	class Meta:
		verbose_name = "ExamStatus"
		verbose_name_plural = "ExamStatuses"

	def __str__(self):
		return self.status

	def get_absolute_url(self):
		return reverse("ExamStatus_detail", kwargs={"pk": self.pk})

class PaperModel(models.Model):

	type = models.CharField(max_length=10, unique=True)
	
	class Meta:
		verbose_name = "PaperModel"
		verbose_name_plural = "PaperModels"

	def __str__(self):
		return self.type

	def get_absolute_url(self):
		return reverse("PaperModel_detail", kwargs={"pk": self.pk})

class Subject(models.Model):

	paper = models.ForeignKey(PaperModel, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	length = models.IntegerField()
	start = models.IntegerField()
	end = models.IntegerField()

	def __str__(self):
		return self.name

class Result(models.Model):

	user_id = models.IntegerField()
	exam_id = models.IntegerField()
	correct = models.IntegerField()
	wrong = models.IntegerField()
	unattempted = models.IntegerField()


	class Meta:
		verbose_name = "Result"
		verbose_name_plural = "Results"

	def __str__(self):
		return self.user_id

	def get_absolute_url(self):
		return reverse("Result_detail", kwargs={"pk": self.pk})

@receiver(signals.post_save, sender=User)
def create_user_details(sender, instance, **kwargs):
	print(instance.first_name, instance.username )
	if UserData.objects.filter(user_id=instance.username).exists() or UserVerifyData.objects.filter(username=instance.username).exists():
		return
	UserData.objects.create(user_name=instance.first_name, user_id=instance.username)
	UserVerifyData.objects.create(username=instance.username, verified=True, otp=0)