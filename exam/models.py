from django.db import models

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

	user = models.ForeignKey(UserData, on_delete=models.CASCADE)
	question_id = models.IntegerField(unique=True)
	answer_id = models.IntegerField()
	exam_id = models.IntegerField()
	ans_status = models.CharField(max_length=10, default="aamfr")

	def __str__(self):
		return "Question id: "+str(self.question_id)+", Answer_id: "+str(self.answer_id)

class ExamData(models.Model):
	
	title = models.CharField(max_length=50)
	start_time = models.CharField(max_length=10)
	end_time = models.CharField(max_length=10)
	total_time = models.CharField(max_length=10)
	exam_id = models.IntegerField(unique=True)
	date = models.DateField()

	class Meta:
		verbose_name = "ExamData"
		verbose_name_plural = "ExamDatas"

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("Exam_detail", kwargs={"pk": self.pk})
