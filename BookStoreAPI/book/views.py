from rest_framework import viewsets, authentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope

from book.serializers import BookSerializer
from book.models import Book
   
class BookViewSet(viewsets.ModelViewSet):
   authentication_classes = [OAuth2Authentication]
   permission_classes = [IsAuthenticated]
   
   queryset = Book.objects.all()
   serializer_class = BookSerializer
   
   def get_permissions(self):
      if self.action in ['list', 'retrieve']:
         return [AllowAny()]
      if self.action in ['create', 'update', 'partial_update', 'destroy']:
         return [IsAuthenticated()]
      return super().get_permissions()