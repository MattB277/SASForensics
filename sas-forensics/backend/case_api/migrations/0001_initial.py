# Generated by Django 4.2.18 on 2025-01-25 04:05

import case_api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('case_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('case_number', models.CharField(max_length=20, unique=True)),
                ('crime_type', models.CharField(max_length=255)),
                ('date_opened', models.DateTimeField()),
                ('last_updated', models.DateTimeField()),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('new_evidence', 'New Evidence'), ('new_collaboration', 'New Collaboration'), ('no_changes', 'No Changes')], default='no_changes', max_length=20)),
                ('assigned_users', models.ManyToManyField(blank=True, related_name='assigned_cases', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_cases', to=settings.AUTH_USER_MODEL)),
                ('related_cases', models.ManyToManyField(blank=True, related_name='referenced_cases', to='case_api.case')),
                ('reviewers', models.ManyToManyField(blank=True, related_name='case_reviewers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='case_api/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserCaseAccessRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_accessed', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('New Evidence', 'New Evidence'), ('Updated Information', 'Updated Information'), ('No changes', 'No changes')], max_length=50)),
                ('case_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='case_access_records', to='case_api.case')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='case_access_records', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('file_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('file', models.FileField(upload_to=case_api.models.upload_to_based_on_type)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('file_type', models.CharField(blank=True, choices=[('pdf', 'pdf'), ('mp4', 'mp4'), ('jpeg', 'jpeg'), ('docx', 'docx')], max_length=20)),
                ('case_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files', to='case_api.case')),
            ],
        ),
        migrations.CreateModel(
            name='DocChangelog',
            fields=[
                ('change_id', models.AutoField(primary_key=True, serialize=False)),
                ('change_date', models.DateTimeField(auto_now=True)),
                ('change_details', models.CharField(max_length=70)),
                ('change_author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('file_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_changelog_record', to='case_api.file')),
            ],
        ),
        migrations.CreateModel(
            name='CaseChangelog',
            fields=[
                ('change_id', models.AutoField(primary_key=True, serialize=False)),
                ('change_date', models.DateTimeField(auto_now=True)),
                ('change_details', models.CharField(max_length=70)),
                ('type_of_change', models.CharField(choices=[('Added Evidence', 'Added Evidence'), ('Updated Information', 'Updated Information'), ('Assigned Detective', 'Assigned Detective'), ('Assigned Reviewer', 'Assigned Reviewer'), ('Created Connection', 'Created Connection'), ('Created Case', 'Created Case')], max_length=50)),
                ('case_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='case_changelog_record', to='case_api.case')),
                ('change_author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AnalysedDocs',
            fields=[
                ('Analysis_id', models.AutoField(primary_key=True, serialize=False)),
                ('JSON_file', models.FilePathField()),
                ('case_number', models.CharField(blank=True, max_length=20)),
                ('file_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='analysed_document', to='case_api.file')),
            ],
        ),
    ]
