import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


PASSWORD_RULES = [
    (r".{8,}", "au moins 8 caractères"),
    (r"[A-Z]", "une majuscule"),
    (r"[a-z]", "une minuscule"),
    (r"[0-9]", "un chiffre"),
    (r"[^A-Za-z0-9]", "un caractère spécial"),
]


def validate_strong_password(password):
    errors = []
    for pattern, label in PASSWORD_RULES:
        if not re.search(pattern, password):
            errors.append(label)
    if errors:
        raise ValidationError(
            _("Le mot de passe doit contenir : %(rules)s."),
            params={"rules": ", ".join(errors)},
        )


class StrongPasswordValidator:
    """Validateur AUTH_PASSWORD_VALIDATORS de Django."""

    def validate(self, password, user=None):
        validate_strong_password(password)

    def get_help_text(self):
        return _(
            "Votre mot de passe doit contenir au moins 8 caractères, "
            "une majuscule, une minuscule, un chiffre et un caractère spécial."
        )
