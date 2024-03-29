# Generated by Django 4.0 on 2022-01-25 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('werewolf', '0003_create_player'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='werewolf.round')),
                ('who', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='werewolf.player')),
                ('whom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='werewolf.player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Save',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='werewolf.round')),
                ('who', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='werewolf.player')),
                ('whom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='werewolf.player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Predict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='werewolf.round')),
                ('who', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='werewolf.player')),
                ('whom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='werewolf.player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Poison',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='werewolf.round')),
                ('who', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='werewolf.player')),
                ('whom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='werewolf.player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Murder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='werewolf.round')),
                ('who', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='werewolf.player')),
                ('whom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='werewolf.player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lover', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='werewolf.player')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='werewolf.round')),
                ('who', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='werewolf.player')),
                ('whom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='werewolf.player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Elect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='werewolf.round')),
                ('who', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='werewolf.player')),
                ('whom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='werewolf.player')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
