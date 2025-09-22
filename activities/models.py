from django.db import models
from django.db.models import Q, CheckConstraint
from django.contrib.auth.models import AbstractUser, Group,Permission
from django.core.validators import MinLengthValidator

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    bio = models.TextField(blank=True, max_length=500)
    groups = models.ManyToManyField(
        Group,
        related_name='groupes_users',
        blank=True,
        help_text='goupes auxquels cet utilisateur appartient.',
        verbose_name='groupes'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='permissions_users',
        blank=True,
        help_text='Permission specifique pour cet utilisateur.',
        verbose_name='user permissions'
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['username']

    def __str__(self):
        return self.username


class Activity(models.Model):
    title = models.CharField(
        verbose_name="Titre",
        max_length=200,
        validators=[MinLengthValidator(5)]
    )
    description = models.TextField(
        verbose_name="Description",
        validators=[MinLengthValidator(10)]
    )
    location_city = models.CharField(
        verbose_name="Ville",
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    start_time = models.DateTimeField(verbose_name="Date et heure de début")
    end_time = models.DateTimeField(verbose_name="Date et heure de fin")
    proposer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposed_activities')
    attendees = models.ManyToManyField(User, related_name='attended_activities', blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        constraints = [
            CheckConstraint(
                check=Q(end_time__gt=models.F('start_time')),
                name='end_after_start'
            )
        ]

    def __str__(self):
        return self.title


class Category(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de la catégorie", unique=True,
        error_messages={
            'unique': 'Cette categorie est déjà utilisée.',
            'invalid': 'Veuillez entrer une adresse email valide.'
        }
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['nom']

    def __str__(self):
        return self.nom
    
    #token daae64c6c141fe14900ef7f923b3458525999ae0