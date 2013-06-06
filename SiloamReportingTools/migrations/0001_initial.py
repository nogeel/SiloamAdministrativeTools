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
            ('patient_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('SiloamReportingTools', ['Patient'])

        # Adding model 'PatientDemographics'
        db.create_table('SiloamReportingTools_patientdemographics', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('patient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.Patient'])),
            ('dob', self.gf('django.db.models.fields.DateField')()),
            ('ethnicity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.Ethnicity'])),
            ('homeland', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.Homeland'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.Language'])),
            ('visit_date', self.gf('django.db.models.fields.DateField')()),
            ('active_record', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('SiloamReportingTools', ['PatientDemographics'])

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
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('SiloamReportingTools', ['InsuranceType'])

        # Adding model 'Provider'
        db.create_table('SiloamReportingTools_provider', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('staff_provider', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('SiloamReportingTools', ['Provider'])

        # Adding model 'ProviderName'
        db.create_table('SiloamReportingTools_providername', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('provider_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.Provider'], null=True, blank=True)),
        ))
        db.send_create_signal('SiloamReportingTools', ['ProviderName'])

        # Adding model 'Visit'
        db.create_table('SiloamReportingTools_visit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('visit_date', self.gf('django.db.models.fields.DateField')()),
            ('visit_id', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('patient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.Patient'])),
            ('visit_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.VisitType'])),
            ('visit_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.VisitStatus'])),
            ('insurance_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.InsuranceType'], null=True, blank=True)),
            ('provider_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.ProviderName'])),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('SiloamReportingTools', ['Visit'])

        # Adding model 'EventType'
        db.create_table('SiloamReportingTools_eventtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('SiloamReportingTools', ['EventType'])

        # Adding model 'Event'
        db.create_table('SiloamReportingTools_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SiloamReportingTools.EventType'])),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('file_line', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('raw_data', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('SiloamReportingTools', ['Event'])


    def backwards(self, orm):
        # Deleting model 'Ethnicity'
        db.delete_table('SiloamReportingTools_ethnicity')

        # Deleting model 'Homeland'
        db.delete_table('SiloamReportingTools_homeland')

        # Deleting model 'Language'
        db.delete_table('SiloamReportingTools_language')

        # Deleting model 'Patient'
        db.delete_table('SiloamReportingTools_patient')

        # Deleting model 'PatientDemographics'
        db.delete_table('SiloamReportingTools_patientdemographics')

        # Deleting model 'VisitType'
        db.delete_table('SiloamReportingTools_visittype')

        # Deleting model 'VisitStatus'
        db.delete_table('SiloamReportingTools_visitstatus')

        # Deleting model 'InsuranceType'
        db.delete_table('SiloamReportingTools_insurancetype')

        # Deleting model 'Provider'
        db.delete_table('SiloamReportingTools_provider')

        # Deleting model 'ProviderName'
        db.delete_table('SiloamReportingTools_providername')

        # Deleting model 'Visit'
        db.delete_table('SiloamReportingTools_visit')

        # Deleting model 'EventType'
        db.delete_table('SiloamReportingTools_eventtype')

        # Deleting model 'Event'
        db.delete_table('SiloamReportingTools_event')


    models = {
        'SiloamReportingTools.ethnicity': {
            'Meta': {'ordering': "['ethnicity']", 'object_name': 'Ethnicity'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ethnicity': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'SiloamReportingTools.event': {
            'Meta': {'object_name': 'Event'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.EventType']"}),
            'file_line': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'raw_data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
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
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insurance_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
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
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'patient_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'SiloamReportingTools.patientdemographics': {
            'Meta': {'object_name': 'PatientDemographics'},
            'active_record': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'ethnicity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.Ethnicity']"}),
            'homeland': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.Homeland']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.Language']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.Patient']"}),
            'visit_date': ('django.db.models.fields.DateField', [], {})
        },
        'SiloamReportingTools.provider': {
            'Meta': {'object_name': 'Provider'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'staff_provider': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'SiloamReportingTools.providername': {
            'Meta': {'object_name': 'ProviderName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.Provider']", 'null': 'True', 'blank': 'True'}),
            'provider_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'SiloamReportingTools.visit': {
            'Meta': {'object_name': 'Visit'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insurance_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.InsuranceType']", 'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.Patient']"}),
            'provider_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.ProviderName']"}),
            'visit_date': ('django.db.models.fields.DateField', [], {}),
            'visit_id': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
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