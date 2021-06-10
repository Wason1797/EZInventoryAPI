import pytest

from app.tests.test_utils.mocks import mock_address


def test_create_provider(create_provider):
    provider = create_provider.json()
    assert provider
    assert create_provider.status_code == 200


def test_get_provider_by_uuid(client, create_provider):
    provider = create_provider.json()
    response = client.get(
        f"/provider/{provider['uuid']}"
    )
    response_provider = response.json()
    assert response.status_code == 200
    assert 'password' not in response_provider
    for key in provider:
        assert response_provider[key] == provider[key]


@pytest.mark.parametrize('update_values', [
    {'phone': '0123456789'},
    {'main_address': mock_address()},
    {'description': 'new description'},
    {'phone': '0123456789',
     'main_address': mock_address(),
     'description': 'new_description',
     'meta': {'new_meta': 'new_meta'}},
])
def test_provider_basic_update(client, create_provider, update_values):
    provider = create_provider.json()
    response = client.patch(
        '/provider',
        json={
            'uuid': provider['uuid'],
            **update_values
        }
    )
    updated_provider = response.json()
    assert response.status_code == 200
    for key, value in update_values.items():
        assert key in updated_provider
        assert updated_provider[key] == value


def test_delete_provider(client, create_provider):
    provider = create_provider.json()
    uri = f"/provider/{provider['uuid']}"
    response = client.delete(uri)
    check_deleted_provider = client.get(uri)
    assert response.status_code == 200
    assert response.json()['uuid'] == provider['uuid']
    assert not check_deleted_provider.json()
