from rest_framework import serializers
from .models import UserModel, CardModel, OrderHistoryModel
import datetime

class Registration_response(serializers.Serializer):
    status = serializers.CharField()
    token = serializers.CharField()


class RegistrationSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['documentCode'] and len(data['documentCode']) == 9:
            try:
                int(data['documentCode'][:2])
                raise serializers.ValidationError("Password data is uncorrect")
            except:
                if not data['documentCode'][:2].isupper():
                    raise serializers.ValidationError("Please use uppercase letter")
            try:
                int(data['documentCode'][2:9])
                pass
            except:
                raise serializers.ValidationError("Password data is uncorrect")
        else:
            raise serializers.ValidationError("Password data is uncorrect")
        return data

    def create(self, validated_data):
        documentCode = validated_data.pop('documentCode', None)
        instance = self.Meta.model(**validated_data)
        instance.set_password(documentCode)
        instance.save()
        return instance

    class Meta:
        model = UserModel
        fields = ['id' ,'username','first_name', 'last_name', 'documentCode', 'documentDate', 'password']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
        }


class CardSerializer(serializers.ModelSerializer):
    number = serializers.SerializerMethodField()

    def get_number(self, obj):
        number = obj.number

        return number[:6]+'******'+number[12:]

    class Meta:
        model = CardModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'expire':{'write_only': True},
            'cvv':{'write_only': True},
        }

    def create(self, validated_data):
        user =  self.context['request'].user
        instance = self.Meta.model(**validated_data)
        instance.user = user
        instance.save()
        return instance


class CardGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = CardModel
        fields = ['id', 'number', 'title']


class OrderHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderHistoryModel
        fields = '__all__'