#!/usr/bin/env python3

import os
import http.cookiejar
import urllib
import simplejson as json
import logging
import re
import datetime
import time

os.environ['DJANGO_SETTINGS_MODULE'] = 'partake.settings'

class iracingapi:
	def __init__(self):
		self.path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
		self.cookiejar = http.cookiejar.LWPCookieJar()
		
		try:
			self.cookiejar.load(self.path + "/.cookiejar", True, True)
		except:
			self.cookiejar.clear_session_cookies()
			
		self.delay = 0
		self.dlbytes = 0
		
	def download(self, url, params=None):
		
		time.sleep(self.delay*2)
		
		cookie_handler = urllib.request.HTTPCookieProcessor(self.cookiejar)
		opener = urllib.request.build_opener(cookie_handler)
		timer = time.perf_counter()
		try:
			if not params:
				response = opener.open(url)
			else:
				response = opener.open(url, urllib.parse.urlencode(params).encode('utf-8'))
		except urllib.error.HTTPError:
			logger.critical("HTTPError: %s", exc.code)
		except urllib.error.URLError:
			logger.critical("URLError: %s", exc.code)
		finally:
			self.delay = time.perf_counter() - timer
		
		data = response.read()
		self.dlbytes += len(data)
		
		return data

	def downloadJSON(self, url, params=None):
		# fix broken json
		tmp = re.sub('disabled', '"disabled"', self.download(url, params).decode("latin-1"))
		return json.loads(tmp)

	def connect(self):
		username = 'jari@ylimainen.fi'
		password = 'iHASw1n'
		
		logger.info("logging in...")
		
		if self.testCookie() == False:
			self.cookiejar.clear_session_cookies()
			params = {'username': username, 'password': password}
			self.download("https://members.iracing.com/membersite/Login", params)
			self.cookiejar.save(self.path + "/.cookiejar", True, True)
		
	def testCookie(self):
		try:
			data = self.downloadJSON("http://members.iracing.com/membersite/member/GetDriverStatus")
		except:
			return False
		return True

def addCar(d):
	c = Car(
			id = d["id"],
			name = urllib.parse.unquote_plus(d["name"])
		)
	c.save()
	logger.warning("Adding car %s", c.name)
	return c

def addCarClass(d):
	cc = CarClass(
			id = d["id"],
			name = urllib.parse.unquote_plus(d["name"])
		)
	cc.save()
	logger.warning("Adding class %s", cc.name)
	return cc

def addTrack(d):
	t = Track(
			id = d["id"],
			name = urllib.parse.unquote_plus(d["name"]),
			layout = urllib.parse.unquote_plus(d["config"])
		)
	t.save()
	logger.warning("Adding track %s %s", t.name, t.layout)
	return t

def addSeason(d):
	
	# length
	length = 0
	for track in d["tracks"]:
		length = max(length, track["raceweek"])
	
	# rookie season handling
	if len(d["rookieseason"]) > 0:
		length = 12
	
	# type
	if d["catid"] == 1:
		type = "o"
	elif d["catid"] == 2:
		type = "r"
	else:
		logger.error("Unknown type! (catid: %s)", d["catid"])
	
	if d["rookieseason"] != "B" and d["rookieseason"] != "C":
		s = Season(
				id = d["seasonid"],
				name = urllib.parse.unquote_plus(d["seasonshortname"]),
				type = type,
				length = length,
				year = d["year"],
				quarter = d["quarter"],
				minLicense = d["minlicenselevel"],
				maxLicense = d["maxlicenselevel"],
				start = datetime.date.fromtimestamp(d["start"]/1000),
				end = datetime.date.fromtimestamp(d["end"]/1000)
			)
		s.save()
		
		for cls in d["carclasses"]:
			s.classes.add(CarClass.objects.get(id=cls["id"]))
		s.save()
		
		ser = Series.objects.get(id=d["seriesid"])
		ser.seasons.add(s)
		
		logger.warning("Adding season %s", s.name)
		return s
	else:
		# rookie seasons fallback
		try:
			ser = Series.objects.get(id=d["seriesid"])
			return ser.seasons.get(year=d["year"], quarter=d["quarter"])
		except Series.DoesNotExist:
			logger.error("Did not found parent rookie series for seriesid %s", d["seriesid"])
			return None

def addSeries(d):
	s = Series(
			id = d["seriesid"],
			name = urllib.parse.unquote_plus(d["seriesname"])
		)
	s.save()
	logger.info("Adding series %s", s.name)
	return s

def getWeeklyDrivers(season, carclass, week):
	params = {
			'seasonid': season,
			'carclassid': carclass,
			'clubid': -1,
			'raceweek': week,
			'division': -1,
			'start': 1,
			'end': 1,
			'sort': 'points',
			'order': 'desc'
		}
		
	data = api.downloadJSON("http://members.iracing.com/memberstats/member/GetSeasonStandings", params)
		
	countkey = None
	
	for key in data["m"]:
		if data["m"][key] == "rowcount":
			countkey = key
	
	if countkey is not None:
		return data["d"][countkey];
	else:
		return 0

def rookieWeek(season, week):
	seasonmap = { 'A': 0, 'B': 1,	'C': 2 }
	return 4*seasonmap[season] + week

