from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("inscription/", views.register_view, name="register"),
    path("connexion/", views.login_view, name="login"),
    path("deconnexion/", views.logout_view, name="logout"),
    path("tableau-de-bord/", views.dashboard_view, name="dashboard"),
    path("profil/", views.profile_view, name="profile"),
    path("profil/modifier/", views.profile_edit_view, name="profile_edit"),
    path("mot-de-passe/", views.password_change_view, name="password_change"),
    path("admin/utilisateurs/", views.manage_users_view, name="manage_users"),
    path(
        "admin/utilisateurs/<int:pk>/modifier/",
        views.user_edit_view,
        name="user_edit",
    ),
    path(
        "admin/utilisateurs/<int:pk>/activer/",
        views.user_toggle_active_view,
        name="user_toggle_active",
    ),
]
