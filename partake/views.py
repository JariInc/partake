from django.db.models import Sum
from django.shortcuts import render
from partake.models import *
from datetime import datetime

def frontpage(request):
	return render(request, 'frontpage.html', {'current_date': ""})

def seasonsPerQuarter(request, year=None, quarter=None):
	
	if not year or not quarter:
		ser = Series.objects.all().order_by('seasons__year', 'seasons__quarter').reverse()[0]
		sea = ser.latestSeason()
		year = sea.year
		quarter = sea.quarter
	
	seasons = Season.objects.filter(year=year, quarter=quarter).order_by('type', 'maxLicense')
	return render(request, 'seasons_per_quarter.html', {'seasons': seasons})

def singleSeries(request, id):
	series = Series.objects.get(id=id)
	return render(request, 'single_series.html', {'s': series})

def statistics(request):
	totaldrivers = {}
	populartracks = []
	drivercount = {}
	
	for serie in Series.objects.all():
		for season in serie.seasons.all():
			total = season.weeks.filter(num=-1).aggregate(Sum('drivers'))
			if str(season.year) + " Q" + str(season.quarter) in totaldrivers:
				totaldrivers[str(season.year) + " Q" + str(season.quarter)][season.type] += total['drivers__sum']
			else:
				totaldrivers[str(season.year) + " Q" + str(season.quarter)] = {"r": 0, "o": 0}
				totaldrivers[str(season.year) + " Q" + str(season.quarter)][season.type] = total['drivers__sum']
	
	return render(request, 'statistics.html', {
		'totaldrivers': totaldrivers
	})