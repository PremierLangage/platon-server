from pl_core.mixins import CsrfExemptSessionAuthentication
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class InfoView(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request: Request):
        return Response(request.LTI, status=status.HTTP_200_OK)
