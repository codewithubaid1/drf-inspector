from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver
from drf_inspector.analyzers.serializer_detector import (
    detect_serializer
)
from drf_inspector.analyzers.model_detector import (
    detect_model
)
from drf_inspector.analyzers.relationship_detector import (
    detect_relationships
)

def get_methods(callback):
    """
    Detect HTTP methods for:
    - APIView
    - GenericAPIView
    - ViewSets
    - @api_view function views
    """

    methods = []

    # DRF ViewSets
    if hasattr(callback, "actions"):

        methods = [
            method.upper()
            for method in callback.actions.keys()
        ]

        return methods

    # APIView / GenericAPIView / api_view
    if hasattr(callback, "cls"):

        try:

            view_class = callback.cls

            view_instance = view_class()

            methods = [
                method
                for method in view_instance.allowed_methods
                if method not in ["OPTIONS", "HEAD"]
            ]

            return methods

        except Exception:
            return []

    return []


def walk_patterns(urlpatterns, prefix=""):

    collected = []

    for pattern in urlpatterns:

        # NORMAL ENDPOINT
        if isinstance(pattern, URLPattern):
            try:
                path = prefix + str(pattern.pattern)

                # Skip unwanted urls
                if path.startswith("admin"):
                    continue

                if path.startswith("^media"):
                    continue
                    
                if "drf-inspector" in path or "drf_inspector" in path:
                    continue

                endpoint = {
                    "path": path,
                }

                callback = pattern.callback
                
                # Skip drf_inspector's own views
                callback_module = getattr(callback, "__module__", "")
                if callback_module.startswith("drf_inspector"):
                    continue

                
                serializer = detect_serializer(callback)
                if serializer:
                    endpoint["serializers"] = serializer.__name__
                model = detect_model(callback)
                if model:
                    endpoint["model"] = model.__name__
                    endpoint["relationship"] = detect_relationships(model)
                
                parts = path.split("/")

                if len(parts) > 2:
                  endpoint["app"] = parts[2]


                # Detect class/function view
                if hasattr(callback, "cls"):

                    endpoint["view"] = (
                        callback.cls.__name__
                    )

                else:

                    endpoint["view"] = str(callback)

                # Detect methods
                endpoint["methods"] = (
                    get_methods(callback)
                )

                collected.append(endpoint)
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Error analyzing URL pattern {pattern}: {e}")
        
        

        # INCLUDED URLS
        elif isinstance(pattern, URLResolver):

            nested_patterns = walk_patterns(
                pattern.url_patterns,
                prefix + str(pattern.pattern)
            )

            collected.extend(nested_patterns)

    return collected


def analyze_urls():

    resolver = get_resolver()

    return walk_patterns(
        resolver.url_patterns
    )