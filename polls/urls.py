from django.urls import path
from . import views

app_name = "polls" #this is used for namespacing purposes
urlpatterns = [
    path("",views.index, name="index"),
    # path("poll", views.poll, name="poll")
    path("question/<int:question_id>", views.show, name="show_question"),
    path("question/<int:question_id>/result", views.result, name="question_result"),
    path("question/<int:question_id>/vote", views.vote, name="question_vote"),
    
]
