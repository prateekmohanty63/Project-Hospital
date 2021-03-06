# Generated by Django 4.0.6 on 2022-07-07 06:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_alter_docreview_user_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocAppointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateOfAppointment', models.DateField()),
                ('AdditionalMessage', models.TextField(max_length=500)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.doctor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
