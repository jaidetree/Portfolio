# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Project.side_notes'
        db.add_column('projects_project', 'side_notes', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Project.side_notes'
        db.delete_column('projects_project', 'side_notes')


    models = {
        'projects.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'projects.identity': {
            'Meta': {'object_name': 'Identity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'projects.project': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'Project'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': "orm['projects.Category']"}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_launched': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'html': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'null': 'True', 'to': "orm['projects.Identity']"}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'resources': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects'", 'symmetrical': 'False', 'to': "orm['projects.Resource']"}),
            'side_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'work_involved': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'projects.resource': {
            'Meta': {'object_name': 'Resource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['projects']
