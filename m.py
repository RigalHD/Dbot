import requests

# Токен вашего бота Discord
TOKEN = "TOKEN_HERE"

# ID пользователя, информацию о котором мы хотим получить
user_id = 'SPECIFIC_USER_ID_HERE'

# URL API Discord
api_url = f'https://discord.com/api/v9/users/{581348510830690344}'

# Заголовки запроса, включая токен авторизации
headers = {
    'Authorization': f'Bot {TOKEN}'
}

# Выполнение GET-запроса к API Discord
response = requests.get(api_url, headers=headers)

# Печать ответа
print(response.json())