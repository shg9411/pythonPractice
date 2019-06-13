# Generated by Django 2.2.1 on 2019-06-12 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commute', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='work',
            options={'ordering': ['start']},
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('idx', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=25)),
                ('upload', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
