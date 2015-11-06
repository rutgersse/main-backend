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
			'type'			: location.get_location_type()
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
			'locations'		: activity.get_location_list()
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
	activity_list = location.activity.all()
	data = get_individual_json_data( location )
	jsondata = json.dumps( data, indent = 4 )
	return HttpResponse( jsondata, content_type = 'application/json' )

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