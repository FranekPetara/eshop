from rest_framework import serializers
from .models import Product, Review

class ReviewSerializer(serializers.ModelSerializer):
   class Meta:
      model = Review
      fields = "__all__"



class ProductSerializer(serializers.ModelSerializer):
      
      reviews = serializers.SerializerMethodField(method_name="get_reviews", read_only=True)

     # class Meta:
     #      model = Product
     #      fields = "__all__"

     #      extra_kwags = {
     #           "name": {"required": True, 'allow_blank': False}
     #      }
      class Meta:
         model = Product
         # fields = "__all__"
         fields = ('id', 'name', 'description', 'price', 'brand', 'ratings', 'category', 'stock', 'user', "reviews")

         extra_kwargs = {
            "name": { "required": True, 'allow_blank':False },
            "description": { "required": True, 'allow_blank':False },
            "brand": { "required": True, 'allow_blank':False },
            "category": { "required": True, 'allow_blank':False },
         }

      def get_reviews(self, obj):
         reviews = obj.reviews.all()
         serializer = ReviewSerializer(reviews, many = True)
         return serializer.data
