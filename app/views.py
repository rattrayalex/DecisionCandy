import random

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core import serializers
from django.utils import simplejson

from DecisionCandy.app.models import *

projects = Project.objects.all()
startrows = [1, 4, 7, 10, 13]
endrows = [3, 6, 9, 12, 15]


def standard_context():
  projects = Project.objects.all().order_by('name')
  context = {
    'project_list': projects,
    'startrow':startrows,
    'endrow':endrows
    }
  return context


def index(request):
  context = standard_context()
  return render_to_response('index.html', context)


def choose(request):
  context = standard_context()
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


def results(request):
  project_name = request.GET['project']
  images = list(Image.objects.filter(project__name=project_name))
  images.sort(key = lambda x: -x.score)
  project = Project.objects.get(name=project_name)
  context = {
    'image_list': images,
    'project': project,
    'startrow':startrows,
    'endrow':endrows,
    }
  return render_to_response('results.html', context)


def signin(request): 
  pass


def create_account(request):
  pass
