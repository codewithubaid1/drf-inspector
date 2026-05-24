def detect_model(callback):

    if not hasattr(callback, "cls"):
        return None

    view_class = callback.cls

    # CASE 1:
    # queryset = Post.objects.all()

    if hasattr(view_class, "queryset"):

        queryset = view_class.queryset

        if queryset is not None:

            try:
                return queryset.model
            except Exception:
                pass

    # CASE 2:
    # serializer Meta.model

    if hasattr(view_class, "serializer_class"):

        serializer = (
            view_class.serializer_class
        )

        if serializer:

            try:

                meta = serializer.Meta

                if hasattr(meta, "model"):

                    return meta.model

            except Exception:
                pass

    return None