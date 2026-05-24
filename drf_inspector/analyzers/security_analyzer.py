from django.urls import get_resolver
from django.urls.resolvers import (
    URLPattern,
    URLResolver
)

from rest_framework.views import APIView


SAFE_METHODS = [
    "GET",
    "HEAD",
    "OPTIONS"
]


def get_methods(cls):

    methods = []

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

                    methods = get_methods(
                        cls
                    )

                    permissions = getattr(
                        cls,
                        "permission_classes",
                        []
                    )

                    authentication = getattr(
                        cls,
                        "authentication_classes",
                        []
                    )

                    throttle = getattr(
                        cls,
                        "throttle_classes",
                        []
                    )

                    warnings = []

                    dangerous = any(
                        method not in SAFE_METHODS
                        for method in methods
                    )

                    if dangerous and not permissions:

                        warnings.append(
                            "No permission classes"
                        )

                    if dangerous and not authentication:

                        warnings.append(
                            "No authentication"
                        )

                    if dangerous and not throttle:

                        warnings.append(
                            "No throttling"
                        )

                    collected.append({

                        "path":
                            str(pattern.pattern),

                        "view":
                            cls.__name__,

                        "methods":
                            methods,

                        "permissions": [
                            p.__name__
                            for p in permissions
                        ],

                        "authentication": [
                            a.__name__
                            for a in authentication
                        ],

                        "throttle": [
                            t.__name__
                            for t in throttle
                        ],

                        "warnings":
                            warnings
                    })
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Error analyzing security for pattern {pattern}: {e}")

        elif isinstance(
            pattern,
            URLResolver
        ):

            walk_patterns(
                pattern.url_patterns,
                collected
            )

    return collected


def analyze_security():

    resolver = get_resolver()

    return walk_patterns(
        resolver.url_patterns
    )