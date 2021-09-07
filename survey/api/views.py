import datetime

from django import shortcuts
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.exceptions import APIException

from .serializers import SurveySerializer, QuestionSerializer, VoteSerializer, ChoiceSerializer, VoteListSerializer
from survey.models import Survey, Question, Vote, Choice
from survey.permissions import SurveyPermission, QuestionPermission


class SurveyView(viewsets.ModelViewSet):
    """
    REST API for surveys.
    """
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = (SurveyPermission,)


class QuestionView(viewsets.ModelViewSet):
    """
    REST API for survey questions.
    """
    serializer_class = QuestionSerializer
    permission_classes = (QuestionPermission,)

    def get_queryset(self):
        survey_id = self.kwargs.get('survey_id')
        if survey_id:
            survey = shortcuts.get_object_or_404(Survey, id=survey_id)
            return Question.objects.filter(survey=survey)
        return Question.objects.all()

    def perform_create(self, serializer):
        survey_id = self.kwargs.get('survey_id')
        survey = shortcuts.get_object_or_404(Survey, id=survey_id)
        serializer.is_valid(raise_exception=True)
        serializer.save(survey=survey)

    def perform_update(self, serializer):
        survey_id = self.kwargs.get('survey_id')
        survey = shortcuts.get_object_or_404(Survey, id=survey_id)
        serializer.save(survey=survey)


class ChoiceView(viewsets.ModelViewSet):
    """
    REST API for choice of survey questions.
    """
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        survey_id = self.kwargs.get('survey_id')
        question_id = self.kwargs.get('question_id')
        if survey_id and question_id:
            question = shortcuts.get_object_or_404(Question, id=question_id, survey_id=survey_id)
            new_queryset = Choice.objects.filter(question=question)
            return new_queryset
        raise APIException(
            'question ID or survey ID is empty'
        )

    def perform_create(self, serializer):
        survey_id = self.kwargs.get('survey_id')
        question_id = self.kwargs.get('question_id')
        question = shortcuts.get_object_or_404(Question, id=question_id, survey_id=survey_id)
        serializer.save(question=question)

    def perform_update(self, serializer):
        survey_id = self.kwargs.get('survey_id')
        question_id = self.kwargs.get('question_id')
        question = shortcuts.get_object_or_404(Question, id=question_id, survey_id=survey_id)
        serializer.save(question=question)


class ActiveSurveyView(viewsets.ReadOnlyModelViewSet):
    """
    REST API for get all active Surveys
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = SurveySerializer
    http_method_names = ('get',)

    def get_queryset(self):
        return Survey.objects.filter(end_date__gte=datetime.date.today())


class UserVoteView(viewsets.ModelViewSet):
    """
    REST API for user votes
    """
    http_method_names = ('get', 'post')
    permission_classes = (permissions.AllowAny,)
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()


class UserVoteDetailView(viewsets.ModelViewSet):
    """
    REST API for get detailed vote of user
    """

    http_method_names = ('get',)
    permission_classes = (permissions.AllowAny,)
    serializer_class = VoteSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id:
            return Vote.objects.filter(id_user=user_id)

        raise APIException(
            'User not found'
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return VoteListSerializer
        return VoteSerializer
