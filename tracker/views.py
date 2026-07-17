from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Facility
from .serializers import FacilitySerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class FacilityList(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        facilities = Facility.objects.all()
        serializer = FacilitySerializer(facilities, many=True)
        return Response(serializer.data)


class FacilityDetail(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get_facility(self, pk):
        try:
            return Facility.objects.get(pk=pk)
        except Facility.DoesNotExist:
            return None

    def get(self, request, pk):
        facility = self.get_facility(pk)
        if facility is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FacilitySerializer(facility)
        return Response(serializer.data)

    def put(self, request, pk):
        facility = self.get_facility(pk)
        if facility is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(obj=facility, request=request)
        serializer = FacilitySerializer(facility, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        facility = self.get_facility(pk)
        if facility is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(obj=facility, request=request)
        serializer = FacilitySerializer(facility, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        facility = self.get_facility(pk)
        if facility is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(obj=facility, request=request)
        facility.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
