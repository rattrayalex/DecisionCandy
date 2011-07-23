from django.shortcuts import render_to_response

def index(request):
	#Pass a list of projects, probably via get
	context = {}
	return render_to_response('index.html', context)
	pass

def rank(request):
	#Pass a splitting attribute, two projects, project name / info,
	#progress, value, creator name
        return render_to_response('rank.html')
	pass

def thanks(request):
	#Needs to pass the name
	context = {}
	return render_to_response('thanks.html',context)
	pass

def signin(request):
	pass

def create_account(request):
	pass

def style(request):
        return render_to_response('static/DC-style.css')

def choose(request):
        #Pass a list of projects, probably via get
	context = {}
        return render_to_response('choose.html',context)
