import datetime
from django.db import models
from django.utils import timezone
# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return f"Text:{self.question_text}, Publish Date:{self.pub_date.strftime('%Y-%m-%d %H:%M:%S.%f')}"
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return f"Options:{self.choice_text}, Votes:{self.votes}, Question: {self.question}"