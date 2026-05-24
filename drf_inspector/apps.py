"""
Django app configuration for DRF Visualizer.
"""

from django.apps import AppConfig


class DrfVisualizerConfig(AppConfig):
    """
    Configuration class for the DRF Visualizer Django application.
    Provides visualization tools for Django REST Framework architecture.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "drf_inspector"
    verbose_name = "DRF Visualizer"