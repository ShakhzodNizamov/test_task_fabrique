import datetime

from django.urls import reverse
from rest_framework.test import APITestCase

from survey.api.serializers import SurveySerializer
from survey.models import Survey


class ActiveSurveyAPITestCAse(APITestCase):
    def test_get(self):
        survey1 = Survey.objects.create(
            title='Survey1',
            start_date=datetime.date.today(),
            end_date=(datetime.date.today() + datetime.timedelta(days=1)),  # to get tomorrow
            description='description for Survey1'
        )
        survey2 = Survey.objects.create(
            title='Survey2',
            start_date=datetime.date.today(),
            end_date=(datetime.date.today() + datetime.timedelta(days=1)),  # to get tomorrow
            description='description for Survey2'
        )
        serializer_data = SurveySerializer([survey1, survey2], many=True).data
        url = 'http://127.0.0.1:8000/v1/user/survey/'
        response = self.client.get(url)
        self.assertEqual(serializer_data, response.data)
