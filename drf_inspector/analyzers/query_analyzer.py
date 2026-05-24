from django.urls import get_resolver
from django.urls.resolvers import (
    URLPattern,
    URLResolver
)

from rest_framework.views import APIView

from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet
)

RELATION_FIELDS = [
    "ForeignKey",
    "ManyToManyField",
    "OneToOneField"
]

LIST_TYPES = (
    ListAPIView,
    ListCreateAPIView,
    ModelViewSet,
    ReadOnlyModelViewSet
)

DETAIL_TYPES = (
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)


def analyze_queryset(queryset, view_class):
    """
    Analyze a queryset for optimization opportunities
    Returns a list of warnings and optimization suggestions
    """
    warnings = []

    if queryset is None:
        return warnings

    try:
        model = queryset.model
    except AttributeError:
        return warnings

    # Get all fields including relations
    foreign_keys = []
    many_to_many = []
    reverse_relations = []

    for field in model._meta.get_fields():
        field_type = field.__class__.__name__

        if field_type == "ForeignKey":
            foreign_keys.append(field.name)
        elif field_type == "ManyToManyField":
            many_to_many.append(field.name)
        elif field_type in ["ManyToOneRel", "OneToOneRel"]:
            reverse_relations.append(field.name)

    # Check for select_related opportunities (for ForeignKey and OneToOne)
    if foreign_keys:
        try:
            sql = str(queryset.query).upper()
            # Check if select_related is already applied
            has_select_related = any(
                f"INNER JOIN" in sql or f"LEFT OUTER JOIN" in sql
                for _ in foreign_keys
            )

            if not has_select_related and issubclass(view_class, LIST_TYPES):
                warnings.append(
                    f"Missing select_related() for ForeignKey fields: {', '.join(foreign_keys)}"
                )
        except Exception:
            pass

    # Check for prefetch_related opportunities (for ManyToMany and reverse relations)
    if many_to_many or reverse_relations:
        try:
            has_prefetch = hasattr(
                queryset,
                "_prefetch_related_lookups"
            ) and bool(queryset._prefetch_related_lookups)

            if not has_prefetch and issubclass(view_class, LIST_TYPES):
                related_fields = many_to_many + reverse_relations
                warnings.append(
                    f"Missing prefetch_related() for many-to-many/reverse relations: {', '.join(related_fields)}"
                )
        except Exception:
            pass

    # Check for only() or defer() optimization
    try:
        has_only_defer = (
            hasattr(queryset, "query") and
            (queryset.query.deferred_loading[0] or queryset.query.deferred_loading[1])
        )

        if not has_only_defer and issubclass(view_class, LIST_TYPES):
            warnings.append(
                "Consider using only() or defer() to limit fields retrieved from database"
            )
    except Exception:
        pass

    return warnings


def walk_patterns(
    urlpatterns,
    collected=None
):
    """
    Walk through URL patterns and collect view information
    """
    if collected is None:
        collected = []

    for pattern in urlpatterns:

        if isinstance(pattern, URLPattern):
            try:
                callback = pattern.callback

                # Skip drf_inspector's own views
                callback_module = getattr(callback, "__module__", "")
                if callback_module.startswith("drf_inspector"):
                    continue

                cls = getattr(
                    callback,
                    "cls",
                    None
                )

                if cls and issubclass(cls, APIView):

                    queryset = getattr(
                        cls,
                        "queryset",
                        None
                    )

                    warnings = []

                    # Analyze queries for list and retrieve views
                    if issubclass(cls, (LIST_TYPES + DETAIL_TYPES)):
                        warnings = analyze_queryset(queryset, cls)

                    collected.append({
                        "path": str(pattern.pattern),
                        "view": cls.__name__,
                        "warnings": warnings
                    })
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Error analyzing queries for pattern {pattern}: {e}")

        elif isinstance(pattern, URLResolver):

            walk_patterns(
                pattern.url_patterns,
                collected
            )

    return collected


def analyze_queries():
    """
    Analyze all registered queries for optimization opportunities
    """
    resolver = get_resolver()

    return walk_patterns(
        resolver.url_patterns
    )