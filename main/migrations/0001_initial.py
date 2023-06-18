# Generated by Django 4.2.1 on 2023-06-18 08:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('region', models.CharField(max_length=50, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubscriberRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('region', models.TextField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SubscriberVille',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('ville', models.TextField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TouristicPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('lat', models.FloatField()),
                ('long', models.FloatField()),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('beach', 'beach'), ('forrest', 'forrest'), ('museum', 'museum'), ('monumant', 'monumant'), ('landmark', 'landmark'), ('public square', 'public square'), ('archaeological site', 'archaeological site'), ('garden', 'garden'), ('relegious site', 'relegious site'), ('market', 'market'), ('restaurant', 'restaurant'), ('event', 'event')], max_length=30)),
                ('nb_visitors', models.IntegerField(default=0)),
                ('date_debut', models.DateField(null=True)),
                ('date_fin', models.DateField(null=True)),
                ('opening_time', models.TimeField(null=True)),
                ('closing_time', models.TimeField(null=True)),
                ('transport', models.CharField(choices=[('car', 'Car'), ('bus', 'Bus'), ('train', 'Train'), ('metro', 'Metro'), ('walking', 'Walking'), ('bicycle', 'Bicycle'), ('motorcycle', 'Motorcycle'), ('boat', 'Boat'), ('ferry', 'Ferry'), ('taxi', 'Taxi'), ('ride-sharing', 'Ride-sharing'), ('helicopter', 'Helicopter')], max_length=20, null=True)),
                ('region', models.CharField(max_length=50, null=True)),
                ('wilaya', models.CharField(max_length=50, null=True)),
                ('ville', models.CharField(max_length=50, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='TouristicPlaces', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos/', validators=[main.validators.file_size])),
                ('touristicPlace', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.touristicplace')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='multimedia')),
                ('touristicPlace', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.touristicplace')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('approved', models.BooleanField(default=False)),
                ('rating', models.IntegerField()),
                ('touristicPlace', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.touristicplace')),
            ],
        ),
    ]
