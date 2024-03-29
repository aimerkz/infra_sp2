from datetime import datetime

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import RefreshToken

from reviews import models
from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания пользователя.
    Проверяет username на запрещенные значения.
    """

    def send_mail(self, username):
        """
        Метод send_mail отправляет confirmation_code на почту пользователя.
        """
        user = get_object_or_404(User, username=username)
        send_mail(
            'Добро пожаловать на YaMDB',
            f'Дорогой {username},\n'
            f'Ваш confirmation_code: {user.confirmation_code}',
            'from@example.com',
            [f'{user.email}'],
            fail_silently=False,
        )

    def validate(self, attrs):
        """Проверка ввода недопустимого имени ("me") и уникальность полей."""
        if attrs['username'] == 'me':
            raise serializers.ValidationError(
                "Поле username не может быть 'me'."
            )
        if attrs['username'] == attrs['email']:
            raise serializers.ValidationError(
                'Поля email и username не должны совпадать.'
            )
        return attrs

    class Meta:
        model = User
        fields = ('email', 'username')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]


class CustomTokenObtainSerializer(serializers.ModelSerializer):
    """
    Кастомный сериализатор формы предоставления данных для аутентификации.
    Валидация по "confirmation_code".
    """
    username_field = User.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        """Переопределяем поля в форме получения токена"""
        super(CustomTokenObtainSerializer, self).__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields["confirmation_code"] = serializers.CharField()

    def get_token(self, user):
        """Функция создания токена."""
        refresh = RefreshToken.for_user(user)
        return {'access': str(refresh.access_token), }

    def validate(self, attrs):
        username = attrs['username']
        confirmation_code = attrs['confirmation_code']
        user = get_object_or_404(User, username=username)
        if confirmation_code != user.confirmation_code:
            raise serializers.ValidationError('Не правильно введены данные')
        return attrs

    class Meta:
        model = User
        fields = ('confirmation_code', 'username', )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения данных пользователя."""
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "role",
            "first_name",
            "last_name",
            "bio",
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = models.Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating')


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=models.Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=models.Genre.objects.all(),
        many=True,
        slug_field='slug'
    )

    class Meta:
        model = models.Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category')

    def validate_year(self, value):
        if value > datetime.today().year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли!'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(default=TitleReadSerializer)

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        title = request.parser_context['kwargs']['title_id']
        review = models.Review.objects.filter(title=title, author=user)
        if review.exists() and request.method == 'POST':
            raise serializers.ValidationError(
                detail='Нельзя оставлять больше одного отзыва на произведение',
                code=status.HTTP_400_BAD_REQUEST
            )
        return attrs

    class Meta:
        model = models.Review
        fields = ('id', 'text', 'author', 'title', 'score', 'pub_date')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=models.Review.objects.all(),
                fields=['title', 'author'],
                message='вы уже оставляли отзыв'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    review = serializers.HiddenField(default=ReviewSerializer)

    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'author', 'review', 'pub_date')
