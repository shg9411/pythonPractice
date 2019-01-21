from django.contrib import admin
from guestbook.models import Guestbook

class GuestbookAdmin(admin.ModelAdmin):
    list_display=("name","email","passwd","content")

admin.site.register(Guestbook,GuestbookAdmin)
