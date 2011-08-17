from django.shortcuts import render_to_response
from DecisionCandy.app.models import *
import random

projects = [
                { 'name':'Smushkies 9', 'rankpage':'../../rank/', 'coverpic':'media/projects/smushkies-9/smushkies-9-02.png' },
                { 'name':'Smushkies 6', 'rankpage':'../../rank/', 'coverpic':'media/projects/smushkies-6/smushkies 6-01.png' },
                { 'name':'Bask', 'rankpage':'../../rank/', 'coverpic':'../../front-end/media/projects/bask-4/bask-4-11.png' },
                { 'name':'Envirostickers', 'rankpage':'../../rank/', 'coverpic':'../../front-end/media/projects/envirostickers/UPSE Stickers-02.png' },
                { 'name':'Envirostickers 2', 'rankpage':'../../rank/', 'coverpic':'../../front-end/media/projects/envirostickers/UPSE Stickers-02.png' },
                ]
projects = Project.objects.all()
startrows = [1, 4, 7, 10, 13]
endrows = [3, 6, 9, 12, 15]
other_stuff = {
        'left_img':'../../front-end/media/projects/smushkies-9/smushkies-9-03.png',
        'right_img':'../../front-end/media/projects/smushkies-9/smushkies-9-02.png',
        'choose_left':'#',
        'choose_right':'../../thanks/',
        'choice_none':'../../choose/',
        'project_name':'Smushkies logo',
        }
project_info = {
                'Project': {'criteria':'reminds you the most of yummy cookies',
                'more_criteria':'gourmet, classy, appealing',
                'creator':'Rattray Design Corp',
                'description':'Smushkies is a wonderful company started by Nicole Noel with the intent to reinvent the cookie.',
                'reward':'$0'
                            }        }
project_info = dict(project_info.items() + other_stuff.items())
def index(request):
	#Pass a list of projects, probably via get
        pics = Image.objects.all().order_by('project__name')[0]
        projects = Project.objects.all().order_by('name')
	context = {
                'project_list': projects,
                'pics':pics,
                'startrow':startrows,
                'endrow':endrows
                }
	return render_to_response('index.html', context)
	pass

def rank(request, project, stage): #(request, project, step)
	#Pass a splitting attribute, two projects, project name / info,
	#progress, value, creator name
        project =  Project.objects.get(name=project)
        stage = str(stage)
        context = {
                'Project': project,
                'progress': stage,
                }
        context = dict(context.items() + other_stuff.items())
        return render_to_response('rank.html',context)
	pass

def thanks(request, project): #(request, project)
	#Needs to pass the name
	project =  Project.objects.get(name=project)
        context = {
                'Project': project,
                }
        context = dict(context.items() + other_stuff.items())
	return render_to_response('thanks.html',context)
	pass

def signin(request): 
	pass

def create_account(request):
	pass

def style(request):
        return render_to_response('media/DC-style.css')

def choose(request):
        #Pass a list of projects, probably via get
        pics = Image.objects.all().order_by('project__name')[0]
        projects = Project.objects.all().order_by('name')
	context = {
                'project_list': projects,
                'pics':pics,
                'startrow':startrows,
                'endrow':endrows
                }
        return render_to_response('choose.html',context)

def results(request, project):
        project = str(project)
        ilq = Image.objects.filter(project__name=project)
        ilq = ilq.order_by('-votes_for')
        project = Project.objects.get(name=project)
        context = {
                'image_list': ilq,
                'project': project,
                'startrow':startrows,
                'endrow':endrows,
                
                }
        return render_to_response('results.html', context)
