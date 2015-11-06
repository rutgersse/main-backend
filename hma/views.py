from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.dispatch import receiver
from django.db import models
from django.db.models import F, Q
from django.core.files.storage import default_storage as storage

import json

from hma.models import *

def get_exercise_data( location ):
	import random
	actlist=['Running', 'Swimming', 'Walking', 'Yoga', 'Gymnastics', 'Bicycling','Badminton']
	from random import randint

	l = []

	data = {}
	count = 0
	temp = []
	while(1):
		data = {}
		# x = randint(0,5)
		# data['activity'] = actlist[x]
		s = randint(0,6)
		if count == 5:
			break
		if s in temp:
			continue
		else:
			data['activity'] = actlist[s]
			data['population'] = randint(0, 1000)
			l.append(data)
			count = count + 1
			temp.append(s)


	print l

	with open('exercise.json', 'w') as f:
		f.write(json.dumps(l, indent=4))
		f.close()

	import os
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

	p = os.path.join(BASE_DIR, 'exercise.json')
	path = os.path.join(BASE_DIR, 'static/data/')
	print os.system('mv '+ p + ' ' + path)

def get_json_ldata( location_list ):
	"""
	Function for converting list to json data
	"""
	data = []
	for idx,location in enumerate( location_list ):
		temp = {
			'name' 			: location.get_name(),
			'url' 			: location.get_url(),
			'population' 	: location.get_population(),
			'type'			: location.get_location_type(),
			'tweet_count'	: location.tweet_count
		}
		# data[ str( idx ) ] = temp
		data.append(temp)
	return data

def get_json_adata( activity_list ):
	"""
	Function for converting list to json data
	"""
	data = []
	for idx,activity in enumerate( activity_list ):
		temp = {
			'name' 			: activity.get_name(),
			'url' 			: activity.get_url(),
			'type'			: activity.get_activity_type(),
			'hour'			: activity.get_hours(),
			'locations'		: activity.get_location_list(),
			'tweet_count'	: activity.tweet_count
		}
		# data[ str( idx ) ] = temp
		data.append(temp)
	return data

def get_individual_json_data( location ):
	"""
	Function for converting list to json data
	"""
	temp = {
		'name' 			: location.get_name(),
		'url' 			: location.get_url(),
		'population' 	: location.get_population(),
		'type'			: location.get_location_type()
	}
	# data[ str( idx ) ] = temp
	return temp

def index(request):
	"""
	Functiona Name : Index

	Args : request
	Return : index.html file
	"""
	return render( request, 'index.html', locals() )

def location_all(request):
	"""
	Functiona Name : location_all

	Args : request
	Return : index.html file
	"""
	location_list = Location.objects.all()
	data = get_json_ldata(location_list)
	jsondata = json.dumps(data, indent = 4)
	return HttpResponse( jsondata, content_type = 'application/json' )

def activity_all(request):
	"""
	Functiona Name : activity_all

	Args : request
	Return : index.html file
	"""
	activity_list = Activity.objects.all()
	data = get_json_adata(activity_list)
	jsondata = json.dumps(data, indent = 4)
	return HttpResponse( jsondata, content_type = 'application/json' )

def location( request, entity_slug ):
	"""
	Functiona Name : location

	Args : request, entity_slug
	Return : json data for individual location
	"""
	location = Location.objects.get( slug=entity_slug )
	get_exercise_data( location.name )
	# activity_list = location.activity.all()
	# data = get_individual_json_data( location )
	# jsondata = json.dumps( data, indent = 4 )
	# return HttpResponse( jsondata, content_type = 'application/json' )
	return render( request, 'location.html', locals() )

def activity(request):
	"""
	Functiona Name : activity

	Args : request, entity_slug
	Return : json data for individual activity
	"""
	activity = Activity.objects.get( slug=entity_slug )
	location_list = activity.location.all()
	data = get_individual_json_data( activity )
	jsondata = json.dumps( data, indent = 4 )
	return HttpResponse( jsondata, content_type = 'application/json' )

def leaderboard( request ):
	"""
	Functiona Name : leaderboard

	Args : request
	Return : leader board
	"""
	location_list = Location.objects.order_by('-tweet_count')[:10]
	return render( request, 'leaderboard.html', locals() )

def search( request ):
	"""
	Functiona Name : search

	Args : request
	Return : leader board
	"""
	# location_list = Location.objects.order_by('-tweet_count')[:10]
	return render( request, 'search.html', locals() )