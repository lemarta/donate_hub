from django.db.models import fields
from rest_framework import serializers

import donating.models as donating_models


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = donating_models.Donation
        fields = [
            'quantity',
            'categories',
            'institution',
            'address',
            'phone_number',
            'city',
            'zip_code',
            'pick_up_date',
            'pick_up_time',
            'pick_up_comment',
        ]

