from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from rest_framework import permissions, authentication
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config

# import serializers
from users.serializers import RegisterSerializer, LoginSerializer, recoverEmailSerializer

class Register(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        if data.get('password') != data.get('confirm_password'):
            return Response({'error': 'Password and Confirm password do not match'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()

        return Response(serializer.data)

class Login(APIView):
    def post(self, request, *args, **kwargs):
        
        data = request.data
        serializer = LoginSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh =  RefreshToken.for_user(user)
        accessToken = refresh.access_token
        login(request=request, user=user)
        print(request.user)
        return Response({
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'Refresh Token': str(refresh),
            'Access Token': str(accessToken)
        })
    
class Logout(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': "User has been logged out"})

@api_view(['POST'])
def passwordResetRequest(request, *args, **kwargs):
    email = request.data['email']
    serializer = recoverEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_user_model().objects.get(email=email)
    token = default_token_generator.make_token(user)
    uuid = urlsafe_base64_encode(force_bytes(user.pk))
    url = '{}/reset/{}/{}'.format(config('FRONT_END_BASE_URL'), uuid, token)

    message = Mail(
    from_email='abdulkadir.abubakar@vnicomhub.com',
    to_emails=email,
    subject='Password Reset',
    html_content='''<p style="text-align: center; font-size: 11pt">
                        <img width="40px" height="40px" src="https://static-media.streema.com/media/cache/85/77/85772762a9b7087d575a158ef78ddc97.jpg" alt="trakit-icon" />
                        <h2 style="font-size:14pt; text-align: center; margin-top: 30px"> Forgot Your Trakit Password?</h2>
                        <p style="font-size: 10pt; text-align: center; margin-top: 30px"> Dont worry, it happens!  <br /> 
                            To create a new password, just follow this link:
                        </p>
                        <p style="font-size:12pt; text-align: center; margin-top: 40px"> 
                            <a style="padding:10px; background-color: rgba(74, 147, 76, 0.8); color: white; text-decoration: none; border-radius: 10px" href='{}'>  Create a new password </a> 
                        </p>
                        <p style="font-size: 10pt; text-align: center; margin-top: 40px"> The button doest work? Copy and past the following link in your browser address bar:
                        <p style="font-size: 10pt; text-align: center; margin-top: 30px"><a href='{}'> {} </a> <p>
                    </p>'''.format(url, url, url)
    )
    try:
        sg = SendGridAPIClient(config('SENDGRID_API_KEY'))
        response = sg.send(message)

        if str(response.status_code)[0] == '2':
            return Response({'message': 'Recover email link sent successfully', 'uuid': uuid, 'token':token}, status= response.status_code)
        elif str(response.status_code)[0] == '4':
            return Response({'message': 'Client side failure'}, status=response.status_code)
        elif str(response.status_code)[0] == '5':
            return Response({'message': 'Server side failure'}, status=response.status_code)
        else:
            return Response({'message': 'Unidentified error'}, status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        return Response({'message': 'Failed to send message'}, status.HTTP_503_SERVICE_UNAVAILABLE)
    


class PasswordResetUpdate(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        password = data['password']
        confirm_password = data['confirm_password']

        if not password == confirm_password:
            return Response({'error': "Password and Confirm password do not match"}, status.HTTP_400_BAD_REQUEST)

        try:
            uuid = force_str(urlsafe_base64_decode(data['uuid']))
            user = get_user_model().objects.get(pk=uuid)
        except:
            return Response({'message': 'Invalid Recovery link'}, status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, data['token']):
            print(password)
            user.set_password(password)
            user.save()
            print(user, user.password)
            return Response({'message': 'Password Reset successfull'})
        
        return Response({'error': 'Something went wrong. Please try again later'}, status.HTTP_500_INTERNAL_SERVER_ERROR)
