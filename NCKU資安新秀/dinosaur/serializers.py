from django.contrib.auth.models import User, Group
from rest_framework import serializers
from dinosaur.models import check
from .models import Order



class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model  = check
        fields = ['cardid','room' ,'check_time']
        #exclude = ('user', 'room','start_time','end_time','room_timezone')

