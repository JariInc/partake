from django.contrib import admin
from partake.models import Car, CarClass, Track, RaceWeek, Season, Series

class SeasonAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'year', 'quarter', 'type')
	filter_horizontal = ('weeks',)
	list_filter = ['year', 'quarter']

class SeriesAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')
	filter_horizontal = ('seasons',)
	
class CarAdmin(admin.ModelAdmin):
	list_display = ('id', 'name',)

class TrackAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')

class RaceWeekAdmin(admin.ModelAdmin):
	list_display = ('num', 'track', 'carclass', 'drivers')
	

admin.site.register(Car, CarAdmin)
admin.site.register(CarClass)
admin.site.register(Track, TrackAdmin)
admin.site.register(RaceWeek, RaceWeekAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Series, SeriesAdmin)