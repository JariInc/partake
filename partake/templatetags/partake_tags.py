from operator import itemgetter
from django import template
from partake.models import *

register = template.Library()

def driver_avg(weeks):
	l = []
	for week in weeks:
		if week.drivers > 0:
			l.append(week.drivers)
	
	if len(l) > 0:
		return round(sum(l) / float(len(l)))
	else:
		return 0

def acronize(str):
	if not str:
		return ""
	
	words = str.split(' ')
	
	if len(words) > 1:
		acronym = ""
		for word in words:
			acronym = acronym + word[0]
		return acronym
	else:
		return str[0:4]

def quarter_menu():
	#seasons = Season.objects.all() #.distinct('quarter', 'year')
	seasons = Season.objects.distinct('quarter', 'year')
	quarters = []
	for season in seasons:
		quarters.append({'year': season.year, 'quarter': season.quarter})
	quarters = sorted(quarters, key=itemgetter('year'))
	return {'quarters': quarters}

def series_menu():
	series = Series.objects.all().order_by('name')
	result = []
	for serie in series:
		result.append({'id': serie.id, 'name': serie.name})
	return {'series': result}

register.filter('driver_avg', driver_avg)
register.filter('acronize', acronize)

register.inclusion_tag('quarter_menu.html')(quarter_menu)
register.inclusion_tag('series_menu.html')(series_menu)
