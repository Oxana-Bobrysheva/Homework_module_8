import django_filters

from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    # Фильтрация по курсу (по ID курса)
    course = django_filters.NumberFilter(field_name="paid_course__id")

    # Фильтрация по уроку (по ID урока)
    lesson = django_filters.NumberFilter(field_name="paid_lesson__id")

    # Фильтрация по способу оплаты (точное совпадение)
    payment_method = django_filters.ChoiceFilter(
        field_name="payment_type", choices=Payment.PAYMENT_TYPE_CHOICE
    )

    # Фильтрация по дате (диапазон)
    payment_date_from = django_filters.DateFilter(
        field_name="payment_date", lookup_expr="gte"
    )
    payment_date_to = django_filters.DateFilter(
        field_name="payment_date", lookup_expr="lte"
    )

    class Meta:
        model = Payment
        fields = []

    # Добавляем сортировку
    @property
    def ordering_filters(self):
        return {
            "payment_date": "payment_date",
            "-payment_date": "-payment_date",
        }
