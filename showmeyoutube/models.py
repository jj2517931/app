from django.db import models
import praw
import re
from apiclient.discovery import build
from django.contrib.auth.models import User
from data import categories

DEVELOPER_KEY = "AIzaSyAyxgg8M20ahh54LLYPfNUbl1PDNjW6irs"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class Category(models.Model):
	category_id = models.IntegerField()
	name = models.TextField()

class Video(models.Model):
	name = models.TextField()
	video_id = models.TextField()
	category = models.ForeignKey(Category)
	url = models.TextField()
	thumbnail = models.TextField()

class Watched(models.Model):
	user = models.ForeignKey(User)
	video = models.ForeignKey(Video)

class Liked(models.Model):
	user = models.ForeignKey(User)
	video = models.ForeignKey(Video)


class User_Category(models.Model):
	user = models.ForeignKey(User)
	category = models.ForeignKey(Category)

def find_videos(num):

	r = praw.Reddit(user_agent='my_cool_application')
	submissions = r.get_subreddit('videos').get_top_from_all(limit=num)
	id_list = [re.search('v=([A-Za-z0-9\-]+)', x.url).groups()[0] for x in submissions if re.search('v=([A-Za-z0-9\-]+)',x.url)]
	return id_list
	#Video.objects.create()

def retrieve_video_info(video_id, youtube):
	video_info = youtube.videos().list(
	part = 'snippet',
	id = video_id, 
	).execute()

	try:
		category_id = video_info['items'][0]['snippet']['categoryId']
		title = video_info['items'][0]['snippet']['title']
	except:
		category_id, title = (None, None)
	return title, category_id

def setup_youtube_connection():
	return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  developerKey=DEVELOPER_KEY)

def add_videos(num):
	youtube = setup_youtube_connection()
	id_list = find_videos(int(num))
	for id in id_list:
		title, category_id = retrieve_video_info(id, youtube)
		if category_id == None or title == None:
			continue
		video_url = "http://www.youtube.com/embed/" + id + "?autoplay=1"
		thumbnail = "http://img.youtube.com/vi/" + id + "/0.jpg"
		category = Category.objects.filter(category_id = category_id)[0]
		print category.name
		if not Video.objects.filter(video_id = id):
			Video.objects.create(name = title, video_id = id, category = category, url = video_url, thumbnail = thumbnail)
		else:
			print 'Video already in database........'

# def add_categories():
# 	for i in categories:
# 		Category.objects.create(category_id = i, name = categories[i])


