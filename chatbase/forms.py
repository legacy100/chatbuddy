from django.forms import ModelForm
from .models import Room, Message


class RoomForm(ModelForm):
    class Meta:
# Specify the model you want to create a form for
        model = Room

# the '__all__' attribute will create a form according to the attributes of the Room model
        fields = '__all__'

class MessageForm(ModelForm):
        class Meta:
                model = Message
                fields = '__all__'
            

            
                