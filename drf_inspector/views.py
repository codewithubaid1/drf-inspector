import logging
from django.shortcuts import render
from django.http import HttpResponse

from drf_inspector.analyzers.query_analyzer import analyze_queries
from drf_inspector.exporters.architecture_exporter import export_json, export_markdown
from drf_inspector.analyzers.security_analyzer import analyze_security
from drf_inspector.analyzers.statistics_analyzer import analyze_statistics
from drf_inspector.analyzers.analyzer import analyze_urls
from drf_inspector.analyzers.views_analyzer import analyze_views
from drf_inspector.analyzers.models_analyzer import analyze_models
from drf_inspector.analyzers.serializers_analyzer import analyze_serializers

logger = logging.getLogger(__name__)


def visualizer_home(request):
    return render(request, "drf_inspector/index.html")


def urls_page(request):
    try:
        endpoints = analyze_urls()
    except Exception as e:
        logger.error(f"Error analyzing URLs: {e}", exc_info=True)
        endpoints = []

    return render(request, "drf_inspector/urls.html", {"endpoints": endpoints})


def models_page(request):
    try:
        graph = analyze_models()
    except Exception as e:
        logger.error(f"Error analyzing models: {e}", exc_info=True)
        graph = {"nodes": [], "edges": []}

    return render(request, "drf_inspector/models.html", {"graph": graph})


def serializers_page(request):
    try:
        serializers = analyze_serializers()
    except Exception as e:
        logger.error(f"Error analyzing serializers: {e}", exc_info=True)
        serializers = []

    return render(request, "drf_inspector/serializers.html", {"serializers": serializers})


def views_page(request):
    try:
        views = analyze_views()
    except Exception as e:
        logger.error(f"Error analyzing views: {e}", exc_info=True)
        views = []

    return render(request, "drf_inspector/views.html", {"views": views})


def statistics_page(request):
    try:
        stats = analyze_statistics()
    except Exception as e:
        logger.error(f"Error analyzing statistics: {e}", exc_info=True)
        stats = {
            "total_endpoints": 0,
            "total_serializers": 0,
            "total_models": 0,
            "total_relationships": 0,
            "methods": {}
        }

    return render(request, "drf_inspector/statistics.html", {"stats": stats})


def security_page(request):
    try:
        endpoints = analyze_security()
    except Exception as e:
        logger.error(f"Error analyzing security: {e}", exc_info=True)
        endpoints = []

    return render(request, "drf_inspector/security.html", {"endpoints": endpoints})


def query_page(request):
    try:
        endpoints = analyze_queries()
    except Exception as e:
        logger.error(f"Error analyzing queries: {e}", exc_info=True)
        endpoints = []

    return render(request, "drf_inspector/query_analysis.html", {"endpoints": endpoints})


def export_json_view(request):
    try:
        data = export_json()
    except Exception as e:
        logger.error(f"Error exporting JSON: {e}", exc_info=True)
        data = "{}"

    response = HttpResponse(data, content_type="application/json")
    response["Content-Disposition"] = "attachment; filename=architecture.json"
    return response


def export_markdown_view(request):
    try:
        data = export_markdown()
    except Exception as e:
        logger.error(f"Error exporting markdown: {e}", exc_info=True)
        data = "# Error\nCould not generate architecture markdown."

    response = HttpResponse(data, content_type="text/markdown")
    response["Content-Disposition"] = "attachment; filename=architecture.md"
    return response


def dashboard(request):
    return render(request, "drf_inspector/dashboard.html")
