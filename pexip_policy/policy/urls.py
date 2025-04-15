from django.urls import path
from . import views

urlpatterns = [
    path("policy/v1/service/configuration", views.service_configuration, name="service_configuration"),
    path("policy/v1/participant/properties", views.participant_properties, name="participant_properties"),
    path("policy/v1/registrations/<path:alias>", views.registration_policy, name="registration_policy"),
]
