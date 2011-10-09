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


def choices(request):
  project =  Project.objects.get(name=request.GET['project'])
  images = [image.img for image in project.images.all()]
  left, right = random.sample(images, 2)
  context = {
    'Project': project,
    'left_img': left,
    'right_img': right,
    'user': request.user,
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
    'user': request.user,
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
    
def upload_files(request):
  if request.method == 'POST':
    project_form = create_project(request.POST)
    image_form = upload_image_form(request.POST)
    if form.is_valid():
      new_project = project_form.save()
      new_iamge = image_form.save()
  else:
      project_form = create_project()
      image_form = upload_image_form()
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

def results(request):
  project_name = request.GET['project']
  images = list(Image.objects.filter(project__name=project_name))
  images.sort(key = lambda x: -x.score)
  project = Project.objects.get(name=project_name)
  context = {
    'image_list': divide(images, ROW_WIDTH),
    'project': project,
    'user': request.user,
    }
  return render_to_response('results.html', context)

class UploaderForm(forms.Form):
  pass
##  file1 = forms.FileField(upload_to='user_files')
##
##
##  UploaderFormset = formset_factory(UploaderForm)
##
##  # long as you specify 'form-TOTAL_FORMS' and 2 other fields listed in the docs,
##  # the formset will auto generate form instances & populate with fields based on
##  # their 0 index.
##  formset = UploaderFormset(request.POST)
##
##  for form in formset.forms:
##      form.save()
