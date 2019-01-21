from django.db import models

class Survey(models.Model):
    survey_idx = models.AutoField(primary_key=True)
    question = models.TextField(null=False)
    ans1 = models.TextField(null=True)
    ans2 = models.TextField(null=True)
    ans3 = models.TextField(null=True)
    ans4 = models.TextField(null=True)
    status = models.CharField(max_length=1, default="y")

class Answer(models.Model):
    answer_idx = models.AutoField(primary_key = True)
    survey_idx = models.IntegerField()
    num = models.IntegerField()