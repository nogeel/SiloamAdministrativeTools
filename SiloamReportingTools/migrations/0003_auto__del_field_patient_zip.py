# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Patient.zip'
        db.delete_column('SiloamReportingTools_patient', 'zip')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Patient.zip'
        raise RuntimeError("Cannot reverse this migration. 'Patient.zip' and its values cannot be restored.")

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
            'active_record': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'ethnicity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.Ethnicity']"}),
            'homeland': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.Homeland']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SiloamReportingTools.Language']"}),
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