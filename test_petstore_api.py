# python3 -m venv .venv
# pip3 freeze > requirements.txt
import requests
import pytest
import random

baseUrl = "https://petstore.swagger.io/v2/"
petId = random.randrange(100000, 200000)
catTagId = random.randrange(1, 100)
defaultHeaders = {"accept": "application/json"}
defaultBody = {
    "id": petId,
    "category": {
        "id": catTagId,
        "name": "testCategory"
    },
    "name": "Buddy",
    "photoUrls": [
        "https://testPhotoSite.com/test"
    ],
    "tags": [{
        "id": catTagId,
        "name": "testTag"
    }],
    "status": "availableToSell"
}


def test_petstore_api():
    # Check that our petId is not exist
    url = baseUrl + f'pet/{petId}'
    response = requests.get(url, headers=defaultHeaders)
    assert response.status_code == 404
    assert ("Pet not found" in response.text) == 1, 'Response is wrong'
    # TODO add assert for response.text for correct encoding as a function
    print('\nPet is not exist. RESPONSE:\n' + response.text)

    # Create pet with our petId
    url = baseUrl + 'pet'
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers.update(defaultHeaders),
                             json=defaultBody)
    assert response.status_code == 200
    assert (str(petId) in response.text) == 1, 'Response is wrong'
    print('\nPet has been created. RESPONSE:\n' + response.text)

    # Delete our pet
    url = baseUrl + f'pet/{petId}'
    response = requests.delete(url, headers=defaultHeaders)
    assert response.status_code == 200
    assert (str(petId) in response.text) == 1, 'Response is wrong'
    print('\nPet has been deleted. RESPONSE:\n' + response.text)


if __name__ == '__main__':
    pytest.main()
