from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tracking.mixins import LoggingMixin


class MockNoLoggingAPI(APIView):
    def get(self, request):
        return Response({'message': 'no logging'})


class MockLoggingAPI(LoggingMixin, APIView):
    def get(self, request):
        return Response({'message': 'logging'})


class MockExplicitLoggingAPI(LoggingMixin, APIView):
    logging_methods = ['POST']

    def get(self, request):
        return Response({'message': 'no logging'})

    def post(self, request):
        return Response({'message': 'logging'})


class MockCustomCheckLoggingAPI(LoggingMixin, APIView):
    def should_log(self, request, response):
        return 'log' in response.data

    def get(self, request):
        return Response({'message': 'logging'})

    def post(self, request):
        return Response({'message': 'no recording'})


class MockSessionAuthLoggingAPI(LoggingMixin, APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({'message': 'session auth logging'})


class MockTokenAuthLoggingAPI(LoggingMixin, APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({'message': 'token auth logging'})


class MockSensitiveFieldsLoggingAPI(LoggingMixin, APIView):
    sensitive_fields = {'mYfiEld'}

    def get(self, request):
        return Response({'message': 'logging'})


class MockInvalidCleanedSubstituteLoggingAPI(LoggingMixin, APIView):
    CLEANED_SUBSTITUTE = 1234
