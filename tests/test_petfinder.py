# test_petfinder.py

from petfinder_api import get_token, get_dogs

def test_petfinder():
    token = get_token()
    dogs = get_dogs(token, params={"location": "10001", "limit": 5})

    for dog in dogs:
        print(f"{dog['name']} - {dog['breeds']['primary']} - {dog['age']}")

if __name__ == "__main__":
    test_petfinder()
