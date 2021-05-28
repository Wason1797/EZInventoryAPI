
def test_create_user(create_user):
    user = create_user.json()
    assert user
    assert 'password' not in user
    assert create_user.status_code == 200


def test_get_user_by_uuid(client, create_user):
    user = create_user.json()
    response = client.get(
        f"/user/{user['uuid']}"
    )
    response_user = response.json()
    assert response.status_code == 200
    assert 'password' not in response_user
    for key in user:
        assert response_user[key] == user[key]


def test_user_basic_update(client, create_user):
    new_phone = '0123456789'
    user = create_user.json()
    response = client.patch(
        '/user',
        json={
            'uuid': user['uuid'],
            'phone': new_phone
        }
    )
    updated_user = response.json()
    assert response.status_code == 200
    assert updated_user['phone'] == new_phone


def test_delete_user(client, create_user):
    user = create_user.json()
    uri = f"/user/{user['uuid']}"
    response = client.delete(uri)
    check_deleted_user = client.get(uri)
    assert response.status_code == 200
    assert response.json()['uuid'] == user['uuid']
    assert not check_deleted_user.json()


def test_get_tenants_related_to_user(client, create_user):
    user = create_user.json()
    response = client.get(f"/user/{user['uuid']}/tenants")
    tenants = response.json()
    assert response.status_code == 200
    assert isinstance(tenants, list)
    assert len(tenants) > 0
