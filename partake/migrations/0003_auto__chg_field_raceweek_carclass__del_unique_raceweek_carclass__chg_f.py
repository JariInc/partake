# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'RaceWeek', fields ['track']
        db.delete_unique('partake_raceweek', ['track_id'])

        # Removing unique constraint on 'RaceWeek', fields ['carclass']
        db.delete_unique('partake_raceweek', ['carclass_id'])


        # Changing field 'RaceWeek.carclass'
        db.alter_column('partake_raceweek', 'carclass_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['partake.CarClass']))

        # Changing field 'RaceWeek.track'
        db.alter_column('partake_raceweek', 'track_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['partake.Track']))

    def backwards(self, orm):

        # Changing field 'RaceWeek.carclass'
        db.alter_column('partake_raceweek', 'carclass_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['partake.CarClass']))
        # Adding unique constraint on 'RaceWeek', fields ['carclass']
        db.create_unique('partake_raceweek', ['carclass_id'])


        # Changing field 'RaceWeek.track'
        db.alter_column('partake_raceweek', 'track_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['partake.Track']))
        # Adding unique constraint on 'RaceWeek', fields ['track']
        db.create_unique('partake_raceweek', ['track_id'])


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
            'carclass': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['partake.CarClass']"}),
            'drivers': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['partake.Track']"})
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