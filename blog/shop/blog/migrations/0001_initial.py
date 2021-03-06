# Generated by Django 2.2.1 on 2019-05-09 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('quauntity', models.IntegerField(default=0)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='ProductImg')),
                ('description', models.TextField()),
            ],
        ),
    ]
