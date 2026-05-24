from rest_framework.serializers import (
    BaseSerializer
)

from django.apps import apps


def analyze_serializers():

    serializers_data = []

    visited = set()

    for model in apps.get_models():

        app_name = (
            model.__module__
            .split(".")[0]
        )

        try:

            serializers_module = __import__(
                f"{app_name}.serializers",
                fromlist=["*"]
            )

        except Exception:
            continue

        for attr_name in dir(serializers_module):

            attr = getattr(
                serializers_module,
                attr_name
            )

            try:

                if not (
                    isinstance(attr, type)
                    and issubclass(
                        attr,
                        BaseSerializer
                    )
                ):
                    continue

                if attr in visited:
                    continue

                visited.add(attr)

                serializer = attr()

                fields_data = []

                for (
                    field_name,
                    field
                ) in serializer.fields.items():

                    nested_serializer = None

                    many = False

                    if isinstance(
                        field,
                        BaseSerializer
                    ):

                        nested_serializer = (
                            field.__class__.__name__
                        )

                        many = getattr(
                            field,
                            "many",
                            False
                        )

                    field_data = {

                        "name":
                            field_name,

                        "type":
                            field.__class__.__name__,

                        "nested_serializer":
                            nested_serializer,

                        "many":
                            many,

                        "read_only":
                            field.read_only,

                        "write_only":
                            field.write_only
                    }

                    fields_data.append(
                        field_data
                    )

                model_name = None

                relationships = []

                meta = getattr(
                    attr,
                    "Meta",
                    None
                )

                if (
                    meta
                    and hasattr(
                        meta,
                        "model"
                    )
                ):

                    model = meta.model

                    model_name = (
                        model.__name__
                    )

                    for field in (
                        model._meta.get_fields()
                    ):

                        if (
                            field.is_relation
                        ):

                            relationships.append({

                                "field":
                                    field.name,

                                "related_model":
                                    field.related_model.__name__,

                                "type":
                                    field.__class__.__name__
                            })

                serializers_data.append({

                    "name":
                        attr.__name__,

                    "model":
                        model_name,

                    "relationships":
                        relationships,

                    "fields":
                        fields_data
                })

            except Exception:
                continue

    return serializers_data