# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'quiz',
            },
        ),
        migrations.CreateModel(
            name='QuizSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quiz', models.ForeignKey(to='rubrics.Quiz')),
            ],
            options={
                'db_table': 'quiz_submission',
            },
        ),
        migrations.CreateModel(
            name='RubricLevel1',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, unique=True, null=True, blank=True)),
            ],
            options={
                'db_table': 'rubric_level1',
            },
        ),
        migrations.CreateModel(
            name='RubricLevel2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, blank=True)),
                ('level1', models.ForeignKey(related_name='level2_mappings', to='rubrics.RubricLevel1')),
            ],
            options={
                'db_table': 'rubric_level2',
            },
        ),
        migrations.CreateModel(
            name='RubricLevel3',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, blank=True)),
                ('max_marks', models.IntegerField()),
                ('level2', models.ForeignKey(related_name='level3_mappings', to='rubrics.RubricLevel2')),
            ],
            options={
                'db_table': 'rubric_level3',
            },
        ),
        migrations.CreateModel(
            name='RubricStudentScoreMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField()),
                ('quiz_submission', models.ForeignKey(related_name='submission_score_mappings', to='rubrics.QuizSubmission')),
                ('rubric3', models.ForeignKey(related_name='level3_score_mappings', to='rubrics.RubricLevel3')),
            ],
            options={
                'db_table': 'rubric_student_score_mapping',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, blank=True)),
                ('email', models.CharField(unique=True, max_length=200, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'student',
            },
        ),
        migrations.AddField(
            model_name='quizsubmission',
            name='student',
            field=models.ForeignKey(to='rubrics.Student'),
        ),
        migrations.AlterUniqueTogether(
            name='rubriclevel3',
            unique_together=set([('name', 'level2')]),
        ),
        migrations.AlterUniqueTogether(
            name='rubriclevel2',
            unique_together=set([('name', 'level1')]),
        ),
    ]
