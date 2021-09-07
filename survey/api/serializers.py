from rest_framework import serializers

from .field import ChoiceIdField
from survey.models import Survey, Question, Choice, Answer, Vote, ChoiceAnswer


class ChoiceSerializer(serializers.ModelSerializer):
    """
    Choice serializer.
    """

    class Meta:
        model = Choice
        fields = ('id', 'text')
        read_only_fields = ('id',)


class QuestionSerializer(serializers.ModelSerializer):
    """
    Question serializer.
    """
    type = serializers.ChoiceField(
        choices=Question.choice_case, default=Question.TEXT
    )
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ('id', 'survey', 'text', 'type', 'choices')
        read_only_fields = ('id',)
        extra_kwargs = {
            'survey': {'write_only': True}
        }

    def create_choices(self, question, choices):
        Choice.objects.bulk_create([
            Choice(question=question, **d) for d in choices
        ])

    def create(self, validated_data):
        choices = validated_data.pop('choices', [])
        question = Question.objects.create(**validated_data)
        self.create_choices(question, choices)
        return question

    def update(self, instance, validated_data):
        choices = validated_data.pop('choices', [])
        instance.choices.all().delete()
        self.create_choices(instance, choices)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class SurveySerializer(serializers.ModelSerializer):
    """
    Survey serializer.
    """
    questions = QuestionSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Survey
        fields = ('id', 'title', 'start_date', 'end_date', 'description', 'questions')
        read_only_fields = ('id',)

    def validate_start_date(self, value):
        """
        Raise error if try to change start_date after poll started.
        """
        if self.instance and self.instance.start_date < value:
            raise serializers.ValidationError(
                "Not allow change start_date poll is started"
            )

        return value

    def validate_end_date(self, value):
        """
        Raise error if end_date earlier than start_date.
        """
        if self.instance and value < self.instance.start_date:
            raise serializers.ValidationError(
                'The end_date cannot be earlier than the start_date'
            )
        return value


class AnswerSerializer(serializers.ModelSerializer):
    """
    Answer in Vote r/w serializer.
    """

    choice = ChoiceSerializer(read_only=True)
    choice_id = ChoiceIdField(
        queryset=Choice.objects.all(),
        many=True,
        required=False,
        write_only=True
    )

    question = QuestionSerializer(read_only=True)
    question_id = ChoiceIdField(queryset=Question.objects.all(), write_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'question_id', 'question', 'choice', 'choice_id', 'value')
        read_only_fields = ('id',)


class UserAnswerSerializer(serializers.ModelSerializer):
    choice_id = ChoiceIdField(
        queryset=Choice.objects.all(),
        write_only=True,
        many=True,
        required=False
    )

    class Meta:
        model = Answer
        fields = ('id', 'question', 'choice', 'choice_id', 'value')


class VoteSerializer(serializers.ModelSerializer):
    """
    Vote on Survey r/w serializer.
    """
    answers = UserAnswerSerializer(many=True)

    class Meta:
        model = Vote
        fields = ('id', 'survey', 'id_user', 'answers')
        # read_only_fields = ('id', 'user', 'vote_date')

    def create(self, validated_data):
        if 'answers' not in self.initial_data:
            raise serializers.ValidationError('Enter answers')

        answers = validated_data.pop('answers', [])
        instance = Vote.objects.create(**validated_data)

        for answer in answers:
            if 'choice_id' in answer:
                choice_id = answer.pop('choice_id')
                answer = Answer.objects.create(**answer, vote=instance)

                for pk in choice_id:
                    ChoiceAnswer.objects.create(choice_id=pk, answer=answer)
            else:
                Answer.objects.create(**answer, vote=instance)
        return instance

    def validate_answers(self, answers):
        for answer in answers:
            if answer['question'].type == Question.TEXT and 'choice_id' in answer:
                raise serializers.ValidationError(
                    'Questions with TEXT type must have only text answer without choices'
                )
            if answer['question'].type in [Question.CHOICE, Question.MULTI_CHOICE] and \
                    'value' in answer:
                raise serializers.ValidationError(
                    'Questions with CHOICE or MULTI_CHOICE type must have only choices answer without value'
                )

        return answers


class UserVoteSerializer(serializers.ModelSerializer):
    question = serializers.StringRelatedField()
    choice = ChoiceSerializer(read_only=True, many=True)

    class Meta:
        model = Answer
        fields = ('id', 'question', 'choice', 'value')


class VoteListSerializer(serializers.ModelSerializer):
    answers = UserVoteSerializer(many=True)
    survey = serializers.StringRelatedField()

    class Meta:
        model = Vote
        fields = ('id', 'id_user', 'survey', 'vote_date', 'answers')
