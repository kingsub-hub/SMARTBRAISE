from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.validators import validate_email

from .models import Profile, User
from .validators import validate_strong_password

REGISTRATION_ROLES = (
    User.Role.VIEWER,
    User.Role.STUDENT,
    User.Role.EDITOR,
)


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"


class RegistrationForm(BootstrapFormMixin, forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Mot de passe",
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirmer le mot de passe",
    )
    accept_terms = forms.BooleanField(
        required=True,
        label="J'accepte les conditions générales",
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].choices = [
            (role.value, role.label) for role in REGISTRATION_ROLES
        ]
        self.fields["role"].initial = User.Role.VIEWER
        self.fields["email"].widget.attrs["placeholder"] = "vous@exemple.com"

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        validate_email(email)
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            validate_strong_password(password)
        return password

    def clean_role(self):
        role = self.cleaned_data.get("role")
        allowed = {r.value for r in REGISTRATION_ROLES}
        if role not in allowed:
            raise forms.ValidationError(
                "Ce rôle n'est pas disponible à l'inscription."
            )
        return role

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get("password")
        confirm = cleaned.get("password_confirm")
        if pwd and confirm and pwd != confirm:
            self.add_error(
                "password_confirm", "Les mots de passe ne correspondent pas."
            )
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.email.lower()
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            Profile.objects.get_or_create(user=user)
        return user


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        label="Se souvenir de moi",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Adresse email"
        self.fields["username"].widget.attrs.update(
            {
                "placeholder": "vous@exemple.com",
                "autocomplete": "email",
            }
        )
        self.fields["password"].widget.attrs["autocomplete"] = "current-password"

    def clean_username(self):
        return self.cleaned_data.get("username", "").strip().lower()

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if email and password:
            self.user_cache = authenticate(
                self.request,
                username=email,
                password=password,
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Email ou mot de passe incorrect.",
                    code="invalid_login",
                )
            if not self.user_cache.is_active:
                raise forms.ValidationError(
                    "Ce compte est désactivé.",
                    code="inactive",
                )
            self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class ProfileUserForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone", "date_of_birth", "bio", "avatar")
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "bio": forms.Textarea(attrs={"rows": 3}),
        }


class ProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("address", "city", "country", "zip_code")


class UserEditForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("role", "is_active")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].choices = User.Role.choices


class CustomPasswordChangeForm(BootstrapFormMixin, PasswordChangeForm):
    def clean_new_password1(self):
        password = super().clean_new_password1()
        validate_strong_password(password)
        return password
