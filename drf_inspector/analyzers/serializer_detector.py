def detect_serializer(callback):

    # ViewSets / APIViews
    if hasattr(callback, "cls"):

        view_class = callback.cls

        # serializer_class
        if hasattr(view_class, "serializer_class"):

            serializer = (
                view_class.serializer_class
            )

            if serializer:
                return serializer

        # get_serializer_class
        if hasattr(view_class, "get_serializer_class"):

            try:

                view_instance = view_class()

                serializer = (
                    view_instance.get_serializer_class()
                )

                if serializer:
                    return serializer

            except Exception:
                pass

    return None