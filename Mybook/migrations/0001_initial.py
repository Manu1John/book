# Generated by Django 3.1 on 2020-09-16 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='books',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=60)),
                ('category', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('image_url', models.CharField(max_length=500)),
                ('language', models.CharField(max_length=30)),
                ('pages', models.IntegerField()),
                ('book_published', models.IntegerField()),
            ],
        ),
    ]
