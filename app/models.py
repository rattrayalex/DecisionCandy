from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save
from django.core.files import File
import os.path

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
    full = models.ImageField(upload_to='projects') 
    large = models.ImageField(upload_to='large_thumbs')
    medium = models.ImageField(upload_to='medium_thumbs')

    @property
    def score(self):
        return self.winvotes.count()
    
    def __unicode__(self):
        return str(self.full)

    def save(self):
        super(Image, self).save()
        if self.full and not self.large and not self.medium: 
            # We use PIL's Image object
            # Docs: http://www.pythonware.com/library/pil/handbook/image.htm
            import Image as IMG
        
            # Set our max thumbnail size in a tuple (max width, max height)
            large_size = (330, 230)
            medium_size = (210, 150)

            # Open original photo which we want to thumbnail using PIL's Image
            # object
            media_root = os.path.join(os.path.dirname(__file__), '../front-end/media/').replace('\\','/')
            
            large_image = IMG.open(media_root + self.full.name)
            medium_image = IMG.open(media_root + self.full.name)
        
            # Convert to RGB if necessary
            # Thanks to Limodou on DjangoSnippets.org
            # http://www.djangosnippets.org/snippets/20/
            if large_image.mode not in ('L', 'RGB'):
                large_image = large_image.convert('RGB')
                medium_image = medium_image.convert('RGB')
        
            # We use our PIL Image object to create the thumbnail, which already
            # has a thumbnail() convenience method that contrains proportions.
            # Additionally, we use Image.ANTIALIAS to make the image look better.
            # Without antialiasing the image pattern artifacts may result.
            large_image.thumbnail(large_size, IMG.ANTIALIAS)
            medium_image.thumbnail(medium_size, IMG.ANTIALIAS)

            large_name = 'large_thumbs/' + self.full.name.split(".", 1)[0].split("/",1)[1] + ".PNG"#get_full_filename().split(".", 1)[0] + "_large.PNG"
            medium_name = 'medium_thumbs/' + self.full.name.split(".", 1)[0].split("/",1)[1] + ".PNG"#get_full_filename().split(".", 1)[0] + "_medium.PNG"
            print large_name, medium_name
            
            # Save the thumbnail to the computer
            large_image.save(media_root + large_name)
            medium_image.save(media_root + medium_name)
            # Save the thumbnail to the database
            self.large.name = large_name
            self.medium.name = medium_name
        
        # Save this photo instance      
        super(Image, self).save()

class UserProfile(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
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
    voter = models.ForeignKey(Minion, null=True, blank=True) # change to User?
    index = models.IntegerField(null=True, blank=True)
    time = models.DateTimeField(default=datetime.datetime.now())
    winner_comment = models.CharField(max_length=1000, blank=True)
    loser_comment = models.CharField(max_length=1000, blank=True)

    def __unicode__(self):
        return "w: %s, l: %s" % (self.winner, self.loser)

