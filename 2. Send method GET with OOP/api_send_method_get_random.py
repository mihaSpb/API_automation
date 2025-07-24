import json
import requests


class TestCreateJoke:


    base_url = "https://api.chucknorris.io/jokes/random"

    def __init__(self, category: str):
        self.category = category

    def test_create_random_joke(self):

        params = {'category': self.category}
        print(f"Requesting joke in category {self.category}")

        response = requests.get(self.base_url, params=params)
        print(f"Status code: {response.status_code}")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        print("Status code is expected")

        data = response.json()
        print(json.dumps(data,  ensure_ascii=False, indent=2))

        categories = data.get('categories', [])
        print(f"Categories in response: {categories}")
        assert isinstance(categories, list), f"'categories' should be a list {type(categories)}"
        assert self.category in categories, f"Expected category '{self.category}' to be in '{categories}'"
        print("Category is expected")

        joke_text = data.get('value', "")
        assert 'Chuck' in joke_text, f"'Chuck' not found in joke: '{joke_text}'"
        print("Next check passed: contains 'Chuck'")
        print("All tests passed")

start = TestCreateJoke('dev')
start.test_create_random_joke()

