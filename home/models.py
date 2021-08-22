from django.db import models

# Create your models here.

class UserVerifyData(models.Model):

	username = models.CharField(unique=True, max_length=15)
	verified = models.BooleanField()
	otp = models.IntegerField()

	class Meta:
		verbose_name = "UserVerifyData"
		verbose_name_plural = "UserVerifyDatas"

	def __str__(self):
		return self.username

	def get_absolute_url(self):
		return reverse("UserVerifyData_detail", kwargs={"pk": self.pk})
