# Generated by Django 2.2.5 on 2019-10-10 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poem', '0002_remove_groupofmetrics_metrics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metric',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='poem.GroupOfMetrics'),
        ),
    ]
