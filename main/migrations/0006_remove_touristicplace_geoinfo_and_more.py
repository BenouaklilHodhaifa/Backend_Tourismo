# Generated by Django 4.2.1 on 2023-06-16 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_useraccount_region_video_touristicplace_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='touristicplace',
            name='geoinfo',
        ),
        migrations.AddField(
            model_name='touristicplace',
            name='date_debut',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='touristicplace',
            name='date_fin',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='touristicplace',
            name='region',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='touristicplace',
            name='ville',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='touristicplace',
            name='wilaya',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='touristicplace',
            name='category',
            field=models.CharField(choices=[('beach', 'beach'), ('forrest', 'forrest'), ('museum', 'museum'), ('monumant', 'monumant'), ('landmark', 'landmark'), ('public square', 'public square'), ('archaeological site', 'archaeological site'), ('garden', 'garden'), ('relegious site', 'relegious site'), ('market', 'market'), ('restaurant', 'restaurant'), ('event', 'event')], max_length=30),
        ),
    ]
