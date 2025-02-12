from . import models
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
   class Meta:
      model = models.Book
      fields = '__all__'