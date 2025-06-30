from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    'message': 'Inscription réussie',
                    'user': UserSerializer(user).data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'message': 'Erreur de validation',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': 'Erreur lors de l\'inscription',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST) 