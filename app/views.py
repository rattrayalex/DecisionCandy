from django.shortcuts import render_to_response

def index(request):
	#Pass a list of projects, probably via get
	context = {
                'project_list':
                                (
                                        'smushkies','smushkies-6'
                                ),
##                                {
##                                        'smushkies-9':{ 'name':'smushkies', 'project_rankpage':'../../rank/', 'project_coverpic':'../../front-end/media/projects/smushkies-9/smushkies-9-02.png' },
##                                        'smushkies-6':{ 'project_rankpage':'../../rank/', 'project_coverpic':'../../front-end/media/projects/smushkies-6/smushkies-6-01.png' },
##                                        'bask-4':{ 'project_rankpage':'../../rank/', 'project_coverpic':'../../front-end/media/projects/bask-4/bask-4-11.png' },
##                                        'envirostickers':{ 'project_rankpage':'../../rank/', 'project_coverpic':'../../front-end/media/projects/envirostickers/UPSE Stickers-02.png' },
##                                        'envirostickers2':{ 'project_rankpage':'../../rank/', 'project_coverpic':'../../front-end/media/projects/envirostickers/UPSE Stickers-02.png' },
##                                        'thing1':'thing1',
##                                        'thing2':'thing2',
##                                        'thing3':'thing3'
##                                },
                'startrow':(1, 4, 7, 10, 13),
                'endrow':(3, 6, 9, 12)
                }
	return render_to_response('index.html', context)
	pass

def rank(request):
	#Pass a splitting attribute, two projects, project name / info,
	#progress, value, creator name
        context = {
                'criteria':'reminds you the most of yummy cookies',
                'more_criteria':'gourmet, classy, appealing',
                'creative':'Rattray Design Corp',
                'project_description':'Smushkies is a wonderful company started by Nicole Noel with the intent to reinvent the cookie.',
                'reward':'$0',
                'left_img':'../../front-end/media/projects/smushkies-9/smushkies-9-03.png',
                'right_img':'../../front-end/media/projects/smushkies-9/smushkies-9-02.png',
                'choose_left':'#',
                'choose_right':'../../thanks/',
                'choice_none':'../../choose/',
                'project_name':'Smushkies logo',
                'progress':'indeterminate progress'
                }
        return render_to_response('rank.html',context)
	pass

def thanks(request):
	#Needs to pass the name
	context = {
                'creative':'Rattray Design Corp',
                
                }
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
	context = {
                'project_list':
                                {
                                        'smushkies-9':{ 'project_rankpage':'../../rank/', 'project_coverpic':'../../front-end/media/projects/smushkies-9/smushkies-9-02.png' },
                                        'smushkies-6':{ 'project_rankpage':'../../rank/', 'project_coverpic':'../../front-end/media/projects/smushkies-6/smushkies-6-01.png' },
                                        'bask-4':{ 'project_rankpage':'../../rank/', 'project_coverpic':'../../front-end/media/projects/bask-4/bask-4-11.png' },
                                        'envirostickers':{ 'project_rankpage':'../../rank/', 'project_coverpic':'../../front-end/media/projects/envirostickers/UPSE Stickers-02.png' },
                                        'envirostickers':{ 'project_rankpage':'../../rank/', 'project_coverpic':'../../front-end/media/projects/envirostickers/UPSE Stickers-02.png' }
                                },
                'startrow':(1, 4, 7, 10, 13),
                'endrow':(3, 6, 9, 12)
                }
        return render_to_response('choose.html',context)
