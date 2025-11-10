from django.contrib import admin
from .models import QuestionTypes, Questions, Scores
# Register your models here.

admin.site.register(QuestionTypes)
admin.site.register(Questions)
admin.site.register(Scores)
