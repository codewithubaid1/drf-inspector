"""
URL configuration for DRF Visualizer views.

Includes routes for dashboard, analysis pages, and export functionality.
"""

from django.urls import path

from .views import (
    dashboard,
    urls_page,
    models_page,
    serializers_page,
    views_page,
    statistics_page,
    security_page,
    query_page,
    export_json_view,
    export_markdown_view,
)

app_name = "drf_inspector"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("urls/", urls_page, name="urls_page"),
    path("models/", models_page, name="models_page"),
    path("serializers/", serializers_page, name="serializers_page"),
    path("views/", views_page, name="views_page"),
    path("statistics/", statistics_page, name="statistics_page"),
    path("security/", security_page, name="security_page"),
    path("query-analysis/", query_page, name="query_page"),
    path("export/json/", export_json_view, name="export_json"),
    path("export/markdown/", export_markdown_view, name="export_markdown"),
]
