# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Model'
        db.create_table(u'models_model', (
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'models', ['Model'])

        # Adding model 'Field'
        db.create_table(u'models_field', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fields', to=orm['models.Model'])),
            ('field_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'models', ['Field'])

        # Adding unique constraint on 'Field', fields ['model', 'field_id']
        db.create_unique(u'models_field', ['model_id', 'field_id'])

        # Adding model 'ModelObject'
        db.create_table(u'models_modelobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['models.Model'])),
            ('values', self.gf('picklefield.fields.PickledObjectField')()),
        ))
        db.send_create_signal(u'models', ['ModelObject'])


    def backwards(self, orm):
        # Removing unique constraint on 'Field', fields ['model', 'field_id']
        db.delete_unique(u'models_field', ['model_id', 'field_id'])

        # Deleting model 'Model'
        db.delete_table(u'models_model')

        # Deleting model 'Field'
        db.delete_table(u'models_field')

        # Deleting model 'ModelObject'
        db.delete_table(u'models_modelobject')


    models = {
        u'models.field': {
            'Meta': {'unique_together': "(('model', 'field_id'),)", 'object_name': 'Field'},
            'field_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fields'", 'to': u"orm['models.Model']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        u'models.model': {
            'Meta': {'object_name': 'Model'},
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'models.modelobject': {
            'Meta': {'object_name': 'ModelObject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['models.Model']"}),
            'values': ('picklefield.fields.PickledObjectField', [], {})
        }
    }

    complete_apps = ['models']