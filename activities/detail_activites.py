import requests

token = "daae64c6c141fe14900ef7f923b3458525999ae0"
def get_air_quality(city):
    url = f"https://api.waqi.info/feed/{city}/?token={token}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

