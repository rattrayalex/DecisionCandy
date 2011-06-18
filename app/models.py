from django.db import models



class Image(models.Model):
	pass

class Project(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	creator = models.ForeignKey(User)
	payout = models.IntegerField()
	attributes = []
	images = models.ManyToManyField(Image)
	pass

class User(models.Model):
	name = models.CharField(max_length=100)

