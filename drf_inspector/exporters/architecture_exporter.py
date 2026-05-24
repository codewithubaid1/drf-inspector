import json

from drf_inspector.analyzers.analyzer import (
    analyze_urls
)

from drf_inspector.analyzers.project_structure_analyzer import (
    analyze_project_structure
)

from drf_inspector.analyzers.serializers_analyzer import (
    analyze_serializers
)

from drf_inspector.analyzers.views_analyzer import (
    analyze_views
)


def build_architecture_data():

    return {

        "project": analyze_project_structure(),
        "urls": analyze_urls(),

        "serializers": analyze_serializers(),

        "views": analyze_views()
    }



def export_json():

    return json.dumps(
        build_architecture_data(),
        indent=4
    )
def export_markdown():

    data = build_architecture_data()

    markdown = "# DRF Architecture Report\n\n"

    # =====================================================
    # PROJECT INFO
    # =====================================================

    project = data.get("project", {})

    markdown += "## Project Information\n\n"

    markdown += (
        f"Project Name: "
        f"{project.get('project_name')}\n\n"
    )

    markdown += "### Installed Apps\n\n"

    for app in project.get(
        "installed_apps",
        []
    ):

        markdown += f"- {app}\n"

    markdown += "\n"


    # =====================================================
    # PROJECT STRUCTURE
    # =====================================================

    markdown += "## Project Structure\n\n"


    def render_tree(
        items,
        level=0
    ):

        tree = ""

        indent = "  " * level

        for item in items:

            icon = (
                "📁"
                if item["type"] == "folder"
                else "📄"
            )

            tree += (
                f"{indent}- "
                f"{icon} "
                f"{item['name']}\n"
            )

            if (
                item["type"] == "folder"
                and "children" in item
            ):

                tree += render_tree(
                    item["children"],
                    level + 1
                )

        return tree


    markdown += "```text\n"

    markdown += render_tree(
        project.get(
            "structure",
            []
        )
    )

    markdown += "```\n\n"


    # =====================================================
    # URLS
    # =====================================================

    markdown += "## API Endpoints\n\n"

    for endpoint in data.get(
        "urls",
        []
    ):

        markdown += (
            f"- "
            f"{endpoint.get('path')} "
            f"({endpoint.get('view')})\n"
        )

    markdown += "\n"


    # =====================================================
    # VIEWS
    # =====================================================

    markdown += "## Views\n\n"

    for view in data.get(
        "views",
        []
    ):

        markdown += (
            f"### "
            f"{view.get('view')}\n"
        )

        markdown += (
            f"Path: "
            f"{view.get('path')}\n\n"
        )

        methods = ", ".join(
            view.get(
                "methods",
                []
            )
        )

        markdown += (
            f"Methods: "
            f"{methods}\n\n"
        )


    # =====================================================
    # SERIALIZERS
    # =====================================================

    markdown += "## Serializers\n\n"

    for serializer in data.get(
        "serializers",
        []
    ):

        markdown += (
            f"### "
            f"{serializer.get('name')}\n\n"
        )

        model = serializer.get("model")

        if model:

            markdown += (
                f"Model: "
                f"{model}\n\n"
            )

        markdown += "#### Fields\n\n"

        for field in serializer.get(
            "fields",
            []
        ):

            markdown += (
                f"- "
                f"{field.get('name')} "
                f"({field.get('type')})"
            )

            if field.get(
                "nested_serializer"
            ):

                markdown += (
                    f" → Nested: "
                    f"{field.get('nested_serializer')}"
                )

            if field.get("many"):

                markdown += (
                    " [many=True]"
                )

            markdown += "\n"

        markdown += "\n"

    return markdown