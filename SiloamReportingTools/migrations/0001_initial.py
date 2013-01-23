# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ethnicity'
        db.create_table('SiloamReportingTools_ethnicity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ethnicity', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('SiloamReportingTools', ['Ethnicity'])

        # Adding model 'Homeland'
        db.create_table('SiloamReportingTools_homeland', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('homeland', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('SiloamReportingTools', ['Homeland'])

        # Adding model 'Language'
        db.create_table('SiloamReportingTools_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('SiloamReportingTools', ['Language'])

        # Adding model 'Patient'
        db.create_table('SiloamReportingTools_patient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('patient_id', self.gf('django.db.models.fields.IntegerField')()),
            ('dob', self.gf('django.db.models.fields.DateField')()),
            ('ethnicity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.Ethnicity'])),
            ('homeland', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.Homeland'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.Language'])),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('SiloamReportingTools', ['Patient'])

        # Adding model 'VisitType'
        db.create_table('SiloamReportingTools_visittype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('visit_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('SiloamReportingTools', ['VisitType'])

        # Adding model 'VisitStatus'
        db.create_table('SiloamReportingTools_visitstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('visit_status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('SiloamReportingTools', ['VisitStatus'])

        # Adding model 'InsuranceType'
        db.create_table('SiloamReportingTools_insurancetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('insurance_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('SiloamReportingTools', ['InsuranceType'])

        # Adding model 'Visit'
        db.create_table('SiloamReportingTools_visit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('visit_id', self.gf('django.db.models.fields.IntegerField')()),
            ('patient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.Patient'])),
            ('visit_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.VisitType'])),
            ('visit_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.VisitStatus'])),
            ('insurance_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.InsuranceType'])),
        ))
        db.send_create_signal('SiloamReportingTools', ['Visit'])


    def backwards(self, orm):
        # Deleting model 'Ethnicity'
        db.delete_table('SiloamReportingTools_ethnicity')

        # Deleting model 'Homeland'
        db.delete_table('SiloamReportingTools_homeland')

        # Deleting model 'Language'
        db.delete_table('SiloamReportingTools_language')

        # Deleting model 'Patient'
        db.delete_table('SiloamReportingTools_patient')

        # Deleting model 'VisitType'
        db.delete_table('SiloamReportingTools_visittype')

        # Deleting model 'VisitStatus'
        db.delete_table('SiloamReportingTools_visitstatus')

        # Deleting model 'InsuranceType'
        db.delete_table('SiloamReportingTools_insurancetype')

        # Deleting model 'Visit'
        db.delete_table('SiloamReportingTools_visit')


    models = {
        'SiloamReportingTools.ethnicity': {
            'Meta': {'object_name': 'Ethnicity'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ethnicity': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'SiloamReportingTools.homeland': {
            'Meta': {'object_name': 'Homeland'},
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
            'Meta': {'object_name': 'Language'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'SiloamReportingTools.patient': {
            'Meta': {'object_name': 'Patient'},
            'dob': ('django.db.models.fields.DateField', [], {}),
            'ethnicity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.Ethnicity']"}),
            'homeland': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.Homeland']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.Language']"}),
            'patient_id': ('django.db.models.fields.IntegerField', [], {}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '10'})
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