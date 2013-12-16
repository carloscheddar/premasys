# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'common_user', (
            ('UserID', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('Username', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('perm', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'common', ['User'])

        # Adding model 'Course'
        db.create_table(u'common_course', (
            ('CourseName', self.gf('django.db.models.fields.CharField')(max_length=260)),
            ('CourseID', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
        ))
        db.send_create_signal(u'common', ['Course'])

        # Adding model 'User_Course'
        db.create_table(u'common_user_course', (
            ('Prof_CourID', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('UserID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.User'])),
            ('CourseID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Course'])),
        ))
        db.send_create_signal(u'common', ['User_Course'])

        # Adding model 'Lessons'
        db.create_table(u'common_lessons', (
            ('LessonID', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('CourseID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Course'])),
            ('Title', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'common', ['Lessons'])

        # Adding model 'Slides'
        db.create_table(u'common_slides', (
            ('SlideID', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('Number', self.gf('django.db.models.fields.BigIntegerField')()),
            ('Data', self.gf('django.db.models.fields.TextField')()),
            ('LessonID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Lessons'])),
        ))
        db.send_create_signal(u'common', ['Slides'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'common_user')

        # Deleting model 'Course'
        db.delete_table(u'common_course')

        # Deleting model 'User_Course'
        db.delete_table(u'common_user_course')

        # Deleting model 'Lessons'
        db.delete_table(u'common_lessons')

        # Deleting model 'Slides'
        db.delete_table(u'common_slides')


    models = {
        u'common.course': {
            'CourseID': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'CourseName': ('django.db.models.fields.CharField', [], {'max_length': '260'}),
            'Meta': {'object_name': 'Course'}
        },
        u'common.lessons': {
            'CourseID': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Course']"}),
            'LessonID': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'Lessons'},
            'Title': ('django.db.models.fields.TextField', [], {})
        },
        u'common.slides': {
            'Data': ('django.db.models.fields.TextField', [], {}),
            'LessonID': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Lessons']"}),
            'Meta': {'object_name': 'Slides'},
            'Number': ('django.db.models.fields.BigIntegerField', [], {}),
            'SlideID': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'})
        },
        u'common.user': {
            'Meta': {'object_name': 'User'},
            'UserID': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'Username': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'perm': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'common.user_course': {
            'CourseID': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Course']"}),
            'Meta': {'object_name': 'User_Course'},
            'Prof_CourID': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'UserID': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.User']"})
        }
    }

    complete_apps = ['common']