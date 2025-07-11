# Generated by Django 5.2.4 on 2025-07-09 13:24

import uuid
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseAgent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('analytics', 'Analytics'), ('utilities', 'Utilities'), ('content', 'Content'), ('marketing', 'Marketing'), ('customer-service', 'Customer Service')], max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('icon', models.CharField(default='🤖', max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('rating', models.DecimalField(decimal_places=1, default=Decimal('4.5'), max_digits=3)),
                ('review_count', models.IntegerField(default=0)),
                ('agent_type', models.CharField(choices=[('webhook', 'Webhook'), ('api', 'API')], default='webhook', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
