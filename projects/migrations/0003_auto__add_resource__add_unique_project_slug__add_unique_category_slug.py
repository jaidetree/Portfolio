# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Resource'
        db.create_table('projects_resource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, unique=True, max_length=50, blank=True)),
        ))
        db.send_create_signal('projects', ['Resource'])

        # Adding M2M table for field resources on 'Project'
        db.create_table('projects_project_resources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['projects.project'], null=False)),
            ('resource', models.ForeignKey(orm['projects.resource'], null=False))
        ))
        db.create_unique('projects_project_resources', ['project_id', 'resource_id'])

        # Adding unique constraint on 'Project', fields ['slug']
        db.create_unique('projects_project', ['slug'])

        # Adding unique constraint on 'Category', fields ['slug']
        db.create_unique('projects_category', ['slug'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Category', fields ['slug']
        db.delete_unique('projects_category', ['slug'])

        # Removing unique constraint on 'Project', fields ['slug']
        db.delete_unique('projects_project', ['slug'])

        # Deleting model 'Resource'
        db.delete_table('projects_resource')

        # Removing M2M table for field resources on 'Project'
        db.delete_table('projects_project_resources')


    models = {
        'projects.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'resources': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['projects.Resource']", 'symmetrical': 'False'}),
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
