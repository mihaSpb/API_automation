import json
import requests
from typing import List


class TestCreateJokeCategory():


    base_url = "https://api.chucknorris.io/"

    def get_all_categories(self) -> List[str]:
        url = self.base_url + "jokes/categories"
        response = requests.get(url)
        assert response.status_code == 200, f"Expected status code 200. Got {response.status_code}"

        categories = response.json()
        assert isinstance(categories, list), f"Expected list of categories. Got {type(categories)}"
        print(f"List of categories: {categories}")

        return categories

    def test_random_joke_for_each_category(self):
        categories = self.get_all_categories()

        for category in categories:
            url = self.base_url + "jokes/random/"
            params = {"category": category}
            print(f"\nRequesting random joke in category {category} ")

            response = requests.get(url, params=params)
            assert response.status_code == 200, f"Expected status code 200. Got {response.status_code}"

            joke = response.json()
            print(json.dumps(joke, ensure_ascii = False, indent=2))


start = TestCreateJokeCategory()
start.test_random_joke_for_each_category()