from playwright.sync_api import Playwright, APIRequestContext
import pytest
import random

petId = random.randrange(100000, 200000)


@pytest.fixture(scope='session')
def api_request_context(playwright: Playwright):
    request_context = playwright.request.new_context(
        base_url='https://petstore.swagger.io/v2/'
        )
    yield request_context
    request_context.dispose()


def test_get_pet(api_request_context: APIRequestContext) -> None:
    petId = 5
    response = api_request_context.get(
        f'pet/{petId}', headers={"Accept": "application/json"},
        )
    assert response.status == 200
    print('\n\nPets were found by id. RESPONSE:')
    print(response.json())
