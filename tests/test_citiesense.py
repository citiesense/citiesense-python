from pytest import fixture
import pytest
import vcr
from datetime import datetime
from citiesense import Client

comm_id = 1
key = "demo"
instance = Client(key=key, host="https://api.citiesense.dev", verify=False)

my_vcr = vcr.VCR(cassette_library_dir="tests/cassettes", filter_headers=["X-Api-Key"])


@fixture
def business_fields():
    return ["address"]


@fixture
def event_fields():
    return ["address"]


@fixture
def community_keys():
    return ["id"]


@my_vcr.use_cassette("community.yml")
def test_community(community_keys, business_fields, event_fields):
    """Tests an API call to get a Community's info"""
    response = instance.community(comm_id).get()
    assert isinstance(response, dict)
    assert set(community_keys).issubset(
        response.keys()
    ), "All keys should be in the response"
    assert set(business_fields).issubset(
        response["fields"]["businesses"]
    ), "All business fields should be in the response"

    assert set(event_fields).issubset(
        response["fields"]["events"]
    ), "All event fields should be in the response"


@my_vcr.use_cassette("businesses.yml")
def test_businesses():
    """Tests an API call to get a list of businesses for a community."""
    response = instance.community(comm_id).businesses().get(params={"fields": ["name"]})
    assert isinstance(response, list)
    for item in response:
        assert "id" in item, "Id key should be present in response"
        assert "lon" in item, "lon key should be present in response"
        assert "lat" in item, "lat key should be present in response"
        assert "name" in item, "Name key should be present in response"


@my_vcr.use_cassette("business.yml")
def test_business():
    """Tests an API call to get a list of businesses for a community."""
    items = instance.community(comm_id).businesses()
    id = items.get()[0]["id"]
    response = items.get(id, params={"fields": ["address"]})
    assert isinstance(response, dict)
    assert response["id"] == id
    assert "address" in response, "Address key should be present in response"


@my_vcr.use_cassette("events.yml")
def test_events():
    """Tests an API call to get a list of events for a community."""
    response = instance.community(comm_id).events().get(params={"fields": ["address"]})
    assert isinstance(response, list)
    for item in response:
        assert "id" in item, "Id key should be present in response"
        assert "lon" in item, "lon key should be present in response"
        assert "lat" in item, "lat key should be present in response"
        assert "address" in item, "Address key should be present in response"


@my_vcr.use_cassette("event.yml")
def test_event():
    """Tests an API call to get a list of events for a community."""
    items = instance.community(comm_id).events()
    id = items.get()[0]["id"]
    response = items.get(id, params={"fields": ["address"]})
    assert isinstance(response, dict)
    assert response["id"] == id
    assert "address" in response, "Address key should be present in response"


@my_vcr.use_cassette("create_event.yml")
def test_create_event():
    """Tests an API call to create an event for a community."""
    items = instance.community(comm_id).events()

    name = "foo"
    lon = -70
    lat = 40
    address = '123 Shadwad'
    category = "Foo"
    subcategories = ["Bar1", "Bar2"]
    tags = ["Tag1", "Tag2"]
    starts_at = datetime(2018, 4, 9, 13, 37, 0).utcnow().isoformat()
    ends_at = datetime(2018, 5, 9, 13, 37, 0).utcnow().isoformat()

    resource = {
        "name": name,
        "address": address,
        "lon": lon,
        "lat": lat,
        "the_geom": f"POINT ({lon} {lat})",
        "category": category,
        "subcategories": subcategories,
        "tags": tags,
        "starts_at": starts_at,
        "ends_at": ends_at,
    }

    post_response = None
    post_response = items.post(data={"resource": resource})
    id = post_response["id"]
    response = items.get(id, params={"fields": ["address"]})
    assert post_response["success"] == True
    assert response["id"] == id
    assert "address" in response, "Address key should be present in response"

    name2 = 'bar'
    resource = {
      "name": name2
    }

    put_response = items.put(id, data={"resource": resource})
    assert put_response["success"] == True

    # Test update workflow
    response = items.get(id, params={"fields": ["name"]})
    assert response["name"] == name2

    # Test delete workflow
    delete_response = items.delete(id)
    assert delete_response["success"] == True


@my_vcr.use_cassette("create_business.yml")
def test_create_business():
    """Tests an API call to create a business for a community."""
    items = instance.community(comm_id).businesses()

    name = "foo"
    lon = -70
    lat = 40
    address = '124 Shadwad'
    category = "Foo"
    subcategories = ["Bar1", "Bar2"]
    tags = ["Tag1", "Tag2"]

    resource = {
        "name": name,
        "address": address,
        "lon": lon,
        "lat": lat,
        "the_geom": f"POINT ({lon} {lat})",
        "category": category,
        "subcategories": subcategories,
        "tags": tags,
    }

    post_response = items.post(data={"resource": resource})
    id = post_response["id"]
    response = items.get(id, params={"fields": ["address"]})
    assert post_response["success"] == True
    assert response["id"] == id
    assert "address" in response, "Address key should be present in response"

    name2 = 'bar'
    resource = {
      "name": name2
    }

    put_response = items.put(id, data={"resource": resource})
    assert put_response["success"] == True

    # Test update workflow
    response = items.get(id, params={"fields": ["name"]})
    assert response["name"] == name2

    # Test delete workflow
    delete_response = items.delete(id)
    assert delete_response["success"] == True




