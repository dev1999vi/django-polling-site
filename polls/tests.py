import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question, Choice
from django.urls import reverse
# Create your tests here.
def create_question(question_text, days):
    date = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=date)

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        
    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionIndexViewTest(TestCase):
    
    def test_no_question(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, "polls/index.html")
        self.assertEqual(len(response.context["latest_questions_list"]), 0)
        self.assertContains(response, "There are no polls available.")
        self.assertQuerySetEqual(response.context["latest_questions_list"], [])
    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question("Past Question", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_questions_list"], [question])
        self.assertTemplateUsed(response, "polls/index.html")
        
    def test_future_question(self):
        """
        Questions with a pub_date in the future are not displayed on the
        index page.
        """
        question = create_question("Future Question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_questions_list"], [])
        self.assertContains(response, "There are no polls available.")
        
    def test_both_future_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question("Past Question", -30)
        create_question("Future Question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_questions_list"], [question])
        self.assertTemplateUsed(response, "polls/index.html")
        
    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question("Past Question 1", -30)
        question2 = create_question("Past Question 2", -5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_questions_list"], [question2, question1])
        self.assertTemplateUsed(response, "polls/index.html")
        
class QuestionDetailViewTests(TestCase):
        
    def test_future_questions(self):
        """
        Questions with a pub_date in the future are not displayed on the
        detail page.
        """
        question = create_question("Future Question", 30)
        response = self.client.get(reverse("polls:show_question", args=(question.id,)))
        self.assertEqual(response.status_code, 404)
            
    def test_past_questions(self):
        """
        Questions with a pub_date in the past are displayed on the
        detail page.
        """
        question = create_question("Future Question", -30)
        response = self.client.get(reverse("polls:show_question", args=(question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["question"], question)
        self.assertTemplateUsed(response, "polls/show.html")
        