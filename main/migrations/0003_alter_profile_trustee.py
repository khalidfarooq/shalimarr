# Generated by Django 3.2.4 on 2021-06-28 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210628_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='trustee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.trustee'),
        ),
    ]
