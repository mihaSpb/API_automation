import json
import requests


class TestCreateJoke():

    base_url = "https://api.chucknorris.io/jokes/random"

    def test_create_random_joke(self):

        category = 'movie'
        params = {'category': category}

        response = requests.get(self.base_url, params=params)
        print(f"Status code: {response.status_code}")
        assert response.status_code == 200
        print("Status code is expected")

        data = response.json()
        print(json.dumps(data,  ensure_ascii=False, indent=2))

        categories = data.get('categories', [])
        print(f"Categories in response: {categories}")
        assert isinstance(categories, list), f"'categories' should be a list {type(categories)}"
        assert category in categories, f"Expected category '{category}' to be in '{categories}'"
        print("Category is expected")

        joke_text = data.get('value', "")
        assert 'Chuck' in joke_text, f"'Chuck' not found in joke: '{joke_text}'"
        print("Next check passed: contains 'Chuck'")

        print(f"Joke text: {joke_text}")
        assert joke_text

        print("All tests passed")

start = TestCreateJoke()
start.test_create_random_joke()

