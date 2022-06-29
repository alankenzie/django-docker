from characteristics.models import Characteristic
from characteristics.serializers import CharacteristicSerializer
from groups.models import Group
from groups.serializers import GroupSerializer
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer
from drf_spectacular.utils import OpenApiExample

from animals.models import Animal

@extend_schema_serializer(
    many=True,
    # exclude_fields=('sex',),
)
class AnimalRequestSerializer(serializers.ModelSerializer):
    group = GroupSerializer()

    class Meta:
        model = Animal
        fields = '__all__'

@extend_schema_serializer(
    exclude_fields=('sex',),
    examples = [
         OpenApiExample(
            'Exemplo Animal Serializer',
            summary='Criação de animais',
            description='Rota para criação de animais',
            value={
                'name': 'Bidu',
                'age': 5.5,
                'weight': 25.2,
                'group': {
                    'name': 'canis lupus familiaris'
                },
                'characteristics': [
                    {'name': 'peludo'}
                ]
            },
            request_only=True,
            response_only=False,
        )
    ]
)
class AnimalResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.FloatField()
    weight = serializers.FloatField()
    sex = serializers.CharField()

    group = GroupSerializer()

    characteristics = CharacteristicSerializer(many=True, allow_empty=False)

    def validate_group(self, value):
        if not value:
            raise serializers.ValidationError('group cannot be empty')

        return value

    def create(self, validated_data):
        group = validated_data.pop("group")
        characteristics = validated_data.pop("characteristics")

        group, _ = Group.objects.get_or_create(**group)

        animal: Animal = Animal.objects.create(**validated_data, group=group)

        for characteristic in characteristics:
            characteristic, _ = Characteristic.objects.get_or_create(**characteristic)
            animal.characteristics.add(characteristic)

        # [
        #     Characteristic.objects.get_or_create(**characteristic)[0]
        #     for characteristic in characteristics
        # ]
        # characteristics = [
        #     Characteristic.objects.get_or_create(**characteristic)[0]
        #     for characteristic in characteristics
        # ]
        # animal: Animal = Animal.objects.create(**validated_data, group=group, characteristics=characteristics)

        return animal

    def update(self, instance: Animal, validated_data: dict):
        non_editable_keys = {"sex", "group"}
        for key, value in validated_data.items():
            # útil para evitar atributos não validados passados no save()
            # if hasattr(instance, key)
            if key in non_editable_keys:
                raise KeyError(f"You can not update {key} property.")
            setattr(instance, key, value)

        instance.save()

        return instance

class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.FloatField()
    weight = serializers.FloatField()
    sex = serializers.CharField()

    group = GroupSerializer()

    characteristics = CharacteristicSerializer(many=True, allow_empty=False)

    def validate_group(self, value):
        if not value:
            raise serializers.ValidationError('group cannot be empty')

        return value

    def create(self, validated_data):
        group = validated_data.pop("group")
        characteristics = validated_data.pop("characteristics")

        group, _ = Group.objects.get_or_create(**group)

        animal: Animal = Animal.objects.create(**validated_data, group=group)

        for characteristic in characteristics:
            characteristic, _ = Characteristic.objects.get_or_create(**characteristic)
            animal.characteristics.add(characteristic)

        # [
        #     Characteristic.objects.get_or_create(**characteristic)[0]
        #     for characteristic in characteristics
        # ]
        # characteristics = [
        #     Characteristic.objects.get_or_create(**characteristic)[0]
        #     for characteristic in characteristics
        # ]
        # animal: Animal = Animal.objects.create(**validated_data, group=group, characteristics=characteristics)

        return animal

    def update(self, instance: Animal, validated_data: dict):
        non_editable_keys = {"sex", "group"}
        for key, value in validated_data.items():
            # útil para evitar atributos não validados passados no save()
            # if hasattr(instance, key)
            if key in non_editable_keys:
                raise KeyError(f"You can not update {key} property.")
            setattr(instance, key, value)

        instance.save()

        return instance
