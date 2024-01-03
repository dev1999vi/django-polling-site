from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
# from django.template import loader
# from django.shortcuts import render
from .models import Question, Choice

# Create your views here.

"""Non Generic Views"""
# def index(request):
#     latest_question = Question.objects.order_by("-pub_date")
#     # output = ", ".join(q.question_text for q in latest_question)
#     # template = loader.get_template('polls/index.html')
#     context = {
#         'latest_questions_list': latest_question,
#     }
#     # return HttpResponse(template.render(context, request))
#     return render(request, 'polls/index.html', context)

# # def poll(request):
# #     return HttpResponse("This is a poll page.")
# def show(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk = question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question Does not exist.")
    
#     """There is shortcut for all the above code"""
    
#     question  =  get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/show.html', {"question": question})
#     # if question:
#     #     return HttpResponse(f"You are looking at the question: {question.question_text}")
#     # else:
#     #     return HttpResponse("Question does not exist")
    
# def result(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {"question": question})

"""Generic Views"""

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = "latest_questions_list"
    
    def get_queryset(self) -> QuerySet[Any]:
        return Question.objects.order_by("-pub_date")
    
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/show.html'
    
class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    # return HttpResponse(f"You are voting for the question: {question_id}")
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'polls/show.html', {"question": question, "error_message": "You didn't select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:question_result", args=(question.id,)))