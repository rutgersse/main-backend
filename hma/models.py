from django.db import models
from django.contrib.auth.models import User

from django.template.defaultfilters import slugify


class Location(models.Model):
	name 				= models.CharField( max_length=255 )
	slug 				= models.SlugField( unique = True, max_length = 255 )
	location_type 		= models.CharField( max_length=5, blank = True, null = True )
	population 			= models.IntegerField( default = 0 )
	last_update_time 	= models.DateTimeField( blank = True, null = True )
	# Activity 			= models.ManyToManyField( Activity, related_name='activities' )
	tweet_count			= models.IntegerField( default = 0 )
	hours 				= models.IntegerField( default = 0 )

	def __unicode__(self):
		return self.name

	def get_name(self):
		return self.name

	def get_slug(self):
		return self.slug

	def get_location_type(self):
		return self.location_type

	def get_population(self):
		return self.population

	def get_url(self):
		return '/location/' + self.slug + '/'





class Activity(models.Model):
	name 				= models.CharField( max_length=255 )
	slug 				= models.SlugField( unique = True, max_length = 255 )
	activity_type 		= models.CharField( max_length=5, blank = True, null = True )
	hours 				= models.IntegerField( blank = True, null = True )
	last_update_time	= models.DateTimeField( blank = True, null = True )
	relationships 		= models.ManyToManyField( Location, through = 'Relationship', symmetrical = False, related_name = 'related_to' )

	tweet_count			= models.IntegerField( default = 0 )

	def __unicode__(self):
		return self.name

	def get_name(self):
		return self.name

	def get_slug(self):
		return self.slug

	def get_activity_type(self):
		return self.activity_type

	# def get_population(self):
	# 	return self.population
	def get_hours(self):
		return self.hours

	def get_location_list(self):
		return self.Location.name

	def get_url(self):
		return '/location/' + self.slug + '/'

# def user_pic(instance, filename):
# 	ext = filename.split('.')[-1]
# 	if not ext:
# 		ext = 'jpg'
# 	image_name = instance.username
# 	return 'user/' + image_name + '.' + ext

# class User(models.Model):
# 	user  				= models.OneToOneField( User )
# 	username			= models.CharField( max_length = 50, blank = True, null = True )
# 	name 				= models.CharField( max_length = 255 )
# 	# profile_pic			= models.ImageField( blank = True, null = True, upload_to = user_pic )
# 	location 			= models.OneToOneField( Location )
# 	activities 			= models.ManyToManyField( Activity, related_name='actor' )
# 	last_update_time	= models.DateTimeField()
# 	time_stamp			= models.DateTimeField()

class Relationship(models.Model):
    location = models.ForeignKey(Location, related_name='location')
    activity = models.ForeignKey(Activity, related_name='activity')

    def rel_name(self):
    	return str(self.location) + ' has ' + str(self.activity)

class Mood(models.Model):
	location 			= models.ManyToManyField( Location, related_name = 'moods' )
	activity 			= models.ManyToManyField( Activity, related_name = 'moods' )
	mood_type 			= models.CharField( max_length = 255 )
	mood_value 			= models.IntegerField( blank = True, null = True )

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

