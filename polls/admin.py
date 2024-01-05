from django.contrib import admin
from .models import Question, Choice
# Register your models here.

#StackedInline adds seperrate forms for each new object
#TabularInline adds a table and one column for each object which takes less space
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date','was_published_recently')
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    # fields = ['pub_date','question_text' ]
    # fieldset is used for grouping fields and displaying
    fieldsets = [(None, {"fields":['question_text']}),
                 ("Date Information", {"fields":['pub_date'], 'classes':["collapse"]}),]
    inlines = [ChoiceInline]
    
    
admin.site.register(Question, QuestionAdmin)