if __name__ == "__main__":
	from partake.models import *
	import datetime
	import pprint
	
	starttime = time.time()
	
	logger = logging.getLogger("iracingapi")
	logger.setLevel(logging.DEBUG)
	ch = logging.StreamHandler()
	ch.setLevel(logging.WARNING)
	formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
	ch.setFormatter(formatter)
	logger.addHandler(ch)
	
	api = iracingapi()
	api.connect()
	
	logger.info("Fetching season listing")
	series = api.download("http://members.iracing.com/membersite/member/SeriesStandings.do?season=1")
	
	p = re.compile(re.escape("var SeasonListing = extractJSON('") + '(.*)' + re.escape("')"))
	m = p.findall(series.decode("latin-1"))
	
	curyear = 0
	curquarter = 0
	
	if m:
		seasons = sorted(json.loads(m[1]), key=lambda k: k['seasonid'])
		
		#f = open('seasons.dict.txt', 'w+')
		#pprint.pprint(seasons, f)
		#f.close()
	
		for season in seasons:
			if season["year"] > curyear and season["quarter"] > curquarter:
				curyear = season["year"]
				curquarter = season["quarter"]
		
		for season in seasons:
			# skip unofficial
			if season["isOfficial"]:
				# series
				try:
					ser = Series.objects.get(id=season["seriesid"])
				except Series.DoesNotExist:
					ser = addSeries(season)
				
				# cars
				for car in season["cars"]:
					try:
						c = Car.objects.get(id=car["id"])
					except Car.DoesNotExist:
						c = addCar(car)
					
				# classes
				for carcls in season["carclasses"]:
					try:
						cc = CarClass.objects.get(id=carcls["id"])
					except CarClass.DoesNotExist:
						cc = addCarClass(carcls)
						for cars in carcls["carsinclass"]:
							cc.cars.add(Car.objects.get(id=cars["id"]))
						
				# tracks
				for track in season["tracks"]:
					try:
						t = Track.objects.get(id=track["id"])
					except Track.DoesNotExist:
						t = addTrack(track)
					
				# seasons
				try:
					ser = Series.objects.get(seasons__id=season["seasonid"])
					sea = Season.objects.get(id=season["seasonid"])
				except Series.DoesNotExist:
					sea = addSeason(season)
				
				# season driver total
				for cls in sea.classes.all():
					try:
						w = Season.objects.get(id=sea.id, weeks__num=-1, weeks__carclass=cls)
						curweek = w.weeks.filter(num=-1, carclass=cls).get()
						if not season["complete"] or (time.time() - season["end"]/1000) < 86400*2:
							tmp = curweek.drivers
							curweek.drivers = getWeeklyDrivers(sea.id, cls.id, -1)
							logger.info("Rechecking total drivers for season %s for %s (+%s)", sea.name, cls.name, (curweek.drivers-tmp))
							curweek.save()
					except Season.DoesNotExist:
						sea.weeks.create(
								num = -1,
								track = None,
								drivers = getWeeklyDrivers(sea.id, cls.id, -1),
								carclass = cls
							)
						logger.info("Adding total drivers to season %s for %s", sea.name, cls.name)
						
				# raceweeks
				lastweek = 0
				totalweeks = 0
				
				if len(season["rookieseason"]) > 0:
					totalweeks = 12
				else:
					for track in season["tracks"]:
						if track["raceweek"] + 1 > totalweeks:
							totalweeks = track["raceweek"] + 1
				
				for track in season["tracks"]:
					
					# offset between formats
					if len(season["rookieseason"]) > 0:
						week = rookieWeek(season["rookieseason"], track["raceweek"]) + 1
					else:
						week = track["raceweek"] + 1
						
					if week > lastweek:
						lastweek = week
						for cls in sea.classes.all():
							try:
								w = Season.objects.get(id=sea.id, weeks__num=week, weeks__carclass=cls)
								# get last week of last season and current seasons
								curweek = w.weeks.filter(num=week, carclass=cls).get()
								if (not season["complete"] and (week == season["raceweek"] or week == season["raceweek"]-1)) or (sea.year+(0.25*(sea.quarter-1)) == ((curyear+(0.25*(curquarter-1)))-0.25) and week == season["raceweek"] and (time.time() - season["end"]/1000) < 86400*14):
									tmp = curweek.drivers
									curweek.drivers = getWeeklyDrivers(sea.id, cls.id, track["raceweek"]+1)
									logger.info("Rechecking week %s to season %s for %s (+%s)", week, sea.name, cls.name, (curweek.drivers-tmp))
									curweek.save()
							except Season.DoesNotExist:
								sea.weeks.create(
										num = week,
										track = Track.objects.get(id=track["id"]),
										drivers = getWeeklyDrivers(sea.id, cls.id, track["raceweek"]+1),
										carclass = cls
									)								
								logger.info("Adding week %s to season %s for %s", week, sea.name, cls.name)
				
				sea.save()
				
	else:
		logger.critical('No match, something went horribly wrong')
	
	logger.info('Update finished in %s minutes, fetched %s kB', round((time.time()-starttime)/60), round(api.dlbytes/1024))
	
