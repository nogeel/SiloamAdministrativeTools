# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EventType'
        db.create_table('SiloamReportingTools_eventtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('SiloamReportingTools', ['EventType'])

        # Adding model 'Events'
        db.create_table('SiloamReportingTools_events', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.EventType'])),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('file_line', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('raw_data', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('SiloamReportingTools', ['Events'])

        # Adding field 'Patient.last_visit'
        db.add_column('SiloamReportingTools_patient', 'last_visit',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(1900, 1, 1, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'EventType'
        db.delete_table('SiloamReportingTools_eventtype')

        # Deleting model 'Events'
        db.delete_table('SiloamReportingTools_events')

        # Deleting field 'Patient.last_visit'
        db.delete_column('SiloamReportingTools_patient', 'last_visit')


    models = {
        'SiloamReportingTools.ethnicity': {
            'Meta': {'ordering': "['ethnicity']", 'object_name': 'Ethnicity'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ethnicity': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'SiloamReportingTools.events': {
            'Meta': {'object_name': 'Events'},
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.EventType']"}),
            'file_line': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'raw_data': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'SiloamReportingTools.eventtype': {
            'Meta': {'object_name': 'EventType'},
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'SiloamReportingTools.homeland': {
            'Meta': {'ordering': "['homeland']", 'object_name': 'Homeland'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'homeland': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'SiloamReportingTools.insurancetype': {
            'Meta': {'object_name': 'InsuranceType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insurance_type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'SiloamReportingTools.language': {
            'Meta': {'ordering': "['language']", 'object_name': 'Language'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'SiloamReportingTools.patient': {
            'Meta': {'object_name': 'Patient'},
            'active_record': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'ethnicity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.Ethnicity']"}),
            'homeland': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.Homeland']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.Language']"}),
            'last_visit': ('django.db.models.fields.DateField', [], {}),
            'patient_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'SiloamReportingTools.visit': {
            'Meta': {'object_name': 'Visit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insurance_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.InsuranceType']"}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.Patient']"}),
            'visit_id': ('django.db.models.fields.IntegerField', [], {}),
            'visit_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.VisitStatus']"}),
            'visit_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.VisitType']"})
        },
        'SiloamReportingTools.visitstatus': {
            'Meta': {'object_name': 'VisitStatus'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'visit_status': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'SiloamReportingTools.visittype': {
            'Meta': {'object_name': 'VisitType'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'visit_type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['SiloamReportingTools']