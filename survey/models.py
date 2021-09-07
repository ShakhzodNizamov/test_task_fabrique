from django.contrib.auth import get_user_model
from django.db import models


class Survey(models.Model):
    """
    Model Survey
    """
    title = models.CharField(verbose_name='Title', max_length=256)
    description = models.TextField(verbose_name='Description', max_length=1024)
    start_date = models.DateField(verbose_name='Start date')
    end_date = models.DateField(verbose_name='End date')

    def __str__(self):
        return self.title


class Question(models.Model):
    """
    Model question
    """

    TEXT = 0
    MULTI_CHOICE = 1
    CHOICE = 2

    choice_case = (
        (TEXT, 'TEXT'),
        (MULTI_CHOICE, 'MULTICHOICE'),
        (CHOICE, 'CHOICE'),
    )

    survey = models.ForeignKey(to=Survey, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name='Text', max_length=1024)
    type = models.SmallIntegerField(verbose_name='Type', choices=choice_case, default=TEXT)

    def __str__(self):
        return self.text


class Choice(models.Model):
    """
    Model Choice for questions
    """
    question = models.ForeignKey(
        to=Question,
        verbose_name='Question',
        on_delete=models.CASCADE,
        related_name='choices'
    )

    text = models.TextField(verbose_name='Text of question', max_length=1024)

    def __str__(self):
        return self.text


class Vote(models.Model):
    """
    Model Vote for survey
    """
    survey = models.ForeignKey(to=Survey, verbose_name='To survey', on_delete=models.CASCADE)
    id_user = models.PositiveIntegerField(verbose_name='User ID')
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='User',
        blank=True,
        null=True
    )
    vote_date = models.DateField(auto_now_add=True, editable=False, verbose_name='Vote date')


class Answer(models.Model):
    """
    Model Answer
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Question')
    vote = models.ForeignKey(to=Vote, verbose_name='To vote', related_name='answers', on_delete=models.CASCADE)
    choice = models.ManyToManyField(
        to=Choice,
        verbose_name='Choice',
        through='ChoiceAnswer',
        related_name='choices'
    )
    value = models.TextField(verbose_name='Value', max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.value


class ChoiceAnswer(models.Model):
    """
    Model ChoiceAnswer for many to many relation of choice in model Answer
    """
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
