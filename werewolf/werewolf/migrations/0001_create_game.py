# Generated by Django 4.0 on 2022-01-25 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_create_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authentication.user')),
            ],
            options={
                'permissions': (('can_elect', 'Elect a player to be mayor'), ('can_vote', 'Vote against a player to be hanged'), ('can_murder', 'Werewolf vote to kill someone'), ('can_predict', 'Seer hability to predict someone character'), ('can_link', 'Cupidon hability to link to player to death'), ('can_save', 'Witch hability to save someone'), ('can_poison', 'Witch hability to kill someone')),
            },
        ),
    ]
