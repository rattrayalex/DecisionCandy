import random
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core import serializers
from django.utils import simplejson
from django.forms import ModelForm
from django.template import RequestContext

from DecisionCandy.app.models import *


ROW_WIDTH = 3


def divide(n, k):
  '''Divide n into sets of size of k or smaller.'''
  for i in range(0, len(n), k):
    yield n[i:i+k]


def index(request):
  projects = Project.objects.all().order_by('name')
  context = {
      'project_table': divide(projects, ROW_WIDTH)
      }
  return render_to_response('index.html', context)


def choose(request):
  projects = Project.objects.all().order_by('name')
  context = {
      'project_table': divide(projects, ROW_WIDTH)
      }
  return render_to_response('choose.html',context)


def choices(request):
  project =  Project.objects.get(name=request.GET['project'])
  images = [image.img for image in project.images.all()]
  left, right = random.sample(images, 2)
  context = {
    'Project': project,
    'left_img': left,
    'right_img': right,
    }
  return render_to_response('choices.html', context)


def rank(request): 
  project_name = request.GET['project']
  project =  Project.objects.get(name=project_name)
  images = [image.img for image in project.images.all()]
  left, right = random.sample(images, 2)
  context = {
    'Project': project,
    'left_img': left,
    'right_img': right,
    }
  return render_to_response('rank.html',context)


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


def thanks(request):
  project_name = request.GET['project']
  project =  Project.objects.get(name=project_name)
  context = {
          'Project': project,
          }
  return render_to_response('thanks.html',context)

class SignUpFormAgain(ModelForm):
    class Meta:
        model = Client

def SignUpForm(request):
  if request.method == 'POST':
    form = SignUpFormAgain(request.POST)
    if form.is_valid():
      return HttpREsponseRedirect('/loggedin/')
  else:
    form = SignUpFormAgain()
  return render_to_response('signup.html', {'form':form,})


class SignInForm(forms.Form):
  email = forms.CharField(max_length=100)
  password = forms.CharField(widget=forms.PasswordInput)

def signin(request): 
##  if request.method != 'POST':
##    raise HTTP404('Only POSTs are allowed')
##  try:
##    m = 
  if request.method == 'POST':
    print "in signin post"
    form = SignInForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      u = User.objects.get(username__exact=email)
      if u.check_password(password):  
        return HttpResponseRedirect('/loggedin/')
      else:
        return HttpResponseRedirect('/signin/')
  else:
    print "in signin else"
    form = SignInForm() 
  print "in signin "
  return render_to_response('signin.html', {'form': form},context_instance=RequestContext(request))

def loggedin(request):
  return render_to_response('loggedin.html',{})
  

def results(request):
  project_name = request.GET['project']
  images = list(Image.objects.filter(project__name=project_name))
  images.sort(key = lambda x: -x.score)
  project = Project.objects.get(name=project_name)
  context = {
    'image_list': divide(images, ROW_WIDTH),
    'project': project,
    }
  return render_to_response('results.html', context)

def create_account(request):
  pass
