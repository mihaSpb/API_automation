import json
import requests
from typing import List


class TestCreatePlaceID:
    base_url = 'https://rahulshettyacademy.com'
    post_resource = '/maps/api/place/add/json'
    get_resource = '/maps/api/place/get/json'
    put_resourse = '/maps/api/place/update/json'
    delete_resourse = '/maps/api/place/delete/json'
    key_id = "?key=qaclick123"
    new_address = '24 Tamar Mepe str, RU'

    def _delete_location(self, place_id: str) -> None:
        delete_url = self.base_url + self.delete_resourse + self.key_id
        print(delete_url)

        json_delete_location = {
            "place_id": place_id
        }
        result_delete = requests.delete(delete_url, json=json_delete_location)
        assert result_delete.status_code == 200, f"Status code is not correct: {result_delete.status_code}"
        print(f"Status code is {result_delete.status_code}")

        check_response_delete = result_delete.json()
        status = check_response_delete['status']
        print(status)
        assert status == 'OK', f"Status code is not correct {status}"
        print("Status code is OK")

        result_get = requests.get(self.base_url + self.get_resource + self.key_id + '&place_id=' + place_id)
        print(result_get.json())
        print(f'Status code is {result_get.status_code}')
        assert result_get.status_code == 404, f"Status code is not correct: {result_get.status_code}"
        print('Status code is correct')

        check_response_get = result_get.json()
        msg = check_response_get.get('msg')
        print(msg)
        assert msg == "Get operation failed, looks like place_id  doesn't exists", \
            f"MSG is not correct: {check_response_get.get('msg')}"
        print('Response MSG is correct')

    def _put_new_address(self, place_id: str, new_address: str) -> None:
        put_url = self.base_url + self.put_resourse + self.key_id
        print(put_url)

        json_put_location = {
            "place_id": place_id,
            "address": new_address,
            "key": "qaclick123"
        }

        result_put = requests.put(put_url, json=json_put_location)
        assert result_put.status_code == 200, f"Status code is not correct: {result_put.status_code}"
        print(f"Status code: {result_put.status_code}")

        check_response_put = result_put.json()
        msg = check_response_put['msg']
        print(msg)
        assert msg == 'Address successfully updated', f"Status code is not correct: {msg}"
        print("MSG is correct")

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

    def test_create_and_verify_place(self, count: int = 5, filename: str = "place_id.txt") -> None:
        places_id: List[str] = [self._create_new_location() for _ in range(count)]
        with open(filename, 'w') as f:
            for plid in places_id:
                f.write(plid + "\n")
        print(f"Saved {len(places_id)} places ID to {filename}")

        for pid in places_id:
            orig_address = self._get_location(pid)
            old_address = orig_address.get('address')
            print(f"Old address: {old_address}")

            # Обновление адреса
            self._put_new_address(pid, self.new_address)

            # Проверяем изменение адреса
            updated_address = self._get_location(pid)
            assert updated_address.get('address') == self.new_address, (f"Expected update address: '{self.new_address}',"
                                                                        f" got {updated_address.get('address')}")
            print(f"Updated address verified for {pid}\n")

        # Удаление 2 и 4 ID
        to_delete = [places_id[1], places_id[3]]
        for pid in to_delete:
            self._delete_location(pid)

        # Фильтрация оставшихся адресов
        existing_address: List[str] = []
        with open(filename, 'r') as f:
            for line in f:
                pid =line.strip()
                get_url = self.base_url + self.get_resource + self.key_id + '&place_id=' + pid
                resp = requests.get(get_url)

                if resp.status_code == 200:
                    existing_address.append(pid)
                else:
                    print(f"{pid} is not exist")

        # Запись в файл
        new_file = "existing_address.txt"
        with open(new_file, 'w') as f_new:
            for pid in existing_address:
                f_new.write(pid + "\n")
        print(f"Saved {len(existing_address)} addresses to {new_file}")

        print("All tests completed")


start = TestCreatePlaceID()
start.test_create_and_verify_place()