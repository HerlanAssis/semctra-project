from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager

from ..models import PatientProfile, Role, PatientProfile, DoctorProfile
from ..enum import RolesEnum
from ...core.utils import get_unique_or_none

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_id_display')

    class Meta:
        model = Role
        fields = ('id', 'name')


class UserRegisterSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(
        write_only=True
    )
    sus_number = serializers.CharField(required=False, write_only=True)
    crm = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password',
                  'password_confirmation', 'email',
                  'cpf', 'birthdate', 'phone',
                  'crm', 'sus_number'
                  )
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
        }

    def validate(self, data):
        """
        Check that passwords match.
        """
        password_confirmation = data.pop('password_confirmation')
        if data['password'] != password_confirmation:
            raise serializers.ValidationError(
                {"password": "As senhas devem ser iguais!"})

        '''
        Check if user send crm or sus_number
        '''
        sus_number = data.get('sus_number', None)
        crm = data.get('crm', None)
        if sus_number is None and crm is None:
            raise serializers.ValidationError(
                {'detail': 'CRM ou Número do SUS deve ser informados para definir o perfil'}
            )
        return data

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError("Email já cadastrado")
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validated_data):
        sus_number = validated_data.pop('sus_number', None)
        crm = validated_data.pop('crm', None)

        user = User.objects.create(**validated_data)

        if(sus_number):
            PatientProfile.objects.create(user=user, sus_number=sus_number)

        if(crm):
            DoctorProfile.objects.create(user=user, crm=crm)

        user.set_password(validated_data['password'])
        user.save()

        return user


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ('sus_number')


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ('crm')


class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'birthdate', 'roles')


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Senha inválida!')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()
    roles = RoleSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'is_active', 'auth_token', 'roles')
        read_only_fields = ('id', 'is_active', 'is_staff')

    def get_auth_token(self, obj):
        'Apenas o último login é válido'

        token = get_unique_or_none(Token, user=obj)

        if token:
            token.delete()

        token, create = Token.objects.get_or_create(user=obj)
        return token.key


class EmptySerializer(serializers.Serializer):
    pass
