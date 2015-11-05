from django.db import models
from django.contrib.auth.models import User

from django.template.defaultfilters import slugify


class Location(models.Model):
	name 				= models.CharField( max_length=255 )
	slug 				= models.SlugField( unique = True, max_length = 255 )
	location_type 		= models.CharField( max_length=5 )
	population 			= models.IntegerField()
	last_update_time 	= models.DateTimeField()


class Activity(models.Model):
	name 				= models.CharField( max_length=255 )
	slug 				= models.SlugField( unique = True, max_length = 255 )
	activity_type 		= models.CharField( max_length=5 )
	hours 				= models.IntegerField()
	last_update_time	= models.DateTimeField()
	Location 			= models.ForeignKey( Location, related_name='locations' )


def user_pic(instance, filename):
	ext = filename.split('.')[-1]
	if not ext:
		ext = 'jpg'
	image_name = instance.username
	return 'user/' + image_name + '.' + ext

class User(models.Model):
	user  				= models.OneToOneField( User )
	username			= models.CharField( max_length = 50, blank = True, null = True )
	name 				= models.CharField( max_length = 255 )
	profile_pic			= models.ImageField( blank = True, null = True, upload_to = user_pic )
	location 			= models.OneToOneField( Location )
	activities 			= models.ManyToManyField( Activity, related_name='actor' )
	last_update_time	= models.DateTimeField()
	time_stamp			= models.DateTimeField()

class Mood(models.Model):
	location 			= models.ManyToManyField( Location, related_name = 'moods' )
	activity 			= models.ManyToManyField( Activity, related_name = 'moods' )
	mood_type 			= models.CharField( max_length = 255 )
	mood_value 			= models.IntegerField()

class Log(models.Model):
	creator 			= models.ForeignKey( User, related_name = 'created_exercise' )
	added_exercise 		= models.CharField( max_length = 255 )
	time_stamp			= models.DateTimeField()
	verified 			= models.BooleanField( default = False )

class Tweet(models.Model):
	tweet_id 			= models.CharField(max_length=255)
	locations 			= models.ManyToManyField( Location, related_name = 'tweets' )
	activities 			= models.ManyToManyField( Activity, related_name = 'tweets' )
	moods 				= models.ManyToManyField( Mood, related_name = 'tweets' )

