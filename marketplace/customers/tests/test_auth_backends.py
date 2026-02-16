import pytest
from unittest.mock import MagicMock
from customers.auth_backends import CustomOIDCBackend
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def oidc_backend():
    # We initialize the backend with a dummy request
    return CustomOIDCBackend(MagicMock())

@pytest.mark.django_db
def test_create_user_from_oidc_claims(oidc_backend):
    """Test that the backend correctly creates a user from OIDC claims"""
    
    # Simulate the dictionary of data Google returns
    claims = {
        "email": "patrick@example.com",
        "name": "Patrick Test",
        "picture": "http://example.com/photo.jpg"
    }

    # Execute the backend logic
    user = oidc_backend.create_user(claims)

    # Assertions
    assert user.email == "patrick@example.com"
    assert user.username == "patrick@example.com"
    assert user.first_name == "Patrick Test"
    assert user.profile_picture == "http://example.com/photo.jpg"
    assert len(user.code) == 8  # Verify our 8-char uuid logic
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_update_user_from_oidc_claims(oidc_backend):
    """Test that existing users get their profile updated on login"""
    
    # 1. Pre-create a user
    user = User.objects.create_user(
        username="patrick@example.com", 
        email="old@email.com",
        first_name="Old Name",
        code="OLDCODE1"
    )

    # 2. Simulate new data from OIDC provider
    new_claims = {
        "email": "patrick@example.com",
        "name": "New Patrick",
        "picture": "http://newphoto.com"
    }

    # Execute update logic
    updated_user = oidc_backend.update_user(user, new_claims)

    # Assertions
    assert updated_user.first_name == "New Patrick"
    assert updated_user.profile_picture == "http://newphoto.com"
    # Ensure code wasn't changed (it should stay persistent)
    assert updated_user.code == "OLDCODE1"