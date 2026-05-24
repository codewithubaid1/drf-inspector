from django.urls import get_resolver
from django.urls.resolvers import (
    URLPattern,
    URLResolver
)

from rest_framework.views import APIView


def get_methods(callback):

    methods = []

    cls = getattr(
        callback,
        "cls",
        None
    )

    if cls:

        for method in [
            "get",
            "post",
            "put",
            "patch",
            "delete"
        ]:

            if hasattr(cls, method):

                methods.append(
                    method.upper()
                )

    return methods


def get_serializer(cls):

    serializer = getattr(
        cls,
        "serializer_class",
        None
    )

    if serializer:

        return serializer.__name__

    return None


def get_model(cls):

    queryset = getattr(
        cls,
        "queryset",
        None
    )

    if queryset is not None:

        try:
            return queryset.model.__name__

        except Exception:
            pass

    return None


def get_permissions(cls):

    permissions = getattr(
        cls,
        "permission_classes",
        []
    )

    return [
        p.__name__
        for p in permissions
    ]


def get_authentication(cls):

    authentication = getattr(
        cls,
        "authentication_classes",
        []
    )

    return [
        a.__name__
        for a in authentication
    ]


def get_pagination(cls):

    pagination = getattr(
        cls,
        "pagination_class",
        None
    )

    if pagination:

        return pagination.__name__

    return None


def walk_patterns(
    urlpatterns,
    collected=None
):

    if collected is None:
        collected = []

    for pattern in urlpatterns:

        if isinstance(
            pattern,
            URLPattern
        ):

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

                if (
                    cls
                    and issubclass(
                        cls,
                        APIView
                    )
                ):

                    collected.append({

                        "path":
                            str(
                                pattern.pattern
                            ),

                        "view":
                            cls.__name__,

                        "methods":
                            get_methods(
                                callback
                            ),

                        "serializer":
                            get_serializer(
                                cls
                            ),

                        "model":
                            get_model(
                                cls
                            ),

                        "permissions":
                            get_permissions(
                                cls
                            ),

                        "authentication":
                            get_authentication(
                                cls
                            ),

                        "pagination":
                            get_pagination(
                                cls
                            )
                    })
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Error analyzing view pattern {pattern}: {e}")

        elif isinstance(
            pattern,
            URLResolver
        ):

            walk_patterns(
                pattern.url_patterns,
                collected
            )

    return collected


def analyze_views():

    resolver = get_resolver()

    return walk_patterns(
        resolver.url_patterns
    )