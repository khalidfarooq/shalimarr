from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import File
from .serializers import FileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import api.file_crypto as fc
from main.models import Profile

class FileAPIView(APIView):
    def get(self, request):
        if 'profile' in request.GET:
            files = File.objects.filter(owner_id=request.GET['profile'])
        else:
            files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

    def post(self, request):
        if 'profile' in request.GET:
            print(request.GET['profile'])
            profile = Profile.objects.filter(id=request.GET['profile'])[0]
            profilekey = bytes(profile.cryptoKey[2:-1], 'utf-8')
            file_data = request.data['file_data']
            encrypted = fc.encrypt(request.data['file_data'].read(), profilekey)
            category = request.data['file_category']
            serializer = FileSerializer(
                data={'file_data': str(encrypted), 'file_name': file_data.name, 'file_size': file_data.size, 'file_content_type': file_data.content_type, 'owner_id': request.GET['profile'],'category': category})
            if serializer.is_valid():
                serializer.save()
                return redirect("http://127.0.0.1:3000/drive/")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return redirect("http://127.0.0.1:3000/login/")

class FileOperations(APIView):
    def get_file(self, fid):
        try:
            return File.objects.get(fid=fid)
        except File.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, fid):
        file = self.get_file(fid)
        serializer = FileSerializer(file)
        return Response(serializer.data)

    def put(self, request, fid):
        file = self.get_file(fid)
        serializer = FileSerializer(file, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, fid):
        file = self.get_file(fid)
        file.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


