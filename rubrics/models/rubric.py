from django.db import models


class Quiz(models.Model):
    name = models.CharField(blank=True, null=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quiz'


class Student(models.Model):
    name = models.CharField(blank=True, null=True, max_length=200)
    email = models.CharField(blank=True, max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student'


class QuizSubmission(models.Model):
    quiz = models.ForeignKey(Quiz)
    student = models.ForeignKey(Student)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quiz_submission'


class RubricLevel1(models.Model):
    name = models.CharField(blank=True, null=True, max_length=200, unique=True)

    class Meta:
        db_table = 'rubric_level1'


class RubricLevel2(models.Model):
    name = models.CharField(blank=True, null=True, max_length=200)
    level1 = models.ForeignKey(RubricLevel1, related_name='level2_mappings')

    class Meta:
        db_table = 'rubric_level2'
        unique_together = ('name', 'level1')


class RubricLevel3(models.Model):
    name = models.CharField(blank=True, null=True, max_length=200)
    level2 = models.ForeignKey(RubricLevel2, related_name='level3_mappings')
    max_marks = models.IntegerField()

    class Meta:
        db_table = 'rubric_level3'
        unique_together = ('name', 'level2')


class RubricStudentScoreMapping(models.Model):
    rubric3 = models.ForeignKey(RubricLevel3, related_name='level3_score_mappings')
    quiz_submission = models.ForeignKey(QuizSubmission, related_name='submission_score_mappings')
    score = models.FloatField()

    class Meta:
        db_table = 'rubric_student_score_mapping'
