from django_filters import rest_framework as filters

from .models import *


class FutureFilter(filters.FilterSet):
    class Meta:
        model = Future
        fields = {
            "lot": ["exact"],
            "start_time": ["lte"],
            "end_time": ["gte"],
        }

    def __init__(self, *args, **kwargs):
        del kwargs["a"]
        super().__init__(*args, **kwargs)


class OptionFilter(FutureFilter):
    class Meta(FutureFilter.Meta):
        model = Option
        fields = {
            "lot": ["exact"],
            "start_time": ["lte"],
            "end_time": ["gte"],
            "request_expiration_time": ["lte"],
            "price": ["lte", "gte"],
            "fee": ["gte"],
            "collateral": ["gte"],
        }


class AcceptedOptionFilter(FutureFilter):
    class Meta(FutureFilter.Meta):
        model = Option
        fields = {
            "lot": ["exact"],
        }


class SingleUserSpotFilter(filters.FilterSet):
    date_range = filters.DateTimeFromToRangeFilter(label="Date Range")

    class Meta:
        model = Future
        fields = ["lot", "date_range"]

    def __init__(self, *args, **kwargs):
        self.a = kwargs.pop("a", None)
        super().__init__(*args, **kwargs)

    def filter_queryset(self, queryset):
        dates = self.form.cleaned_data.get("date_range", None)
        if dates:
            return queryset.accessible(self.a, dates.start, dates.stop)
        return Future.objects.none()


class MultipleUserSpotFilter(filters.FilterSet):
    user = filters.ModelChoiceFilter(label="User", queryset=EOSAccount.objects.all())
    date_range = filters.DateTimeFromToRangeFilter(label="Date Range")

    def __init__(self, *args, **kwargs):
        self.a = kwargs.pop("a", None)
        super().__init__(*args, **kwargs)

    def filter_queryset(self, queryset):
        a = self.form.cleaned_data.get("user", None)
        dates = self.form.cleaned_data.get("date_range", None)
        if a and dates:
            return queryset.accessible(a, dates.start, dates.stop)
        return Future.objects.none()


class GroupFilter(filters.FilterSet):
    class Meta(FutureFilter.Meta):
        model = Group
        fields = {
            "name": ["icontains"],
            "fee": ["lte"],
            "minimum_price": ["gte"],
            "minimum_ratio": ["gte"],
        }

    def __init__(self, *args, **kwargs):
        del kwargs["a"]
        super().__init__(*args, **kwargs)
