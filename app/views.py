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
from operator import mul
import Image as IMG
from django.core.files.uploadedfile import InMemoryUploadedFile

from DecisionCandy.app.models import *

import os, sys, datetime, copy


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

def isUnique(matrix, pair):
  for p in matrix:
##    print "testing..."
    if (p[0]==pair[0] and p[1]==pair[1]) or (p[1]==pair[0] and p[0]==pair[1]):
##      print "it's not unique!"
      return False
  return True

def rank(request, project): 
  project_name = str(project)
  project =  Project.objects.get(name=project_name)
  images = [image.large for image in project.images.all()]
  
  n = len(images)
  k = 2
  nCr = lambda n,k: int(round(
    reduce(mul, (float(n-i)/(i+1) for i in range(k)), 1)
    ))
  max_limit = 10
  limit = min(nCr(n,k), max_limit)
  pairs = []
  for i in range(limit):
##    print "in big for loop"
    left, right = random.sample(images, 2)
    pair = [left, right]
    while isUnique(pairs, pair)!= True:
##      print "in while loop"
      left, right = random.sample(images, 2)
      pair = [left, right]
    pairs.append(pair)
##    print i
      
##  print pairs
  context = {
    'Project': project,
##    'left_img': left,
##    'right_img': right,
    'limit': limit,
    'img_list': pairs,
    'user': request.user,
    }
  return render_to_response('rank.html',context, context_instance = RequestContext(request))


def vote(request):
  print "in vote method"
  if request.method == 'POST':
    data = request.POST
    print data
    w = Image.objects.get(large__exact=data['winner'])
    l = Image.objects.get(large__exact=data['loser'])
    print w, l
    vote = Vote(
    winner = w,
    loser = l,
    time = datetime.datetime.now()
    )
  vote.save()
  return HttpResponse('boo!')

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
      
      user = auth.authenticate(username=email, password=password)
      if user is not None:
        auth.login(request, user)
      return HttpResponseRedirect('/loggedin/')
  else:
    form = SignUpForm()
  return render_to_response('signup.html', {'form':form,}, context_instance = RequestContext(request))

class create_project(forms.Form):
  name = forms.CharField(max_length=100, label="Project Name")
  description = forms.CharField(widget=forms.Textarea, label="A description of your project")
  criteria = forms.CharField(max_length=100, label="Criteria (Which one ___?)")
  more_criteria = forms.CharField(widget=forms.Textarea, label="More Criteria (what else is important?)")

class upload_image_form(forms.Form):
  filename = forms.ImageField(label = "Image")

def thumbify(infile, size, size_name):
  name = infile.name.split(".", 1)[0] + "_" + size_name + ".PNG"
  outfile = InMemoryUploadedFile(None, None, None, None, None, None)
  outfile.name = name#copy.copy(infile)
  print outfile
##  outfile.name = outfile.name.split(".", 1)[0] + "_" + size_name + ".PNG"
  print outfile.name
  try:
    im = IMG.open(infile, "r")
    im.load()
    im.thumbnail(size)
    print im
    im.save(outfile, "PNG")
##    out = IMG.open(outfile, "r")
##    print out
    return outfile
  except IOError:
    print "cannot create thumbnail for ", outfile
  
def upload_files(request):
  UploaderFormset = formset_factory(upload_image_form, extra=10)
  if request.method == 'POST':
    image_form = UploaderFormset(request.POST, request.FILES)
    project_form = create_project(request.POST)
    if image_form.is_valid() and project_form.is_valid():
      if len(request.FILES) < 2:
        return HttpResponse('Upload more pix!')
      else:
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
        large_size = 330, 230
        medium_size = 210, 150
        project = Project.objects.get(name=project_form.cleaned_data['name'])
        for image in request.FILES:
          datapoint = 'form-%s-filename' % str(n)
          full = request.FILES[datapoint]
##          large = thumbify(full, large_size, "large")
##          medium = thumbify(full, medium_size, "medium")
          i = Image(project=project,
                    full=full#, large=large, medium=medium
                    )
          i.save()
          n += 1
        return HttpResponseRedirect('../rank/'+ project.name.replace(' ', '%20'))
  else:
      project_form = create_project()
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
##    print "in signin post"
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
##    print "in signin else"
    form = SignInForm() 
##  print "in signin "
  return render_to_response('signin.html', {'form': form, 'user': request.user,},context_instance=RequestContext(request))

def loggedin(request):
  username = request.user.client.name
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

