import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return f"Text:{self.question_text}, Publish Date:{self.pub_date.strftime('%Y-%m-%d %H:%M:%S.%f')}"
    
    @admin.display(
        boolean= True,
        ordering= 'pub_date',
        description="Published recently?"
    )
    
    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.pub_date <= timezone.now()
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return f"Options:{self.choice_text}, Votes:{self.votes}, Question: {self.question}"