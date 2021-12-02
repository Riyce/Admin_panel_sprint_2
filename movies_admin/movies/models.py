import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils import file_upload_to


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('Movie')
    TV_SHOW = 'tv_show', _('TV Show')


class Role(models.TextChoices):
    ACTOR = 'actor', _('Actor')
    DIRECTOR = 'director', _('Director')
    WRITER = 'writer', _('Writer')


class Genre(TimeStampedMixin, models.Model):
    id = models.UUIDField('ID', primary_key=True, default=uuid.uuid4,
                          editable=False)
    name = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), blank=True)

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        db_table = '"content"."genre"'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Person(TimeStampedMixin, models.Model):
    id = models.UUIDField('ID', primary_key=True, default=uuid.uuid4,
                          editable=False)
    full_name = models.CharField(_('Full name'), max_length=255, unique=True)
    birth_date = models.DateField(_('Birthday'), blank=True)

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        db_table = '"content"."person"'
        indexes = [
            models.Index(fields=('full_name',), name='person_full_name_idx')
        ]
        ordering = ('full_name',)

    def __str__(self) -> str:
        return self.full_name


class Filmwork(TimeStampedMixin, models.Model):
    id = models.UUIDField('ID', primary_key=True, default=uuid.uuid4,
                          editable=False)
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    creation_date = models.DateField(_('Creation date'), blank=True)
    certificate = models.CharField(_('Certificate'), max_length=255,
                                   blank=True)
    file_path = models.FileField(_('File path'), upload_to=file_upload_to,
                                 blank=True)
    rating = models.FloatField(_('Rating'), blank=True, validators=[
        MinValueValidator(0), MaxValueValidator(10)
    ])
    type = models.CharField(_('Type'), max_length=20,
                            choices=FilmworkType.choices)
    genre = models.ManyToManyField(Genre, verbose_name=_('Genres'),
                                   through='FilmworkGenre')
    persons = models.ManyToManyField(Person, verbose_name=_('Persons'),
                                     through='FilmworkPerson')

    class Meta:
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')
        db_table = '"content"."film_work"'
        indexes = [
            models.Index(
                fields=('title',),
                name='film_work_idx'
            )
        ]
        ordering = ('title',)

    def __str__(self) -> str:
        return self.title


class FilmworkGenre(models.Model):
    id = models.UUIDField('ID', primary_key=True, default=uuid.uuid4,
                          editable=False)
    film_work = models.ForeignKey(Filmwork, related_name='filmwork_genres',
                                  on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, related_name='genre_filmworks',
                              on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '"content"."genre_film_work"'
        ordering = ('film_work', 'genre')
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'genre'],
                name='film_work_genre_idx'
            )
        ]

    def __str__(self) -> str:
        return f'{self.film_work} - {self.genre}'


class FilmworkPerson(models.Model):
    id = models.UUIDField('ID', primary_key=True, default=uuid.uuid4,
                          editable=False)
    film_work = models.ForeignKey(Filmwork, related_name='filmwork_persons',
                                  on_delete=models.CASCADE)
    person = models.ForeignKey(Person, related_name='person_filmworks',
                               on_delete=models.CASCADE)
    role = models.CharField(_('Role'), max_length=16, choices=Role.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '"content"."person_film_work"'
        ordering = ('film_work', 'person')
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'person', 'role'],
                name='film_work_person_role_idx'
            )
        ]

    def __str__(self) -> str:
        return f'{self.film_work} - {self.person}'
