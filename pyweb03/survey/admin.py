from django.contrib import admin
from survey.models import Survey, Answer

class SurveyAdmin(admin.ModelAdmin):
    list_display = ("question","ans1","ans2","ans3","ans4","status")

admin.site.register(Survey,SurveyAdmin)
admin.site.register(Answer)
