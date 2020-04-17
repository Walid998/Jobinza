from django.contrib import admin

# Register your models here.

from company.models import CreatePost,Match_Results,Send_Email

admin.site.register(CreatePost)
admin.site.register(Match_Results)
admin.site.register(Send_Email)