from rest_framework import serializers
from .models import Listing, Booking, Review
from users.serializers import UserSerializer


class ListingSerializer(serializers.ModelSerializer):

    owner = UserSerializer(read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id',
            'name',
            'description',
            'price',
            'status',
            'owner',
            'created_at',
        ]

        read_only_fields = ['id', 'created_at']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id',
            'customer',# should nest nested
            'listing', # should nest nested
            'start_date',
            'end_date',
            'payment_status',
            'created_at',
            'updated_at'
        ]

        read_only_fields = ['id', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'customer', # Should nest
            'booking', # should nest
            'rating',
            'comment',
            'created_at'
        ]

        read_only_fields = ['id', 'created_at']
