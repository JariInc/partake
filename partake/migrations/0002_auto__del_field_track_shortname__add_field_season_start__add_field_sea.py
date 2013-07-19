# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Track.shortname'
        db.delete_column('partake_track', 'shortname')

        # Adding field 'Season.start'
        db.add_column('partake_season', 'start',
                      self.gf('django.db.models.fields.DateField')(blank=True, default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Season.end'
        db.add_column('partake_season', 'end',
                      self.gf('django.db.models.fields.DateField')(blank=True, default=datetime.datetime.now),
                      keep_default=False)

        # Deleting field 'Car.shortname'
        db.delete_column('partake_car', 'shortname')


    def backwards(self, orm):
        # Adding field 'Track.shortname'
        db.add_column('partake_track', 'shortname',
                      self.gf('django.db.models.fields.CharField')(blank=True, max_length=8, default=''),
                      keep_default=False)

        # Deleting field 'Season.start'
        db.delete_column('partake_season', 'start')

        # Deleting field 'Season.end'
        db.delete_column('partake_season', 'end')

        # Adding field 'Car.shortname'
        db.add_column('partake_car', 'shortname',
                      self.gf('django.db.models.fields.CharField')(blank=True, max_length=8, default=''),
                      keep_default=False)


    models = {
        'partake.car': {
            'Meta': {'object_name': 'Car'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'partake.carclass': {
            'Meta': {'object_name': 'CarClass'},
            'cars': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['partake.Car']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'partake.raceweek': {
            'Meta': {'object_name': 'RaceWeek'},
            'carclass': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['partake.CarClass']", 'unique': 'True'}),
            'drivers': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {}),
            'track': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['partake.Track']", 'unique': 'True'})
        },
        'partake.season': {
            'Meta': {'object_name': 'Season'},
            'classes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['partake.CarClass']", 'symmetrical': 'False'}),
            'end': ('django.db.models.fields.DateField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {}),
            'maxLicense': ('django.db.models.fields.IntegerField', [], {}),
            'minLicense': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'quarter': ('django.db.models.fields.IntegerField', [], {}),
            'start': ('django.db.models.fields.DateField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'weeks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['partake.RaceWeek']", 'symmetrical': 'False'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'partake.series': {
            'Meta': {'object_name': 'Series'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'seasons': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['partake.Season']", 'symmetrical': 'False'})
        },
        'partake.track': {
            'Meta': {'object_name': 'Track'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'layout': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '128'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['partake']