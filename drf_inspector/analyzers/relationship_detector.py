from django.db.models import (
    ForeignKey,
    OneToOneField,
    ManyToManyField
)


IGNORE_FIELDS = [
    "groups",
    "user_permissions",
]


def detect_relationships(model):

    relationships = []

    if model is None:
        return relationships

    try:

        fields = model._meta.get_fields()

        for field in fields:

            if field.name in IGNORE_FIELDS:
                continue

            if isinstance(
                field,
                (
                    ForeignKey,
                    OneToOneField,
                    ManyToManyField
                )
            ):

                relationships.append({
                    "field": field.name,
                    "related_model": (
                        field.related_model.__name__
                    ),
                    "type": field.__class__.__name__
                })

    except Exception:
        pass

    return relationships