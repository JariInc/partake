# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Car'
        db.create_table('partake_car', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('shortname', self.gf('django.db.models.fields.CharField')(blank=True, max_length=8)),
        ))
        db.send_create_signal('partake', ['Car'])

        # Adding model 'CarClass'
        db.create_table('partake_carclass', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('partake', ['CarClass'])

        # Adding M2M table for field cars on 'CarClass'
        m2m_table_name = db.shorten_name('partake_carclass_cars')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('carclass', models.ForeignKey(orm['partake.carclass'], null=False)),
            ('car', models.ForeignKey(orm['partake.car'], null=False))
        ))
        db.create_unique(m2m_table_name, ['carclass_id', 'car_id'])

        # Adding model 'Track'
        db.create_table('partake_track', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('layout', self.gf('django.db.models.fields.CharField')(blank=True, max_length=128)),
            ('shortname', self.gf('django.db.models.fields.CharField')(blank=True, max_length=8)),
        ))
        db.send_create_signal('partake', ['Track'])

        # Adding model 'RaceWeek'
        db.create_table('partake_raceweek', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num', self.gf('django.db.models.fields.IntegerField')()),
            ('drivers', self.gf('django.db.models.fields.IntegerField')()),
            ('track', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['partake.Track'], unique=True)),
            ('carclass', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['partake.CarClass'], unique=True)),
        ))
        db.send_create_signal('partake', ['RaceWeek'])

        # Adding model 'Season'
        db.create_table('partake_season', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('length', self.gf('django.db.models.fields.IntegerField')()),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('quarter', self.gf('django.db.models.fields.IntegerField')()),
            ('minLicense', self.gf('django.db.models.fields.IntegerField')()),
            ('maxLicense', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('partake', ['Season'])

        # Adding M2M table for field classes on 'Season'
        m2m_table_name = db.shorten_name('partake_season_classes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('season', models.ForeignKey(orm['partake.season'], null=False)),
            ('carclass', models.ForeignKey(orm['partake.carclass'], null=False))
        ))
        db.create_unique(m2m_table_name, ['season_id', 'carclass_id'])

        # Adding M2M table for field weeks on 'Season'
        m2m_table_name = db.shorten_name('partake_season_weeks')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('season', models.ForeignKey(orm['partake.season'], null=False)),
            ('raceweek', models.ForeignKey(orm['partake.raceweek'], null=False))
        ))
        db.create_unique(m2m_table_name, ['season_id', 'raceweek_id'])

        # Adding model 'Series'
        db.create_table('partake_series', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('partake', ['Series'])

        # Adding M2M table for field seasons on 'Series'
        m2m_table_name = db.shorten_name('partake_series_seasons')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('series', models.ForeignKey(orm['partake.series'], null=False)),
            ('season', models.ForeignKey(orm['partake.season'], null=False))
        ))
        db.create_unique(m2m_table_name, ['series_id', 'season_id'])


    def backwards(self, orm):
        # Deleting model 'Car'
        db.delete_table('partake_car')

        # Deleting model 'CarClass'
        db.delete_table('partake_carclass')

        # Removing M2M table for field cars on 'CarClass'
        db.delete_table(db.shorten_name('partake_carclass_cars'))

        # Deleting model 'Track'
        db.delete_table('partake_track')

        # Deleting model 'RaceWeek'
        db.delete_table('partake_raceweek')

        # Deleting model 'Season'
        db.delete_table('partake_season')

        # Removing M2M table for field classes on 'Season'
        db.delete_table(db.shorten_name('partake_season_classes'))

        # Removing M2M table for field weeks on 'Season'
        db.delete_table(db.shorten_name('partake_season_weeks'))

        # Deleting model 'Series'
        db.delete_table('partake_series')

        # Removing M2M table for field seasons on 'Series'
        db.delete_table(db.shorten_name('partake_series_seasons'))


    models = {
        'partake.car': {
            'Meta': {'object_name': 'Car'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'shortname': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '8'})
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
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {}),
            'maxLicense': ('django.db.models.fields.IntegerField', [], {}),
            'minLicense': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'quarter': ('django.db.models.fields.IntegerField', [], {}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'shortname': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '8'})
        }
    }

    complete_apps = ['partake']