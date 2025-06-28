import json
import requests


url = "https://api.chucknorris.io/jokes/random"
print(f"Запрос будет отправлен на URL: {url}")

response = requests.get(url)

status_code = response.status_code
print("Статус код: ", status_code)

expected = 200
actual = status_code
if actual == expected:
    print(f"ОР == ФР: ожидаемый результат {expected} совпал с фактическим {actual}")
else:
    print(f"ОР != ФР: ожидаемый результат {expected}, фактический {actual}")

response.encoding = 'utf-8'
data = response.json()

print("Ответ JSON (не форматированные данные):")
print(data)

print("\nОтвет JSON (форматированный):")
print(json.dumps(data, ensure_ascii=False, indent=2))
