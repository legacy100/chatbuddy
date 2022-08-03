from rest_framework.decorators import api_view
from rest_framework.response import Response
from chatbase.models import Room
from .serializers import RoomSerializer
# from django.http import JsonResponse
# JsonResponse is a javascript object notation response


@api_view(['GET'])
def getRoutes(request):
# with this api we allow people to view/get a Json array of all our rooms in our project from our database and maybe allow them to access down to a specific room with the :id parameter
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
# safe here means that we can use more than the python dictionary in this response, it will allow the list to be turned into a json list
    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
# many=True means that we are might/will be serializing many objects from the rooms list/objects
    serializer= RoomSerializer(rooms, many=True)
    return Response(serializer.data)


# if we want a user to access only a single room from our rooms
@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)




