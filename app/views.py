import random
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core import serializers
from django.utils import simplejson
from django.forms import ModelForm
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import auth
from django.forms.formsets import formset_factory
import datetime

from DecisionCandy.app.models import *


ROW_WIDTH = 3


def divide(n, k):
  '''Divide n into sets of size of k or smaller.'''
  for i in range(0, len(n), k):
    yield n[i:i+k]


def index(request):
  projects = Project.objects.all().order_by('name')
  context = {
      'project_table': divide(projects, ROW_WIDTH),
      'user': request.user,
      }
  return render_to_response('index.html', context)


def choose(request):
  projects = Project.objects.all().order_by('name')
  context = {
      'project_table': divide(projects, ROW_WIDTH),
      'user': request.user,
      }
  return render_to_response('choose.html',context)


def choices(request, project):
  project_name = str(project).replace('%20',' ')
  project =  Project.objects.get(name=project_name)
  images = [image.img for image in project.images.all()]
  left, right = random.sample(images, 2)
  context = {
    'Project': project,
    'left_img': left,
    'right_img': right,
    'user': request.user,
    }
  return render_to_response('choices.html', context, context_instance = RequestContext(request))


def rank(request, project): 
  project_name = str(project)
  project =  Project.objects.get(name=project_name)
  images = [image.img for image in project.images.all()]
  left, right = random.sample(images, 2)
  context = {
    'Project': project,
    'left_img': left,
    'right_img': right,
    'user': request.user,
    }
  return render_to_response('rank.html',context, context_instance = RequestContext(request))


def rank_xhr(request, project_name, format):
  project = Project.objects.get(name=project_name)
  images = [image.img for image in project.images.all()]

  if request.is_ajax():
    if format == 'xml':
            mimetype = 'application/xml'
    elif format == 'json':
            mimetype = 'application/javascript'
    left, right = random.sample(images, 2)
    json_dict = {
      'left':left,
      'right':right
      }
    json_dump = simplejson.dumps(json_dict)
    return HttpResponse(json_dump, mimetype)       
  context = {
    'Project': project
    }
  return render_to_response('rank_xhr.html',context)

def vote(request, winner, loser):
  print "in vote method"
  winner = str(winner).replace('___', '.')
  loser = str(loser).replace('___', '.')
  vote = Vote(
    winner = str(winner),
    loser = str(loser),
    time = datetime.datetime.now()
    )
  vote.save()
  return render_to_response('voted', {}, context_instance = RequestContext(request))

def thanks(request, project):
  project_name = str(project)#.replace('%20', ' ')
  project =  Project.objects.get(name=project_name)
  context = {
          'Project': project,
          'user': request.user,
          }
  return render_to_response('thanks.html',context)

class SignUpFormAgain(ModelForm):
    class Meta:
        model = Client

class SignUpForm(forms.Form):
  email = forms.EmailField(max_length=30)
  password = forms.CharField(widget=forms.PasswordInput, label="Your Password")
  name = forms.CharField(max_length=50, label="Publicly visible name")
  description = forms.CharField(widget=forms.Textarea)
  
def signup(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      username = email
      name = form.cleaned_data['name']
      description = form.cleaned_data['description']

      user = User.objects.create_user(username, email, password)
      user.save()
      
      client = Client(name=name, email=email, user=user, description=description)
      client.save()
      u= auth.authenticate(username=email, password=password)
      auth.login(request, u)
      return HttpResponseRedirect('/loggedin/')
  else:
    form = SignUpForm()
  return render_to_response('signup.html', {'form':form,}, context_instance = RequestContext(request))

##class create_project(ModelForm):
##  class Meta:
##    model = Project
##
##class upload_image_form(ModelForm):
##  class Meta:
##    model = Image

class create_project(forms.Form):
  name = forms.CharField(max_length=100, label="Project Name")
  description = forms.CharField(widget=forms.Textarea, label="A description of your project")
  criteria = forms.CharField(max_length=100, label="Criteria (Which one ___?)")
  more_criteria = forms.CharField(widget=forms.Textarea, label="More Criteria (what else is important?)")

class upload_image_form(forms.Form):
  filename = forms.ImageField()#upload_to='user_files')
##  for form in formset.forms:
##      form.save()
  
def upload_files(request):
  UploaderFormset = formset_factory(upload_image_form, extra=9)
  if request.method == 'POST':
    image_form = UploaderFormset(request.POST, request.FILES)
    project_form = create_project(request.POST)
##    image_form = upload_image_form(request.POST)
    if image_form.is_valid() and project_form.is_valid():
      if len(image_form) < 2:
        return HttpResponse('Upload more pix!')
      new_project = Project(
        name=project_form.cleaned_data['name'],
        description=project_form.cleaned_data['description'],
        creator = request.user.client,
        reward = 0,
        criteria = project_form.cleaned_data['criteria'],
        more_criteria = project_form.cleaned_data['more_criteria']
        )
      new_project.save()
      n = 0
      for image in request.FILES:
        datapoint = 'form-%s-filename' % str(n)
        i = Image(project=Project.objects.get(name=project_form.cleaned_data['name']),
                  img = request.FILES[datapoint])
        i.save()
        n += 1
  else:
      project_form = create_project()
##      image_form = upload_image_form()
      image_form = UploaderFormset()
  context = {
    'project_form': project_form,
    'image_form': image_form,
    'user': request.user,
    }
  return render_to_response('upload.html', context, context_instance = RequestContext(request))

class SignInForm(forms.Form):
  email = forms.CharField(max_length=100)
  password = forms.CharField(widget=forms.PasswordInput)

def signin(request): 
  if request.method == 'POST':
    print "in signin post"
    form = SignInForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      user = auth.authenticate(username=email, password=password)
      if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/loggedin/')
      else:
        return HttpResponseRedirect('/signin/')
  else:
    print "in signin else"
    form = SignInForm() 
  print "in signin "
  return render_to_response('signin.html', {'form': form, 'user': request.user,},context_instance=RequestContext(request))

def loggedin(request):
  username = request.user.username
  return render_to_response('loggedin.html',{'username':username, 'user': request.user,})

def logout(request):
  auth.logout(request)
  return HttpResponseRedirect('/')

def results(request, project):
  project_name = str(project)
  images = list(Image.objects.filter(project__name=project_name))
  images.sort(key = lambda x: -x.score)
  project = Project.objects.get(name=project_name)
  context = {
    'image_list': divide(images, ROW_WIDTH),
    'project': project,
    'user': request.user,
    }
  return render_to_response('results.html', context)

