from django.shortcuts import render, redirect

def index_view(request):
	args = {}
	args['current_page'] = 'index'
	return render(request, 'index.html', args)

def login(request):
	## Log the user in
	# Need the login form
	return indexview(request)

def home_view(request):
	args = {}
	args['current_page'] = 'home'
	return render(request, 'home.html', args)

def classify_view(request):
	args = {}
	args['current_page'] = 'classify'
	return render(request, 'classify.html', args)

def extract_view(request):
	args = {}
	args['current_page'] = 'extract'
	return render(request, 'extract.html', args)

