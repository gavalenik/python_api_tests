# python3 -m venv .venv
# pip3 freeze > requirements.txt
import requests
import pytest
import random
import re

baseUrl = "https://petstore.swagger.io/v2/"
petId = random.randrange(100000, 200000)
catTagId = random.randrange(1, 100)
petStatus = "availableToBuy"
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
    "status": petStatus
}


def assertEncoding(body):
    symbolCounter = 0
    for element in body:
        notAlphaNumeric = re.match(r'[a-zA-Z0-9_]', element) is None
        notAllowedSymbols = re.match(r'[/[{}\":;,.\]\s]', element) is None
        if notAlphaNumeric and notAllowedSymbols:
            raise ValueError("Some weird symbols in response body!")
        symbolCounter += 1
        if symbolCounter > 1000:
            break  # If first 1000 symbols is correct, whole body is correct


def test_petstore_api():
    try:
        # Check that our petId is not exist
        url = baseUrl + f'pet/{petId}'
        response = requests.get(url, headers=defaultHeaders)
        assert response.status_code == 404
        assert ("Pet not found" in response.text) == 1, 'Response is wrong'
        assertEncoding(response.text)
        print('\nPet is not exist. RESPONSE:\n' + response.text)

        # Create pet with our petId
        url = baseUrl + 'pet'
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers.update(defaultHeaders),
                                 json=defaultBody)
        assert response.status_code == 200
        assert (str(petId) in response.text) == 1, 'Response is wrong'
        assertEncoding(response.text)
        print('\nPet has been created. RESPONSE:\n' + response.text)

        # Find account by status
        url = baseUrl + f'pet/findByStatus?status={petStatus}'
        response = requests.get(url, headers=defaultHeaders)
        assert response.status_code == 200
        assert (str(petId) in response.text) == 1, 'Response is wrong'
        assertEncoding(response.text)
        print('\nPets were found by status. RESPONSE:\n' + response.text)

        # Update our pet's name
        url = baseUrl + 'pet'
        headers = {"Content-Type": "application/json"}
        updatedName = "BuddyUpdated"
        defaultBody['name'] = updatedName
        response = requests.put(url, headers=headers.update(defaultHeaders),
                                json=defaultBody)
        assert response.status_code == 200
        assert (str(petId) in response.text) == 1, 'Response is wrong'
        assert (updatedName in response.text) == 1, 'Response is wrong'
        assertEncoding(response.text)
        print('\nPet has been updated. RESPONSE:\n' + response.text)

    finally:
        # Delete our pet
        url = baseUrl + f'pet/{petId}'
        response = requests.delete(url, headers=defaultHeaders)
        assert response.status_code == 200
        assert (str(petId) in response.text) == 1, 'Response is wrong'
        assertEncoding(response.text)
        print('\nPet has been deleted. RESPONSE:\n' + response.text)


if __name__ == '__main__':
    pytest.main()
