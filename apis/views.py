import json
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apis.serializers import *
from apis.queries import *
from apis.permissions import admin_only,admin_or_analyst
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password,check_password
from apis.db import execute
from django.http import JsonResponse
from apis.jwt_utility import generate_token

# User APIs
@api_view(['POST'])
@permission_classes([AllowAny])
def AddNewUser_f(request):
    try:
        serializer = AddNewUser_s(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            role = serializer.data.get('role')

            hashed_password = make_password(password)

            data = {
                'username': username,
                'password': hashed_password,
                'role': role,
            }
            user=CheckUser_q(username)

            if user:
                json_data = {
                    'status_code' : 400,
                    'status': 'Failed',
                    'data': '',
                    'message': 'User already exists',
                }
                return Response(json_data, status= status.HTTP_400_BAD_REQUEST)
            userid=AddNewUser_q(data)
            if userid:
                json_data= {
                    'status_code' : 200,
                    'status': 'SUCCESS',
                    'data': userid,
                    'message': 'Data inserted Successfully',
                }
                return Response(json_data, status= status.HTTP_200_OK)
        
            else:
                json_data = {
                    'status_code' : 200,
                    'status': 'SUCCESS',
                    'data': '',
                    'message': 'Data not inserted',
                }
                return Response(json_data, status= status.HTTP_200_OK)
            
        else:
            json_data = {
                'status_code': 300,
                'status': 'Failed',
                'data': serializer.errors,
                'message': 'Invalid input data',
            }
            return Response(json_data, status=status.HTTP_300_MULTIPLE_CHOICES)

    except Exception as e:
        json_data = {
            'status_code' : 400,
            'status': 'Failed',
            'data': str(e),
            'message': 'Exception occurred',
        }
        return Response(json_data, status= status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def UserLogin_f(request):
    data = request.data  

    username = data.get("username")
    password = data.get("password")


    user = execute(
        "SELECT id, password_hash, role FROM users WHERE username=%s",
        [username],
        fetchone=True
    )

    if not user:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    user_id, password_hash, role = user

    if not check_password(data["password"], password_hash):
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    token = generate_token(user_id, role)

    return JsonResponse({
        "access_token": token,
        "role": role
    })
    # username = request.data.get('username')
    # password = request.data.get('password')

    # user = CheckUser_q(username)
    # if user and check_password(password, user.password_hash):
    #     if not user.is_active:
    #         user.is_active = True # Force active for this session
    #         user.save()

    #     refresh = RefreshToken.for_user(user)
        
    #     return Response({
    #         'status': 'success',
    #         'status_code': 200,
    #         'refresh': str(refresh),
    #         'access': str(refresh.access_token),
    #         'user': {
    #             'username': user.username,
    #             'role': user.role, 
    #             'created_at': user.created_at,
    #         }
    #     })
    # else:
    #     return Response({
    #         'status': 'error',
    #         'message': 'Invalid credentials'
    #     }, status=status.HTTP_401_UNAUTHORIZED)

##   Threat/Event Ingestion API  ##

@api_view(['POST'])
@admin_only
def AddEvent_f(request):
    try:
        serializer = AddEvent_s(data=request.data)
        if serializer.is_valid():
            source_name = serializer.data.get('source_name')
            event_type = serializer.data.get('event_type')
            severity = serializer.data.get('severity')
            description = serializer.data.get('description')

            data = {
                'source_name': source_name,
                'event_type': event_type,
                'severity': severity,
                'description': description,
            }

            eventid=AddEvent_q(data)
            if eventid:
                json_data= {
                    'status_code' : 200,
                    'status': 'SUCCESS',
                    'data': eventid,
                    'message': 'Data inserted Successfully',
                }
                return Response(json_data, status= status.HTTP_200_OK)
        
            else:
                json_data = {
                    'status_code' : 200,
                    'status': 'SUCCESS',
                    'data': '',
                    'message': 'Data not inserted',
                }
                return Response(json_data, status= status.HTTP_200_OK)
            
        else:
            json_data = {
                'status_code': 300,
                'status': 'Failed',
                'data': serializer.errors,
                'message': 'Invalid input data',
            }
            return Response(json_data, status=status.HTTP_300_MULTIPLE_CHOICES)

    except Exception as e:
        json_data = {
            'status_code' : 400,
            'status': 'Failed',
            'data': str(e),
            'message': 'Exception occurred',
        }
        return Response(json_data, status= status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@admin_or_analyst
def AlertsList_f(request):
    try:
        serializer = AlertsList_s(data=request.data)
        if serializer.is_valid():
            event_severity = serializer.data.get('event_severity')
            alert_status = serializer.data.get('alert_status')

            if event_severity and alert_status:
                data = AlertsListByEventSeverityAndAlertStatus_q(event_severity, alert_status) 
            elif event_severity:
                data = AlertsListByEventSeverity_q(event_severity)
            elif alert_status:
                data = AlertsListByAlertStatus_q(alert_status)
            else:
                data = AlertsList_q()
            if data:
                json_data= {
                    'status_code' : 200,
                    'status': 'SUCCESS',
                    'data': data,
                    'message': 'Data Found Successfully',
                }
                return Response(json_data, status= status.HTTP_200_OK)
            else:
                json_data = {
                    'status_code' : 200,
                    'status': 'SUCCESS',
                    'data': [],
                    'message': 'Data Not Found',
                }
                return Response(json_data, status= status.HTTP_200_OK)
            
        else:
            json_data = {
                'status_code': 300,
                'status': 'Failed',
                'data': serializer.errors,
                'message': 'Invalid input data',
            }
            return Response(json_data, status=status.HTTP_300_MULTIPLE_CHOICES)

    except Exception as e:
        json_data = {
            'status_code' : 400,
            'status': 'Failed',
            'data': str(e),
            'message': 'Exception Occurred',
        }
        return Response(json_data, status= status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@admin_only
def AlertStatusUpdate_f(request):
    try:
        serializer = AlertStatusUpdate_s(data=request.data)
        if serializer.is_valid():
            alert_id = serializer.data.get('alert_id')
            alert_status = serializer.data.get('alert_status')
            print(alert_id, alert_status)
            data = AlertStatusUpdate_q(alert_id, alert_status) 
            print(data)
            if data:
                json_data= {
                    'status_code' : 200,
                    'status': 'SUCCESS',
                    'data': data,
                    'message': 'Data Updated Successfully',
                }
                return Response(json_data, status= status.HTTP_200_OK)
            else:
                json_data = {
                    'status_code' : 200,
                    'status': 'SUCCESS',
                    'data': [],
                    'message': 'Data Not Updated',
                }
                return Response(json_data, status= status.HTTP_200_OK)
            
        else:
            json_data = {
                'status_code': 300,
                'status': 'Failed',
                'data': serializer.errors,
                'message': 'Invalid Input Data',
            }
            return Response(json_data, status=status.HTTP_300_MULTIPLE_CHOICES)

    except Exception as e:
        json_data = {
            'status_code' : 400,
            'status': 'Failed',
            'data': str(e),
            'message': 'Exception Occurred',
        }
        return Response(json_data, status= status.HTTP_400_BAD_REQUEST)

