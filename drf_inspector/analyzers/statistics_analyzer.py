from django.apps import apps

from drf_inspector.analyzers.analyzer import (
    analyze_urls
)

from drf_inspector.analyzers.serializers_analyzer import (
    analyze_serializers
)


def analyze_statistics():

    endpoints = analyze_urls()

    serializers = analyze_serializers()

    models = apps.get_models()

    total_relationships = 0

    methods_count = {}

    for endpoint in endpoints:

        relationships = endpoint.get(
            "relationship",
            []
        )

        total_relationships += len(
            relationships
        )

        methods = endpoint.get(
            "methods",
            []
        )

        for method in methods:

            methods_count[method] = (
                methods_count.get(
                    method,
                    0
                ) + 1
            )

    return {

        "total_endpoints":
            len(endpoints),

        "total_serializers":
            len(serializers),

        "total_models":
            len(list(models)),

        "total_relationships":
            total_relationships,

        "methods":
            methods_count
    }