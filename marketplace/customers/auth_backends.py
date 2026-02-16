import uuid
from django.contrib.auth import get_user_model
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

User = get_user_model()

class CustomOIDCBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        email = claims.get("email")
        name = claims.get("name", "")
        picture = claims.get("picture", "")

        # Print lengths and values
        print("username:", email, len(email))
        print("first_name:", name, len(name))
        print("last_name:", "", len(""))
        print("email:", email, len(email))
        print("code:", unique_code, len(unique_code))

        # Generate a unique code
        unique_code = str(uuid.uuid4())[:8]  # 8-char unique code

        user = User.objects.create(
            username=email,
            email=email,
            first_name=name,
            profile_picture=picture,
            code=unique_code,  # must be unique
        )
        return user

    def update_user(self, user, claims):
        user.first_name = claims.get("name", user.first_name)
        user.email = claims.get("email", user.email)
        user.profile_picture = claims.get("picture", user.profile_picture)
        user.save()
        return user
