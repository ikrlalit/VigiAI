from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apis.serializers import *
from apis.queries import *

# Threat/Event Ingestion API
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
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



