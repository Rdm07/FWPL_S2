# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-08 15:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Matchday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('bonus_compulsory', models.BooleanField(default=False)),
                ('deadline', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='MatchdayBonus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus_exists', models.BooleanField(default=False)),
                ('bonus_points', models.IntegerField(default=0)),
                ('for_matchday', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Management.Matchday')),
                ('for_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q_number', models.IntegerField()),
                ('q_text', models.TextField()),
                ('margin', models.IntegerField(default=0)),
                ('bonus_allowed', models.BooleanField(default=True)),
                ('answer_set_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Answer_Set_Type', to='contenttypes.ContentType')),
                ('answer_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Answer_Type', to='contenttypes.ContentType')),
                ('for_matchday', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Management.Matchday')),
            ],
        ),
        migrations.CreateModel(
            name='ScorelineAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_team_score', models.IntegerField()),
                ('away_team_score', models.IntegerField()),
                ('bonus', models.BooleanField(default=False)),
                ('points', models.IntegerField(default=0)),
                ('by_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('for_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SA', to='Management.Question')),
            ],
        ),
        migrations.CreateModel(
            name='ScorelineAnswerSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_team_score', models.IntegerField()),
                ('away_team_score', models.IntegerField()),
                ('for_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SAS', to='Management.Question')),
            ],
        ),
        migrations.CreateModel(
            name='SingleIntegerAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.IntegerField()),
                ('bonus', models.BooleanField(default=False)),
                ('points', models.IntegerField(default=0)),
                ('by_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('for_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SIA', to='Management.Question')),
            ],
        ),
        migrations.CreateModel(
            name='SingleIntegerAnswerSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.IntegerField()),
                ('for_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SIAS', to='Management.Question')),
            ],
        ),
        migrations.CreateModel(
            name='SinglePlayerTeamAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=30)),
                ('bonus', models.BooleanField(default=False)),
                ('points', models.IntegerField(default=0)),
                ('by_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('for_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SPTA', to='Management.Question')),
            ],
        ),
        migrations.CreateModel(
            name='SinglePlayerTeamAnswerSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=30)),
                ('for_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SPTAS', to='Management.Question')),
            ],
        ),
        migrations.CreateModel(
            name='TeamAndValueAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(max_length=30)),
                ('value', models.IntegerField()),
                ('bonus', models.BooleanField(default=False)),
                ('points', models.IntegerField(default=0)),
                ('by_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('for_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TAVA', to='Management.Question')),
            ],
        ),
        migrations.CreateModel(
            name='TeamAndValueAnswerSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(max_length=30)),
                ('value', models.IntegerField()),
                ('for_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TAVAS', to='Management.Question')),
            ],
        ),
        migrations.CreateModel(
            name='WinDrawLoseAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(choices=[('Win', 'Win'), ('Draw', 'Draw'), ('Lose', 'Lose')], max_length=5)),
                ('bonus', models.BooleanField(default=False)),
                ('points', models.IntegerField(default=0)),
                ('by_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('for_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='WDLA', to='Management.Question')),
            ],
        ),
        migrations.CreateModel(
            name='WinDrawLoseAnswerSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(choices=[('Win', 'Win'), ('Draw', 'Draw'), ('Lose', 'Lose')], max_length=30)),
                ('for_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='WDLAS', to='Management.Question')),
            ],
        ),
        migrations.CreateModel(
            name='YesNoAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5)),
                ('bonus', models.BooleanField(default=False)),
                ('points', models.IntegerField(default=0)),
                ('by_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('for_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='YNA', to='Management.Question')),
            ],
        ),
        migrations.CreateModel(
            name='YesNoAnswerSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=30)),
                ('for_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='YNAS', to='Management.Question')),
            ],
        ),
    ]
