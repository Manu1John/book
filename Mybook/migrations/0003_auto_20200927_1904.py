# Generated by Django 3.1 on 2020-09-27 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mybook', '0002_books_summary'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='books',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
