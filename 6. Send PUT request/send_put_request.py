import json
import requests
from typing import List


class TestCreatePlaceID():


    base_url = 'https://rahulshettyacademy.com'
    post_resource = '/maps/api/place/add/json'
    get_resource = '/maps/api/place/get/json'
    put_resourse = '/maps/api/place/update/json'
    key_id = "?key=qaclick123"
    new_address = '24 Tamar Mepe str, RU'

    def _put_new_address(self, place_id: str, new_address: str):
        put_url = self.base_url + self.put_resourse + self.key_id
        print(put_url)

        json_put_location = {
            "place_id": place_id,
            "address": new_address,
            "key": "qaclick123"
        }

        result_put = requests.put(put_url, json=json_put_location)
        print(f"Result PUT: {result_put}")
        assert result_put.status_code == 200, f"Status code is not correct: {result_put.status_code}"
        print(f"Status code: {result_put.status_code}")

        check_response_put = result_put.json()


    def _create_new_location(self) -> str:
        post_url = self.base_url + self.post_resource + self.key_id
        print(post_url)

        json_location = {
            "location": {
                "lat": -38.383494,
                "lng": 33.427362
            }, "accuracy": 50,
            "name": "Frontline house",
            "phone_number": "+90 555 777 77 66",
            "address": "29-st, side layout, cohen 09",
            "types": [
                "shoe park",
                "shop"
            ],
            "website": "https://google.com",
            "language": "en",
        }

        result_post = requests.post(post_url, json=json_location)
        print(f"Result POST: {result_post.json()}")
        assert result_post.status_code == 200, f"Status code not correct: {result_post.status_code}"
        print(f"Status code = {result_post.status_code} it`s correct")

        place_id = result_post.json().get('place_id')
        assert place_id is not None, f"No place id found"
        print(f"Place id = {place_id}")
        return place_id

    def _get_location(self, place_id: str) -> dict:
        get_url = self.base_url + self.get_resource + self.key_id + '&place_id=' + place_id
        print(get_url)

        result_get = requests.get(get_url)
        assert result_get.status_code == 200, f"Status code not correct: {result_get.status_code}"
        print(f"Status code = {result_get.status_code} it`s correct")

        data = result_get.json()
        assert data is not None, f"No data found"
        print(f"Added place {place_id}: {json.dumps(data, indent = 2)}")
        return data

    def test_create_and_verify_place(self, count: int = 5, filename: str = "place_id.txt"):
        places_id: List[str] = [self._create_new_location() for _ in range(count)]

        with open(filename, 'w') as f:
            for plid in places_id:
                f.write(plid + "\n")
        print(f"Saved {len(places_id)} places ID to {filename}")

        with open(filename, 'r') as f:
            for line in f:
                plid = line.strip()
                data = self._get_location(plid)
                assert data is not None, f"No data found"
                print(f"Added place {plid} is correct")


start = TestCreatePlaceID()
start.test_create_and_verify_place()