from django.db import models
from django.db.models import Avg, Sum
from datetime import datetime

RACE_TYPE_CHOICES = (
	('r', 'road'),
	('o', 'oval'),
)

class Car(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=128)

	def __unicode__(self):
		return self.name

class CarClass(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=128)
	cars = models.ManyToManyField(Car)
	
	def __unicode__(self):
		return self.name
	
class Track(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=128)
	layout = models.CharField(max_length=128, blank=True)
	
	def __unicode__(self):
		return u'%s %s' % (self.name, self.layout)
	
class RaceWeek(models.Model):
	num = models.IntegerField()
	drivers = models.IntegerField()	
	track = models.ForeignKey(Track, blank=True, null=True)
	carclass = models.ForeignKey(CarClass)
	
	def __unicode__(self):
		return u'Week %s / %s' % (self.num, self.carclass.name)

class Season(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=128)
	type = models.CharField(max_length=1, choices=RACE_TYPE_CHOICES)
	classes = models.ManyToManyField(CarClass)
	weeks = models.ManyToManyField(RaceWeek)
	length = models.IntegerField()
	year = models.IntegerField()
	quarter = models.IntegerField()
	minLicense = models.IntegerField()
	maxLicense = models.IntegerField()
	start = models.DateField(default=datetime.now, blank=True)
	end = models.DateField(default=datetime.now, blank=True)
	
	def avgDrivers(self):
		avgs = []
		for cls in self.classes.all():
			average = self.weeks.filter(carclass=cls.id, drivers__gt=0).aggregate(Avg('drivers'))
			avgs.append(round(average['drivers__avg']))
		return avgs
	
	def totalDrivers(self):
		sums = []
		for cls in self.classes.all():
			total = self.weeks.get(carclass=cls.id, num=-1)
			sums.append({"id": cls.id, "name": cls.name, "sum": total.drivers})
		return sums
	
	def series(self):
		return Series.objects.get(seasons__id=self.id)
	
	def __unicode__(self):
		return u'%s %sS%s' % (self.name, self.year, self.quarter)

class Series(models.Model):
	id = models.IntegerField(primary_key=True)
	seasons = models.ManyToManyField(Season)
	name = models.CharField(max_length=128)
	
	def latestSeason(self):
		try:
			season = self.seasons.order_by('year', 'quarter').reverse()[0]
		except:
			season = None
		finally:
			return season
		#return self.seasons.order_by('year', 'quarter').reverse()[0]
	
	def allClasses(self):
		classes = {}
		for season in self.seasons.all():
			for cls in season.classes.all():
				classes[cls.id] = cls
		return list(classes.values())
	
	def __unicode__(self):
		return self.name
