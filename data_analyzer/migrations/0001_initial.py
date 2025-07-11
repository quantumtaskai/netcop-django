# Generated by Django 5.2.4 on 2025-07-10 04:09

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agent_base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DataAnalysisAgentRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('processed_at', models.DateTimeField(blank=True, null=True)),
                ('data_file', models.FileField(blank=True, upload_to='uploads/data_analyzer/')),
                ('analysis_type', models.CharField(choices=[('summary', 'Summary Analysis'), ('detailed', 'Detailed Analysis'), ('statistical', 'Statistical Analysis')], default='summary', max_length=50)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent_base.baseagent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Data Analysis Agent Request',
                'verbose_name_plural': 'Data Analysis Agent Requests',
                'db_table': 'data_analyzer_requests',
            },
        ),
        migrations.CreateModel(
            name='DataAnalysisAgentResponse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('success', models.BooleanField(default=False)),
                ('error_message', models.TextField(blank=True)),
                ('processing_time', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('analysis_results', models.JSONField(blank=True, default=dict)),
                ('insights_summary', models.TextField(blank=True)),
                ('report_text', models.TextField(blank=True)),
                ('raw_response', models.JSONField(blank=True, default=dict)),
                ('request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='response', to='data_analyzer.dataanalysisagentrequest')),
            ],
            options={
                'verbose_name': 'Data Analysis Agent Response',
                'verbose_name_plural': 'Data Analysis Agent Responses',
                'db_table': 'data_analyzer_responses',
            },
        ),
    ]
