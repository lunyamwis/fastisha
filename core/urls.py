"""
Combined URLConf (core + Django-CRM)

- Keeps your public site routes (landing/dashboard/subscriptions/allauth)
- Adds Django-CRM routes (secret prefixes, voip, OAuth2 token view, contact form, rosetta, i18n)
- Serves MEDIA always in dev-style; serves STATIC only when DEBUG (matches your core file)
"""

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from common.views.favicon import FaviconRedirect
from crm.views.contact_form import contact_form
from massmail.views.get_oauth2_tokens import get_refresh_token


urlpatterns = [
    # --- Common / misc ---
    path("favicon.ico", FaviconRedirect.as_view()),

    # --- Your CORE site routes ---
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("apps.landing.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("subscriptions/", include("apps.subscriptions.urls")),

    # --- Django-CRM extra routes that are NOT behind i18n_patterns ---
    path("voip/", include("voip.urls")),
    path(
        "OAuth-2/authorize/",
        staff_member_required(get_refresh_token),
        name="get_refresh_token",
    ),
]

# Optional: Rosetta (translations UI)
if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [
        path("rosetta/", include("rosetta.urls")),
    ]

# CRM + related apps behind locale-aware URL patterns
urlpatterns += i18n_patterns(
    path(settings.SECRET_CRM_PREFIX, include("common.urls")),
    path(settings.SECRET_CRM_PREFIX, include("crm.urls")),
    path(settings.SECRET_CRM_PREFIX, include("massmail.urls")),
    path(settings.SECRET_CRM_PREFIX, include("tasks.urls")),
    path(settings.SECRET_ADMIN_PREFIX, admin.site.urls),
    path("contact-form/<uuid:uuid>/", contact_form, name="contact_form"),
)

# Static/media serving (development)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
