from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork, Role


class MovieBaseApi:
    model = Filmwork
    http_method_names = ['get']

    @staticmethod
    def get_field_array(role: str) -> ArrayAgg:
        return ArrayAgg(
            'filmwork_persons__person__full_name', filter=Q(filmwork_persons__role=role), distinct=True
        )

    @classmethod
    def get_queryset(cls):
        return Filmwork.objects.prefetch_related('persons', 'genres').values(
            'id', 'title', 'description', 'creation_date', 'rating', 'type'
        ).annotate(
            genres=ArrayAgg('genre__name', distinct=True)
        ).annotate(
            actors=cls.get_field_array(Role.ACTOR)
        ).annotate(
            directors=cls.get_field_array(Role.DIRECTOR)
        ).annotate(
            writers=cls.get_field_array(Role.WRITER)
        )

    @staticmethod
    def render_to_response(context, **kwargs):
        return JsonResponse(context)


class MoviesListApi(MovieBaseApi, BaseListView):
    paginate_by = 50

    def get_context_data(self, object_list=None, **kwargs):
        paginator, page, queryset, _ = self.paginate_queryset(
            self.get_queryset(),
            self.paginate_by
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset)
        }
        return context


class MoviesDetailApi(MovieBaseApi, BaseDetailView):
    def get_context_data(self, **kwargs):
        return super(MoviesDetailApi, self).get_context_data(**kwargs)['object']
