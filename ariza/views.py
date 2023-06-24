from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ArizaSerializer
from .models import Ariza

@api_view(['GET'])
def ariza_get(request):
    return Response({'status':200, 'data':'Barcha arizalar'})

@api_view(['GET','POST'])
def ariza_post(request):   
    serializer=ArizaSerializer(data=request.data)
    if not serializer.is_valid():        
        return Response({'status':403, 'xatolik':serializer.errors, 'message':'xatolik yuz berdi'})
    serializer.save()
    return Response({'status':200, 'data':serializer.data, 'message':'Malumot qo`shildi'})

@api_view(['GET','PUT'])
def ariza_update(request, id):
    std = Ariza.objects.get(id=id)
    try:
        serializer=ArizaSerializer(std, data=request.data, partial=True)
        if not serializer.is_valid():        
            return Response({'status':403, 'xatolik':serializer.errors, 'message':'xatolik yuz berdi'})
        serializer.save()
        return Response({'status':200, 'data':serializer.data, 'message':'Malumot yangilandi'})
    
    except Exception as e:
        print(e)
        return Response({'status':403, 'message':'Xato id'}) 
    
    
    
@api_view(['GET','DELETE'])
def ariza_delete(request, id):
    std = Ariza.objects.get(id=id)
    std.delete()
    return Response({'status':200, 'message':'Malumot ochirildi'})