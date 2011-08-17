from DecisionCandy.app.models import Image, Project, Client
from django.contrib import admin

class ImageAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Image, ImageAdmin)
admin.site.register(Project)
admin.site.register(Client)
