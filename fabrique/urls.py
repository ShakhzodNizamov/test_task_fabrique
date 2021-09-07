"""fabrique URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter, SimpleRouter

from survey.api.views import SurveyView, QuestionView, ActiveSurveyView, ChoiceView, UserVoteView, UserVoteDetailView

schema_view = get_schema_view(
    openapi.Info(
        title="Survey API",
        default_version='v1',
        description="Fabrique test task"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = SimpleRouter()
router.register(r'survey', SurveyView)
router.register(r'survey/(?P<survey_id>\d+)/question', QuestionView, 'questions')
router.register(r'survey/(?P<survey_id>\d+)/questions/(?P<questions_id>\d+)/choice', ChoiceView, 'choice')
router.register(r'user/survey', ActiveSurveyView, 'active_surveys')
router.register(r'user/vote', UserVoteView, 'uservote')
router.register(r'user/(?P<user_id>\d+)', UserVoteDetailView, 'uservotedetail')



urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    url(r'^v1/', include((router.urls, 'v1'), namespace='v1')),
    path('admin/', admin.site.urls),

]

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]