def build_graph(endpoints):

    nodes = []
    edges = []

    added_nodes = set()

    for endpoint in endpoints:

        view = endpoint.get("view")
        serializer = endpoint.get("serializers")
        model = endpoint.get("model")

        # VIEW NODE
        if view and view not in added_nodes:

            nodes.append({
                "id": view,
                "type": "view"
            })

            added_nodes.add(view)

        # SERIALIZER NODE
        if serializer and serializer not in added_nodes:

            nodes.append({
                "id": serializer,
                "type": "serializer"
            })

            added_nodes.add(serializer)

        # MODEL NODE
        if model and model not in added_nodes:

            nodes.append({
                "id": model,
                "type": "model"
            })

            added_nodes.add(model)

        # VIEW → SERIALIZER
        if view and serializer:

            edges.append({
                "source": view,
                "target": serializer
            })

        # SERIALIZER → MODEL
        if serializer and model:

            edges.append({
                "source": serializer,
                "target": model
            })

        # MODEL RELATIONSHIPS
        relationships = endpoint.get(
            "relationship",
            []
        )

        for rel in relationships:

            related_model = rel.get(
                "related_model"
            )

            rel_type = rel.get("type")

            if (
                related_model
                and related_model
                not in added_nodes
            ):

                nodes.append({
                    "id": related_model,
                    "type": "model"
                })

                added_nodes.add(
                    related_model
                )

            if model and related_model:

                edges.append({
                    "source": model,
                    "target": related_model,
                    "relation": rel_type
                })

    return {
        "nodes": nodes,
        "edges": edges
    }