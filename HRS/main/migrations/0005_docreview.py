# Generated by Django 4.0.5 on 2022-06-24 08:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_hospital'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star_rating', models.TextField(blank=True)),
                ('non_rating', models.TextField(blank=True)),
                ('review', models.TextField(blank=True)),
                ('review_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.doctor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.user')),
            ],
        ),
    ]
