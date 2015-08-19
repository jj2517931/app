from django.shortcuts import render
from django.http import HttpResponse
from models import Video, Watched, Liked, Category, User_Category
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from data import categories

def home(request):
	if not request.user.is_authenticated():
		return redirect('login')

	available_categories = [x.category for x in User_Category.objects.filter(user = request.user)]

	unwatched_videos = [x for x in Video.objects.filter(category__in = available_categories).order_by('?') if not Watched.objects.filter(user = request.user, video = x)]

	if not unwatched_videos:
		return HttpResponse('We have run out of videos!!!')

	# video = Video.objects.filter(category__in = available_categories, ).order_by('?').first()

	video = unwatched_videos.pop()

	# while Watched.objects.filter(user = request.user, video = video):
	# 	video = Video.objects.filter(category_in = available_categories).order_by('?').first()

	Watched.objects.create(user = request.user, video = video)

	user_category_nums = [x.category_id for x in available_categories]

	return render(request, 'showmeyoutube/home.html', {'video': video, 'categories': categories, 'user': request.user, 'available_categories': user_category_nums})

def register(request):
	return render(request, 'showmeyoutube/register.html', {})

def registered(request):
	print 'registered!!!!!!'
	username = request.POST['username']
	email = request.POST['email']
	password = request.POST['password']
	new_user = User.objects.create_user(username =username,email=email,password=password)
	new_user.save()
	# for category in Category.objects.all():
	category = Category.objects.get(name = 'Pets & Animals')
	User_Category.objects.create(user = new_user, category = category)
	user = authenticate(username=username, password=password)
	# user.categories = (1,2,26)
	login(request, user)
	return redirect('home')

def login_(request):
	return render(request, 'showmeyoutube/login.html', {})

def logged_in(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user:
		login(request, user)
	
	return redirect('home')

def logout_(request):
	logout(request)
	return redirect('home')

def like(request):
	video_id = request.GET.get('id')
	video = Video.objects.get(video_id = video_id)
	if not Liked.objects.filter(video = video):
			Liked.objects.create(user = request.user, video = video)
	else:
		print 'Video already in database........'
	return HttpResponse()

def load_likes(request):

	array, qparams = load_videos(request, Liked)
	print qparams

	return render(request, 'showmeyoutube/likes.html', {'videos':array, 'query': "?likes/", 'qparams': qparams})

def load_history(request):

	array, qparams = load_videos(request, Watched)

	return render(request, 'showmeyoutube/likes.html', {'videos':array, 'query': "?history/", 'qparams': qparams})

def set_filters(request):

	return render(request, 'showmeyoutube/settings.html', {})
	
	# page = request.GET.get('page')

	# liked_videos = [like.video for like in Liked.objects.all() if like.user == request.user]

	# array = []
	# count = 0
	# group = []
	# for i in liked_videos:
	# 	group.append(i)
	# 	if len(group) == 3:
	# 		array.append(group)
	# 		group = []
	# if group:
	# 	array.append(group)



	# paginator = Paginator(array, 2)

	# try:
	# 	array = paginator.page(page)
	# except PageNotAnInteger:
	# 	# If page is not an integer, deliver first page.
	# 	array = paginator.page(1)
	# except EmptyPage:
	# 	# If page is out of range (e.g. 9999), deliver last page of results.
	# 	array = paginator.page(paginator.num_pages)

	# return render(request, 'showmeyoutube/likes.html', {'likes':array})

def load_videos(request, table):
	
	page = request.GET.get('page')

	search = request.GET.get('search') 

	videos = [x.video for x in table.objects.all() if x.user == request.user]

	qparams = ''

	if search:
		qparams += '&search=' + search
		videos = [x for x in videos if search.lower() in x.name.lower()]

	array = []
	count = 0
	group = []
	for i in videos:
		group.append(i)
		if len(group) == 3:
			array.append(group)
			group = []
	if group:
		array.append(group)



	paginator = Paginator(array, 2)

	try:
		array = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		array = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		array = paginator.page(paginator.num_pages)

	return array, qparams

def save_categories(request):
	print "SAving dem categories!!!!!"
	categories = request.GET.getlist('array[]')
	User_Category.objects.filter(user = request.user).delete()
	for i in categories:
		category = Category.objects.get(name = i)
		User_Category.objects.create(category = category, user = request.user)
	return HttpResponse()

# Create your views here.
