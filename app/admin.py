from DecisionCandy.app.models import *
from django.contrib import admin

class ImageAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Image, ImageAdmin)
admin.site.register(Project)
admin.site.register(Client)
admin.site.register(Vote)
admin.site.register(Minion)
