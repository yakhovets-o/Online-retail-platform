from django.urls import (
    include,
    re_path,
)


"""
Available endpoints

- /users/
- /users/me/
- /users/resend_activation/
- /users/set_password/
- /users/reset_password/
- /users/reset_password_confirm/
- /users/set_username/
- /users/reset_username/
- /users/reset_username_confirm/
"""

urlpatterns = [
    re_path(r"^auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
]
