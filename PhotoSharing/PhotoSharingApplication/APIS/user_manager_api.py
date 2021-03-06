from django.contrib.auth import authenticate, logout
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth import login as auth_login

# Create your views here.
from PhotoSharingApplication.APIS.helpers import authentication_helper
from PhotoSharingApplication.APIS.helpers.api_helper import JSONResponse, get_response_data
from PhotoSharingApplication.APIS.helpers.serializers import UserSerializer
from PhotoSharingApplication.models import UserProfile
from django.template import RequestContext, loader


@api_view(['POST'])
def login_action(request):
    if request.method == 'POST':
        user = authentication_helper.login_authenticate(request)
        if user is not None:
            if user.is_active:
                # return success response
                authenticated_user = authenticate(username=user.username)
                auth_login(request, authenticated_user)
                # serializer = UserSerializer(authenticated_user)
                return render(request, 'views/home.html')
            else:
                return render(request, 'views/login.html', {'error_message': "Invalid username / password.", })
        else:
            return render(request, 'views/login.html', {'error_message': "Invalid username / password.", })

    else:
        return HttpResponse("Login Failed")


@api_view(['POST'])
def logout_action(request):
    logout(request)
    return render(request, 'views/login.html')


@api_view(['POST'])
def register_action(request):
    home_template = loader.get_template('views/home.html')
    register_template = loader.get_template('views/register.html')
    if request.method == 'POST':
        if authentication_helper.get_user_with_email_address(request.data['email']) is not None:
            context = RequestContext(request, {'error_message': "Email Already exists.", })
            return HttpResponse(register_template.render(context))
        elif authentication_helper.get_user_with_username(request.data['username']) is not None:
            context = RequestContext(request, {'error_message': "Username Already exists.", })
            return HttpResponse(register_template.render(context))
        else:
            user = UserProfile.objects.create_user(request.data['username'], request.data['email'],
                                                   request.data['password'], request.data['firstName'],
                                                   request.data['lastName'])
            user.save()
            if user is not None:
                if user.user.is_active:
                    # return success response
                    authenticated_user = authenticate(username=request.data['username'])
                    auth_login(request, authenticated_user)
                    # serializer = UserSerializer(authenticated_user)

                    context = RequestContext(request)
                    return HttpResponse(home_template.render(context))
                else:
                    context = RequestContext(request, {'error_message': "Invalid username / password.", })
                    return HttpResponse(register_template.render(context))
            else:
                context = RequestContext(request, {'error_message': "Unable to create the user. "
                                                                    "Please check the username, email", })
                return HttpResponse(register_template.render(context))

    else:
        return HttpResponse("Bad request")


@api_view(['POST'])
def facebook_login(request):
    if request.method == 'POST':
        user = authentication_helper.get_user_with_email_address(request.data['email'])
        if user is not None:
            auth_user = authenticate(username=user.username)
            auth_login(request, auth_user)
            serializer = UserSerializer(user)
            return JSONResponse(get_response_data("", serializer.data))
        else:
            facebook_user = UserProfile.objects.create_facebook_user(request.data["fb_user_id"],
                                                                     request.data["fb_access_token"],
                                                                     request.data["email"], request.data["firstName"],
                                                                     request.data['lastName'])
            facebook_user.save()
            auth_user = authenticate(username=facebook_user.user.username)
            auth_login(request, auth_user)
            serializer = UserSerializer(facebook_user.user)
            return JSONResponse(get_response_data("", serializer.data))

    else:
        return JSONResponse(get_response_data("bad request", ""))



