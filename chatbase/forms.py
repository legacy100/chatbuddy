from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
# Specify the model you want to create a form for
        model = Room 
# the '__all__' attribute will create a form according to the attributes of the Room model
        fields = '__all__'