from django.shortcuts import render
from rest_framework.views import APIView


from pl_core.mixins import CrudViewSet
from rest_framework import status
from rest_framework.response import Response

class PlayViewSet(APIView):
    """
        View to build and eval an Asset.
        Require Token authentication.
    """
    
    def get(self, request, *args, **kwargs):
        # TODO
        # Check the user and it's permission
        # Retrieve the asset from its ID and build it
        
        return Response(
            data={
                'response': "Build Success",  
            },
            status=status.HTTP_200_OK
        )
        
    def post(self, request, *args, **kwargs):
        # TODO  
        # Check the user and it's permission
        # R
        return Response(
            data={
                'response': "Eval Success",
                },
            status=status.HTTP_201_CREATED
        )
        
    