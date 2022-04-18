# Generated by Django 4.0 on 2022-04-16 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('werewolf', '0004_create_actions'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='elect',
            unique_together={('round', 'who')},
        ),
        migrations.AlterUniqueTogether(
            name='link',
            unique_together={('round', 'who')},
        ),
        migrations.AlterUniqueTogether(
            name='murder',
            unique_together={('round', 'who')},
        ),
        migrations.AlterUniqueTogether(
            name='poison',
            unique_together={('round', 'who')},
        ),
        migrations.AlterUniqueTogether(
            name='predict',
            unique_together={('round', 'who')},
        ),
        migrations.AlterUniqueTogether(
            name='save',
            unique_together={('round', 'who')},
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('round', 'who')},
        ),
    ]