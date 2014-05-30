# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'OrganizationStats.races'
        db.add_column(u'tx_salaries_organizationstats', 'races',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)

        # Adding field 'OrganizationStats.female'
        db.add_column(u'tx_salaries_organizationstats', 'female',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)

        # Adding field 'OrganizationStats.male'
        db.add_column(u'tx_salaries_organizationstats', 'male',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)

        # Adding field 'OrganizationStats.time_employed'
        db.add_column(u'tx_salaries_organizationstats', 'time_employed',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)

        # Adding field 'EmployeeTitleStats.races'
        db.add_column(u'tx_salaries_employeetitlestats', 'races',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)

        # Adding field 'EmployeeTitleStats.female'
        db.add_column(u'tx_salaries_employeetitlestats', 'female',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)

        # Adding field 'EmployeeTitleStats.male'
        db.add_column(u'tx_salaries_employeetitlestats', 'male',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)

        # Adding field 'EmployeeTitleStats.time_employed'
        db.add_column(u'tx_salaries_employeetitlestats', 'time_employed',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)


        # Changing field 'Employee.title'
        db.alter_column(u'tx_salaries_employee', 'title_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['tx_salaries.EmployeeTitle']))
        # Adding field 'PositionStats.races'
        db.add_column(u'tx_salaries_positionstats', 'races',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)

        # Adding field 'PositionStats.female'
        db.add_column(u'tx_salaries_positionstats', 'female',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)

        # Adding field 'PositionStats.male'
        db.add_column(u'tx_salaries_positionstats', 'male',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)

        # Adding field 'PositionStats.time_employed'
        db.add_column(u'tx_salaries_positionstats', 'time_employed',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'OrganizationStats.races'
        db.delete_column(u'tx_salaries_organizationstats', 'races')

        # Deleting field 'OrganizationStats.female'
        db.delete_column(u'tx_salaries_organizationstats', 'female')

        # Deleting field 'OrganizationStats.male'
        db.delete_column(u'tx_salaries_organizationstats', 'male')

        # Deleting field 'OrganizationStats.time_employed'
        db.delete_column(u'tx_salaries_organizationstats', 'time_employed')

        # Deleting field 'EmployeeTitleStats.races'
        db.delete_column(u'tx_salaries_employeetitlestats', 'races')

        # Deleting field 'EmployeeTitleStats.female'
        db.delete_column(u'tx_salaries_employeetitlestats', 'female')

        # Deleting field 'EmployeeTitleStats.male'
        db.delete_column(u'tx_salaries_employeetitlestats', 'male')

        # Deleting field 'EmployeeTitleStats.time_employed'
        db.delete_column(u'tx_salaries_employeetitlestats', 'time_employed')


        # Changing field 'Employee.title'
        db.alter_column(u'tx_salaries_employee', 'title_id', self.gf('django.db.models.fields.related.ForeignKey')(default=False, to=orm['tx_salaries.EmployeeTitle']))
        # Deleting field 'PositionStats.races'
        db.delete_column(u'tx_salaries_positionstats', 'races')

        # Deleting field 'PositionStats.female'
        db.delete_column(u'tx_salaries_positionstats', 'female')

        # Deleting field 'PositionStats.male'
        db.delete_column(u'tx_salaries_positionstats', 'male')

        # Deleting field 'PositionStats.time_employed'
        db.delete_column(u'tx_salaries_positionstats', 'time_employed')


    models = {
        u'tx_people.contactdetail': {
            'Meta': {'object_name': 'ContactDetail'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sources': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'contact_detail'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.Source']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'tx_people.ethnicity': {
            'Meta': {'object_name': 'Ethnicity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'tx_people.identifier': {
            'Meta': {'object_name': 'Identifier'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'scheme': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'tx_people.link': {
            'Meta': {'object_name': 'Link'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'tx_people.membership': {
            'Meta': {'object_name': 'Membership'},
            'contact_details': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'memberships'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.ContactDetail']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'end_date': ('tx_people.fields.ReducedDateField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'links': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'memberships'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.Link']"}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'members'", 'to': u"orm['tx_people.Organization']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'to': u"orm['tx_people.Person']"}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'members'", 'null': 'True', 'to': u"orm['tx_people.Post']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'sources': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'memberships'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.Source']"}),
            'start_date': ('tx_people.fields.ReducedDateField', [], {'max_length': '10'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'tx_people.organization': {
            'Meta': {'object_name': 'Organization'},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'contact_details': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'organizations'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.ContactDetail']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'dissolution_date': ('tx_people.fields.ReducedDateField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'founding_date': ('tx_people.fields.ReducedDateField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifiers': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'organizations'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.Identifier']"}),
            'links': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'organizations'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.Link']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'other_name': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'organizations'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.OtherNames']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['tx_people.Organization']"}),
            'sources': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'organizations'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.Source']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'tx_people.othernames': {
            'Meta': {'object_name': 'OtherNames'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'tx_people.person': {
            'Meta': {'object_name': 'Person'},
            'additional_name': ('tx_people.fields.OptionalCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'biography': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'birth_date': ('tx_people.fields.OptionalReducedDateField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'contact_details': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'people'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.ContactDetail']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'death_date': ('tx_people.fields.OptionalReducedDateField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'email': ('tx_people.fields.OptionalCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'ethnicities': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'people'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.Ethnicity']"}),
            'family_name': ('tx_people.fields.OptionalCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'gender': ('tx_people.fields.OptionalCharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'given_name': ('tx_people.fields.OptionalCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'honorific_prefix': ('tx_people.fields.OptionalCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'honorific_suffix': ('tx_people.fields.OptionalCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifiers': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'people'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.Identifier']"}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'links': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'people'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.Link']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'organization': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'member'", 'symmetrical': 'False', 'through': u"orm['tx_people.Membership']", 'to': u"orm['tx_people.Organization']"}),
            'other_name': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'people'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.OtherNames']"}),
            'patronymic_name': ('tx_people.fields.OptionalCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'races': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'people'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.Race']"}),
            'sort_name': ('tx_people.fields.OptionalCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'sources': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'people'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.Source']"}),
            'summary': ('tx_people.fields.OptionalCharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'tx_people.post': {
            'Meta': {'object_name': 'Post'},
            'contact_details': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'posts'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.ContactDetail']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'end_date': ('tx_people.fields.ReducedDateField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'links': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'posts'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.Link']"}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': u"orm['tx_people.Organization']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'sources': ('tx_people.fields.OptionalManyToManyField', [], {'blank': 'True', 'related_name': "'posts'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tx_people.Source']"}),
            'start_date': ('tx_people.fields.ReducedDateField', [], {'max_length': '10'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'tx_people.race': {
            'Meta': {'object_name': 'Race'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'tx_people.source': {
            'Meta': {'object_name': 'Source'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'tx_salaries.compensationtype': {
            'Meta': {'object_name': 'CompensationType'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'tx_salaries.employee': {
            'Meta': {'object_name': 'Employee'},
            'compensation': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            'compensation_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tx_salaries.CompensationType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'end_date': ('tx_people.fields.ReducedDateField', [], {'max_length': '10'}),
            'hire_date': ('tx_people.fields.ReducedDateField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tx_people.Membership']"}),
            'start_date': ('tx_people.fields.ReducedDateField', [], {'max_length': '10'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'employees'", 'null': 'True', 'to': u"orm['tx_salaries.EmployeeTitle']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'tx_salaries.employeetitle': {
            'Meta': {'object_name': 'EmployeeTitle'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'tx_salaries.employeetitlestats': {
            'Meta': {'object_name': 'EmployeeTitleStats'},
            'female': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'highest_paid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'title_stats_highest'", 'null': 'True', 'to': u"orm['tx_salaries.Employee']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lowest_paid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'title_stats_lowest'", 'null': 'True', 'to': u"orm['tx_salaries.Employee']"}),
            'male': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'median_paid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'title_stats_median'", 'null': 'True', 'to': u"orm['tx_salaries.Employee']"}),
            'races': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'time_employed': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'title': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'stats'", 'unique': 'True', 'to': u"orm['tx_salaries.EmployeeTitle']"}),
            'total_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'tx_salaries.organizationstats': {
            'Meta': {'object_name': 'OrganizationStats'},
            'female': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'highest_paid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'organization_stats_highest'", 'null': 'True', 'to': u"orm['tx_salaries.Employee']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lowest_paid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'organization_stats_lowest'", 'null': 'True', 'to': u"orm['tx_salaries.Employee']"}),
            'male': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'median_paid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'organization_stats_median'", 'null': 'True', 'to': u"orm['tx_salaries.Employee']"}),
            'organization': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'stats'", 'unique': 'True', 'to': u"orm['tx_people.Organization']"}),
            'races': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'time_employed': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'total_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'tx_salaries.positionstats': {
            'Meta': {'object_name': 'PositionStats'},
            'female': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'highest_paid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'position_stats_highest'", 'null': 'True', 'to': u"orm['tx_salaries.Employee']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lowest_paid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'position_stats_lowest'", 'null': 'True', 'to': u"orm['tx_salaries.Employee']"}),
            'male': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'median_paid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'position_stats_median'", 'null': 'True', 'to': u"orm['tx_salaries.Employee']"}),
            'position': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'stats'", 'unique': 'True', 'to': u"orm['tx_people.Post']"}),
            'races': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'time_employed': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'total_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['tx_salaries']