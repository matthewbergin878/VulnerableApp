from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.db.models import F
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.contrib.auth.decorators import login_required, user_passes_test
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def ssrf(request):
    url = request.GET.get('url')
    if not url:
        return JsonResponse({'error': 'URL parameter is required'}, status=400)
    
    try:
        #Add the custom header to simulate an internal request
        response = requests.get(url, headers={'X-Internal-Request': 'true'}, timeout=5)#don't check where we are trying to fetch
        response.raise_for_status()
        return JsonResponse({'content': response.text}) #return result regardless of where it's from
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

def internal(request):
    if request.headers.get('X-Internal-Request') != 'true': #check for internal request header
        return JsonResponse({'error': 'Access denied'}, status=403)
    if request.META.get('REMOTE_ADDR') not in ['127.0.0.1', '::1']: #check that request originated from the server
        #will always be true since we are running it locally
        return JsonResponse({'error': 'Access denied'}, status=403)
    #if the request was internal, return the secret resource
    return JsonResponse({'secret': 'This is a sensitive internal resource'})


def users(request):
    #vulnerable api
    url = "https://juice-shop.herokuapp.com/#/search"
    response = requests.get(url, verify=False)
    return HttpResponse(response.content, content_type="text/html")

@swagger_auto_schema(
    method="get",
    operation_description="Retrieve a greeting message",
    responses={
        200: openapi.Response(
            description="Successful response",
            examples={
                "application/json": {
                    "firstname": "John",
                    "cardnumber": "1239743628423",
                    "pwd": "password123",
                    "message": "Hello John!"
                }
            },
        )
    },
    manual_parameters=[
        openapi.Parameter(
            "firstname",
            openapi.IN_QUERY,
            description="The first name of the user",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "password",
            openapi.IN_QUERY,
            description="The password of the user",
            type=openapi.TYPE_STRING,
        )
    ],
)
@api_view(['GET'])
def hello(request):
    name = request.GET.get('firstname', 'guest')
    password = request.GET.get('role', 'user')  # Role is passed as a parameter
    data = {
        'firstname': name,
        'pwd': password,  # No validation of the role
        'message': f"Hello {name}!"
    }
    return Response(data, status=200)