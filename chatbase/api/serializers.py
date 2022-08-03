# serializers will take a python model we want to intereact with and convert/turn it into a Json object
# a serializer works more like a model form/a Model

from rest_framework.serializers import ModelSerializer
from chatbase.models import Room



class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'