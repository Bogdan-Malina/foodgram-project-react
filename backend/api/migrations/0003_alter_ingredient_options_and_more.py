# Generated by Django 4.1.3 on 2022-11-19 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_favorite_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['-id']},
        ),
        migrations.RemoveConstraint(
            model_name='ingredient',
            name='unique ingredient',
        ),
    ]
