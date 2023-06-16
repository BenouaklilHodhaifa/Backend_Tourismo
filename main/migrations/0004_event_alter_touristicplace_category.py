# Generated by Django 4.2.1 on 2023-06-16 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_touristicplace_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('touristicplace_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.touristicplace')),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
            ],
            bases=('main.touristicplace',),
        ),
        migrations.AlterField(
            model_name='touristicplace',
            name='category',
            field=models.CharField(choices=[('beach', 'beach'), ('museum', 'museum'), ('monumant', 'monumant'), ('landmark', 'landmark'), ('public square', 'public square'), ('archaeological site', 'archaeological site'), ('garden', 'garden'), ('relegious site', 'relegious site'), ('market', 'market'), ('restaurant', 'restaurant'), ('event', 'event')], max_length=30),
        ),
    ]
