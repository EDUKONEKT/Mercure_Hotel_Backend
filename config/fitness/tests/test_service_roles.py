import pytest
from rest_framework import status
from core.tests.test_utils import create_user_with_role, get_auth_headers
from accounts.models import AccountType
from fitness.models import Fitness, FitnessBooking

# ---------------------------------------------------------------------
# 🔧  FIXTURES GÉNÉRIQUES
# ---------------------------------------------------------------------

@pytest.fixture
def api_client(client):
    """Client REST Framework standard"""
    return client

@pytest.fixture
def sample_fit():
    """Crée un service de base pour les tests"""
    return Fitness.objects.create(price=50.0, is_available=True, type="fitness",flour=1, number=1, max_pers=30)

@pytest.fixture
def booking_url():
    return "/api/fitness/fitness-bookings/"

@pytest.fixture
def service_url():
    return "/api/fitness/fitness/"

# ---------------------------------------------------------------------
# 🧪 TESTS DES SERVICES (CRUD DES ADMIN)
# ---------------------------------------------------------------------

@pytest.mark.django_db
@pytest.mark.parametrize("role, method, expected_status", [
    (AccountType.ADMIN, "post", status.HTTP_201_CREATED),
    (AccountType.ADMIN, "put", status.HTTP_200_OK),
    (AccountType.ADMIN, "delete", status.HTTP_204_NO_CONTENT),
    (AccountType.CLIENT, "post", status.HTTP_403_FORBIDDEN),
    (AccountType.CLIENT, "delete", status.HTTP_403_FORBIDDEN),
    (AccountType.RECEPTIONIST, "post", status.HTTP_403_FORBIDDEN),
])
def test_service_permissions(api_client, role, method, expected_status, service_url):
    """Test global pour créer/modifier/supprimer un service (Spa, Sauna, Room, etc.)"""
    user = create_user_with_role(f"user_{role}", role)
    headers = get_auth_headers(user)
    data = {"price": 99.0, "is_available": True, "type": "fitness" , "flour":1, "number":1, "max_pers":30}

    # Exécute la bonne méthode HTTP
    func = getattr(api_client, method)
    if method == "put":
        # on crée un service d'abord, puis on le modifie
        fit = Fitness.objects.create(price=50.0, is_available=True, type="fitness",flour=1, number=1, max_pers=30)
        url = f"{service_url}{fit.id}/"
        response = func(url, {"price": 120.0, "is_available": True,"type":"fitness","flour":1, "number":1, "max_pers":30}, content_type='application/json', **headers)
    elif method == "delete":
        fit = Fitness.objects.create(price=50.0, is_available=True, type="fitness",flour=1, number=1, max_pers=30)
        url = f"{service_url}{fit.id}/"
        response = func(url, **headers)
    else:
        response = func(service_url, data, content_type='application/json', **headers)

    assert response.status_code == expected_status


@pytest.mark.django_db
def test_anyone_can_list_services(api_client, service_url):
    """Vérifie que tout le monde (même non authentifié) peut lire les services"""
    Fitness.objects.create(price=40.0, is_available=True, type="fitness", flour=1, number=1, max_pers=30)
    response = api_client.get(service_url)
    assert response.status_code == 200
    assert len(response.data) > 0


# ---------------------------------------------------------------------
# 🧪 TESTS DES BOOKINGS (RÉSERVATIONS)
# ---------------------------------------------------------------------

@pytest.mark.django_db
@pytest.mark.parametrize("role, expected_status", [
    (AccountType.ADMIN, status.HTTP_201_CREATED),
    (AccountType.RECEPTIONIST, status.HTTP_201_CREATED),
    (AccountType.CLIENT, status.HTTP_201_CREATED),
])
def test_create_booking_by_role(api_client, sample_fit, role, expected_status, booking_url):
    """Vérifie qui peut créer une réservation"""
    user = create_user_with_role(f"user_{role}", role)
    headers = get_auth_headers(user)
    data = {"fitness": sample_fit.id, "check_in": "2025-11-01", "check_out": "2025-11-02"}

    response = api_client.post(booking_url, data, content_type='application/json', **headers)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize("role, expected_status", [
    (AccountType.ADMIN, status.HTTP_204_NO_CONTENT),
    (AccountType.RECEPTIONIST, status.HTTP_204_NO_CONTENT),
    (AccountType.CLIENT, status.HTTP_403_FORBIDDEN),  # ne peut pas supprimer une réservation d’autrui
])
def test_delete_booking_permissions(api_client, sample_fit, role, expected_status, booking_url):
    """Vérifie que seul admin et réceptionniste peuvent supprimer"""
    # Crée la réservation par un autre utilisateur
    owner = create_user_with_role("owner_client", AccountType.CLIENT)
    owner_account = owner.account
    booking = FitnessBooking.objects.create(fitness=sample_fit, account=owner_account,
                                        check_in="2025-11-01", check_out="2025-11-02", total_price=100)
    user = create_user_with_role(f"user_{role}", role)
    headers = get_auth_headers(user)

    url = f"{booking_url}{booking.id}/"
    response = api_client.delete(url, **headers)
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_receptionist_can_create_booking_for_client(api_client, sample_fit, booking_url):
    receptionist = create_user_with_role("reception", AccountType.RECEPTIONIST)
    client = create_user_with_role("client_user", AccountType.CLIENT)
    headers = get_auth_headers(receptionist)
    data = {
        "fitness": sample_fit.id,
        "account": client.account.id,  # 👈 il indique pour qui
        "check_in": "2025-11-05",
        "check_out": "2025-11-07"
    }

    response = api_client.post(booking_url, data, content_type="application/json", **headers)
    assert response.status_code == 201
    assert  float(response.data["total_price"]) == sample_fit.price * 2