@my_vcr.use_cassette("categories.yml")
def test_categories():
  """Tests an API call to get a list of categories for each resource in a community."""
  response = instance.community(comm_id).businesses().categories().get()
  assert response == ["Foo"]
  response = instance.community(comm_id).events().categories().get()
  assert response == ["Foo"]
  response = instance.community(comm_id).listings().categories().get()
  assert response == []
  response = instance.community(comm_id).streetscape_assets().categories().get()
  assert response == ["Foo"]
  response = instance.community(comm_id).developments().categories().get()
  assert response == []

@my_vcr.use_cassette("subcategories.yml")
def test_subcategories():
  """Tests an API call to get a list of subcategories for each resource in a community."""
  response = instance.community(comm_id).businesses().subcategories().get()
  assert response == ["Bar1", "Bar2"]
  response = instance.community(comm_id).events().subcategories().get()
  assert response == ["Bar1", "Bar2"]
  response = instance.community(comm_id).listings().subcategories().get()
  assert response == []
  response = instance.community(comm_id).streetscape_assets().subcategories().get()
  assert response == []
  response = instance.community(comm_id).developments().subcategories().get()
  assert response == []

@my_vcr.use_cassette("tags.yml")
def test_tags():
  """Tests an API call to get a list of tags for each resource in a community."""
  response = instance.community(comm_id).businesses().tags().get()
  assert response == ["Tag1", "Tag2"]
  response = instance.community(comm_id).events().tags().get()
  assert response == ["Tag1", "Tag2"]
  response = instance.community(comm_id).listings().tags().get()
  assert response == []
  response = instance.community(comm_id).streetscape_assets().tags().get()
  assert response == []
  response = instance.community(comm_id).developments().tags().get()
  assert response == []


@my_vcr.use_cassette("listings.yml")
def test_listings():
    """Tests an API call to get a list of listings for a community."""
    response = instance.community(comm_id).listings().get(params={"fields": ["address"]})
    assert isinstance(response, list)
    for item in response:
        assert "id" in item, "Id key should be present in response"
        assert "lon" in item, "lon key should be present in response"
        assert "lat" in item, "lat key should be present in response"
        assert "address" in item, "Address key should be present in response"


@my_vcr.use_cassette("listing.yml")
def test_listing():
    """Tests an API call to get a list of listings for a community."""
    items = instance.community(comm_id).listings()
    id = items.get()[0]["id"]
    response = items.get(id, params={"fields": ["address"]})
    assert isinstance(response, dict)
    assert response["id"] == id
    assert "address" in response, "Address key should be present in response"


@my_vcr.use_cassette("streetscape_assets.yml")
def test_streetscape_assets():
    """Tests an API call to get a list of streetscape_assets for a community."""
    response = (
        instance.community(comm_id)
        .streetscape_assets()
        .get(params={"fields": ["address"]})
    )
    assert isinstance(response, list)
    for item in response:
        assert "id" in item, "Id key should be present in response"
        assert "lon" in item, "lon key should be present in response"
        assert "lat" in item, "lat key should be present in response"
        assert "address" in item, "Address key should be present in response"


@my_vcr.use_cassette("streetscape_asset.yml")
def test_streetscape_asset():
    """Tests an API call to get a list of streetscape_assets for a community."""
    items = instance.community(comm_id).streetscape_assets()
    id = items.get()[0]["id"]
    response = items.get(id, params={"fields": ["address"]})
    assert isinstance(response, dict)
    assert response["id"] == id
    assert "address" in response, "Address key should be present in response"


@my_vcr.use_cassette("developments.yml")
def test_developments():
    """Tests an API call to get a list of developments for a community."""
    response = (
        instance.community(comm_id).developments().get(params={"fields": ["address"]})
    )
    assert isinstance(response, list)
    for item in response:
        assert "id" in item, "Id key should be present in response"
        assert "lon" in item, "lon key should be present in response"
        assert "lat" in item, "lat key should be present in response"
        assert "address" in item, "Address key should be present in response"


@my_vcr.use_cassette("development.yml")
def test_development():
    """Tests an API call to get a list of developments for a community."""
    items = instance.community(comm_id).developments()
    id = items.get()[0]["id"]
    response = items.get(id, params={"fields": ["address"]})
    assert isinstance(response, dict)
    assert response["id"] == id
    assert "address" in response, "Address key should be present in response"
