import json
import requests
from typing import List


class TestCreateJokeCategory():


    base_url = "https://api.chucknorris.io/"

    def test_random_joke(self, category: str):
        url = self.base_url + "jokes/random"
        params = {"category": category}
        print(f"Requesting joke in category {category}")

        response = requests.get(url , params = params)
        print(f"Status code: {response.status_code}")
        assert response.status_code == 200, (f"Expected status code 200, got {response.status_code}")
        print("Status code is expected")

        data = response.json()
        print(json.dumps(data, ensure_ascii = False, indent = 2))

        categories = data.get("categories", [])
        print(f"Categories in response: {categories}")
        assert isinstance(categories, list), (
            f"'categories' should be a list, got {type(categories)}"
        )
        assert category in categories, (
            f"Expected category '{category}' to be in {categories}"
        )
        print("Category is expected")

    def get_all_categories(self) -> List[str]:
        url = self.base_url + "jokes/categories"
        response = requests.get(url)
        assert response.status_code == 200, f"Expected status code 200. Got {response.status_code}"

        categories = response.json()
        assert isinstance(categories, list), f"Expected list of categories. Got {type(categories)}"
        print(f"List of categories: {categories}")

        return categories

    def test_all_category(self):
        for category in self.get_all_categories():
            self.test_random_joke(category)


start = TestCreateJokeCategory()
start.test_all_category()