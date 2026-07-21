from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Company, Facility, Violation
from .serializers import CompanySerializer, FacilitySerializer, ViolationSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class CompanyList(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)


class CompanyDetail(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get_company(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            return None

    def get(self, request, pk):
        company = self.get_company(pk)
        if company is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def put(self, request, pk):
        company = self.get_company(pk)
        if company is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        company = self.get_company(pk)
        if company is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        company = self.get_company(pk)
        if company is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        serializer = FacilitySerializer(facility, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        facility = self.get_facility(pk)
        if facility is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FacilitySerializer(facility, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        facility = self.get_facility(pk)
        if facility is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        facility.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ViolationList(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        violations = Violation.objects.all()
        serializer = ViolationSerializer(violations, many=True)
        return Response(serializer.data)


class ViolationDetail(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get_violation(self, pk):
        try:
            return Violation.objects.get(pk=pk)
        except Violation.DoesNotExist:
            return None

    def get(self, request, pk):
        violation = self.get_violation(pk)
        if violation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ViolationSerializer(violation)
        return Response(serializer.data)

    def put(self, request, pk):
        violation = self.get_violation(pk)
        if violation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ViolationSerializer(violation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        violation = self.get_violation(pk)
        if violation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ViolationSerializer(violation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        violation = self.get_violation(pk)
        if violation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        violation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
