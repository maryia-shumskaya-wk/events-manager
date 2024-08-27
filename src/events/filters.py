from django_filters import rest_framework as filters

from events.models import Event


class EventFilter(filters.FilterSet):
    """Custom filters for events for user to be able to look for event specified by title, creator, start/end date
    and the maximum of allowed participants"""

    title = filters.CharFilter(lookup_expr="icontains")
    start_date = filters.DateTimeFilter()
    end_date = filters.DateTimeFilter()
    max_attendees = filters.NumberFilter()
    created_by_me = filters.BooleanFilter(
        field_name="created_by", method="filter_created_by_user"
    )

    def filter_created_by_user(self, queryset, value):
        if not value:
            return queryset
        elif value and self.request.user:
            return queryset(created_by=self.request.user)
        return queryset

    class Meta:
        model = Event
        fields = ["title", "start_date", "end_date", "max_attendees", "created_by"]
