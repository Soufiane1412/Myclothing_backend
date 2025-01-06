from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Product
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'price', 'image_url']

# initialised the token serialiser
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username 

        return token
    
# Initialised the token view
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):

    """
    UserSerializer converts User model instances to/from JSON.
    It inherits from ModelSerializer which provides default create/update operations
    """
    # Additional field not in the model
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User # specifies which model to serialize
        fields = ('id', 'username', 'email', 'password', 'password_confirm')
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate(self, data):
        """
        Custom validation method.
        vaidated_data is created after this validation passes.
        """
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("Passwords don't match 🤔 try again")
        return data
    
    def create(self, validated_data):

        """
        Override the create method to properly handle password hashing.
        validated_data: Dictionary of field values that passed validation
        """
        # Never store raw passwords! Django handles hashing
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''), # Email optional
            password=validated_data['password']
        )
        return user
    
    """
    #1 When a POST request comes in with JSON data:
    {
        "username": "John_Doe",
        "email": "John@example.com",
        "password": "securepass123",
        "password_confirm": "securepass123"
    }

    The flow is:

    1. Conversion from JSON to Python Dictionary (automatic)
    2. Validate() checks passwords match
    3. create() is called with validated_data
    4. User instance is created with a hashed password
    5. response is serialized back to JSON (without password field)
    """



