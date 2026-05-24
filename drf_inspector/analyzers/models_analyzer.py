from django.apps import apps

from django.db.models import (
    ForeignKey,
    OneToOneField,
    ManyToManyField
)


IGNORE_MODELS = [
    "Permission",
    "Group",
    "ContentType",
    "Session",
    "LogEntry",
]


def analyze_models():

    nodes = []

    edges = []

    added_models = set()

    models = apps.get_models()

    for model in models:
        try:
            model_name = model.__name__

            if model_name in IGNORE_MODELS:
                continue

            # ADD NODE
            if model_name not in added_models:

                nodes.append({
                    "id": model_name
                })

                added_models.add(model_name)

            # RELATIONSHIPS
            fields = model._meta.get_fields()

            for field in fields:

                if isinstance(
                    field,
                    (
                        ForeignKey,
                        OneToOneField,
                        ManyToManyField
                    )
                ):

                    related_model = (
                        field.related_model.__name__
                    )

                    if (
                        related_model
                        in IGNORE_MODELS
                    ):
                        continue

                    edges.append({
                        "source": model_name,
                        "target": related_model,
                        "label": field.name,
                        "type": (
                            field.__class__.__name__
                        )
                    })
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Error analyzing model {model}: {e}")

    return {
        "nodes": nodes,
        "edges": edges
    }