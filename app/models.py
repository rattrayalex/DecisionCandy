from django.db import models
import random



class Project(models.Model): 
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey('Client')
    reward = models.FloatField(default=0)
    criteria = models.CharField(max_length=100)
    more_criteria = models.TextField()
    
##  attributes = []

    def __unicode__(self):
        return self.name

class Image(models.Model): 
    project = models.ForeignKey(Project)
    img = models.ImageField(upload_to='projects')
    number = models.IntegerField(default=int(random.randrange(1,100,1)))
    votes_for = models.IntegerField(default=0)
    votes_against = models.IntegerField(default=0)
    def __unicode__(self):
        return str(self.project) + str(self.number)#image)

class Client(models.Model): 
    name = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()
    def __unicode__(self):
        return self.name





##def ImageHandler(instance, filename):
##    project = 'fake1'
##    path_base = 'projects/'
##    path = path_base + project + '/' + filename
##    return path
