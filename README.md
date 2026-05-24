<p align="center">
  <img src="https://raw.githubusercontent.com/codewithubaid1/drf-inspector/main/screenshots/dashboard.png" width="900">
</p>

# DRF Inspector

DRF Inspector is a powerful developer tool for analyzing, visualizing, and understanding Django REST Framework (DRF) backends.

It automatically inspects your project architecture and provides interactive visualizations for:

- API endpoints
- serializers
- models
- relationships
- views
- query optimization
- security analysis
- architecture exporting

DRF Inspector helps developers debug, document, optimize, and better understand complex DRF projects.

---

# ✨ Features

## 🌐 API & URL Analysis
- Inspect all DRF endpoints automatically
- Detect HTTP methods (`GET`, `POST`, `PATCH`, etc.)
- View connected views and serializers
- Search and filter endpoints

## 🧠 Model Visualization
- Auto-generate model relationship graphs
- Visualize:
  - `ForeignKey`
  - `ManyToManyField`
  - `OneToOneField`
- Interactive relationship mapping

## 🔍 Serializer Inspection
- Detect serializers used in views
- Inspect serializer fields
- Detect nested serializers
- Show serializer → model mappings

## 🧭 View Analysis
- Analyze:
  - authentication classes
  - permission classes
  - pagination
  - throttling
  - filtering
- Supports DRF class-based views and ViewSets

## 🔒 Security Audit
- Detect endpoints missing:
  - authentication
  - permissions
  - throttling
- Helps identify insecure API routes

## ⚡ Query Optimization Detection
- Detect possible N+1 query issues
- Suggest:
  - `select_related`
  - `prefetch_related`
- Analyze queryset optimization opportunities

## 📦 Exporting
Export project architecture as:
- JSON
- Markdown

Useful for:
- documentation
- architecture reviews
- team sharing
- AI context sharing

## 🖥️ Interactive Dashboard
- Built directly into Django
- No React required
- No external frontend setup
- Works instantly inside your project

---

## 🔗 Links
- GitHub: https://github.com/codewithubaid1/drf-inspector
- PyPI: https://pypi.org/project/drf-inspector/
---


# 📸 Screenshots

## Dashboard

<p align="center">
  <img src="https://raw.githubusercontent.com/codewithubaid1/drf-inspector/main/screenshots/dashboard.png" width="900">
</p>

## URL Explorer

<p align="center">
  <img src="https://raw.githubusercontent.com/codewithubaid1/drf-inspector/main/screenshots/urls.png" width="900">
</p>

## Model Relationships

<p align="center">
  <img src="https://raw.githubusercontent.com/codewithubaid1/drf-inspector/main/screenshots/models.png" width="900">
</p>

## Serializer Inspector

<p align="center">
  <img src="https://raw.githubusercontent.com/codewithubaid1/drf-inspector/main/screenshots/serializers.png" width="900">
</p>

## Query Optimization

<p align="center">
  <img src="https://raw.githubusercontent.com/codewithubaid1/drf-inspector/main/screenshots/optimization.png" width="900">
</p>

---

# ⚡ Installation

## Step 1: Install the package
```bash
pip install drf-inspector==0.1.3
```

## Step 2: Add in settings.py:
```
installed_apps = [
  drf_inspector,
   ....
]
```
## Step 3: Add in project urls.py:

```
from django.urls import path, include
urlpatterns = [
  ...,
  path("drf-inspector/",include("drf_inspector.urls")),
]
```


## Final Step : Go to the url and that's it:
```
   http://127.0.0.1:8000/drf-inspector/
```




