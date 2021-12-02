from django.contrib import admin

from .models import Filmwork, FilmworkGenre, FilmworkPerson, Genre, Person


class FilmworkPersonInline(admin.TabularInline):
    model = FilmworkPerson
    extra = 0


class FilmworkGenreInline(admin.TabularInline):
    model = FilmworkGenre
    extra = 0


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    fields = ('name', 'description', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Filmwork)
class FilmWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'creation_date', 'rating', 'genres')
    fields = (
        'title', 'type', 'description', 'creation_date', 'certificate',
        'file_path', 'rating', 'updated_at'
    )
    list_filter = ('type', 'genre')
    search_fields = ('title', 'description')
    inlines = [FilmworkGenreInline, FilmworkPersonInline]
    list_per_page = 50
    sortable_by = ('rating',)
    readonly_fields = ('created_at', 'updated_at')

    @staticmethod
    def genres(obj):
        return [
            filmwork_genre.genre.name for filmwork_genre in
            obj.filmwork_genres.all()
        ]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'genre':
            kwargs['queryset'] = Genre.objects.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date')
    fields = ('full_name', 'birth_date', 'updated_at')
    search_fields = ('full_name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(FilmworkPerson)
class FilmworkPersonAdmin(admin.ModelAdmin):
    list_display = ('film_work', 'person', 'role')
    list_filter = ('role',)
    search_fields = ('film_work', 'person')

    def has_add_permission(self, request):
        return False


@admin.register(FilmworkGenre)
class FilmworkGenreAdmin(admin.ModelAdmin):
    list_display = ('film_work', 'genre')
    list_filter = ('genre',)
    search_fields = ('film_work',)

    def has_add_permission(self, request):
        return False
