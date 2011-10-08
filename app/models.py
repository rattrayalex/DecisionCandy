from django.db import models
from django.contrib.auth.models import User
import datetime

gender_choices = (
    ('M', 'Male'),
    ('F', 'Female'),
    )

class Project(models.Model): 
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey('Client', related_name='projects')
    reward = models.FloatField(default=0)
    criteria = models.CharField(max_length=100)
    more_criteria = models.TextField()

    def __unicode__(self):
        return self.name

class Image(models.Model): 
    project = models.ForeignKey(Project, related_name='images')
    img = models.ImageField(upload_to='projects')

    @property
    def score(self):
        return self.winvotes.count()

    def __unicode__(self):
        return str(self.img)

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    signup_date = models.DateTimeField(default=datetime.datetime.today())

    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.name

class Client(UserProfile):
    description = models.TextField()

class Minion(UserProfile):
    gender = models.CharField(max_length=1,choices=gender_choices)
    age = models.PositiveIntegerField(blank=True, null=True)
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=2, blank=True)
    country = models.CharField(max_length=50, blank=True)

class Vote(models.Model):
    winner = models.ForeignKey(Image, related_name='winvotes')
    loser = models.ForeignKey(Image, related_name='losevotes')
    voter = models.ForeignKey(Minion, null=True, blank=True)
    index = models.IntegerField(null=True, blank=True)
    time = models.DateTimeField(default=datetime.datetime.now())
    winner_comment = models.CharField(max_length=1000, blank=True)
    loser_comment = models.CharField(max_length=1000, blank=True)

    def __unicode__(self):
        return "w: %s, l: %s" % (self.winner, self.loser)

