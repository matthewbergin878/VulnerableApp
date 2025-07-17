from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import F
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.contrib.auth.decorators import login_required, user_passes_test
import requests

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
    url = "https://brokencrystals.com/api/secrets"
    response = requests.get(url, verify=False)
    return JsonResponse(response.json())