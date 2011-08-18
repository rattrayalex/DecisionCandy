from django.shortcuts import render_to_response
from DecisionCandy.app.models import *
import random

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

def choose_random(iterable):
        left = random.choice(iterable)
        right = random.choice(iterable)
        while left == right:
                right = random.choice(iterable)
        return left, right

def rank(request, project_name, stage): 
        project =  Project.objects.get(name=project_name)
        images = [image.img for image in project.images.all()]
        left, right = choose_random(images)
        context = {
                'Project': project,
                'progress': str(stage),
                'left_img': left,
                'right_img': right,
                'next': u'../../%s/rank/' % str(int(stage) + 1)
                }
        return render_to_response('rank.html',context)


def thanks(request, project_name):
	project =  Project.objects.get(name=project_name)
        context = {
                'Project': project,
                }
	return render_to_response('thanks.html',context)

def signin(request): 
	pass

def create_account(request):
	pass

def results(request, project_name):
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
