import requests
import uuid
import json
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_GIGA')

def find_context_by_topic(topic: str):
    file_content = "Нет данных. Воспользуйтесь официальным сайтом https://nnov.hse.ru/"
    file_path = ""

    if topic == 'общежития общая информация':
        file_path = "data/general_dormitory.txt"
    elif topic == 'общежитие львовская':
        file_path = "data/dormitory_leo.txt"
    elif topic == 'общежитие кузнечиха' or topic == 'общежитие аксальта':
        file_path = "data/dormitory_axalta.txt"
    elif topic == 'военно учебный центр':
        file_path = "data/milit.txt"
    elif topic == 'стипендия':
        file_path = "data/scholarship.txt"

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
    except Exception as e:
        print(f"Ошибка чтения файла: {str(e)}")
        return None

    return file_content


def get_token(auth_token, scope='GIGACHAT_API_PERS'):

  rq_uid = str(uuid.uuid4())

  url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

  payload={
    'scope': scope
  }

  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': rq_uid,
    'Authorization': f'Basic {auth_token}'
  }

  try:
    response = requests.post(url, headers=headers, data=payload, verify=False)
    return response
  except requests.RequestException as e:
    print(f"Ошибка: {str(e)}")
    return -1

def get_topic(auth_token, user_message):
  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  prompt = f"Твоя задача отнести вопрос пользователя к одной из категорий. Категории: общежития общая информация, общежитие львовская, общежитие кузнечиха, общежитие аксальта, военно учебный центр, стипендия. Вопрос: {user_message}. ВЕРНИ ТОЛЬКО КАТЕГОРИЮ ИЗ СПИСКА."

  payload = json.dumps({
      "model": "GigaChat",
      "messages": [
          {
              "role": "user",
              "content": prompt
          }
      ],
      "temperature": 0.3,
      "top_p": 0.1,
      "n": 1,
      "stream": False,
      "max_tokens": 2000,
      "repetition_penalty": 1,
      "update_interval": 0
  })

  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {auth_token}'
  }

  try:
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    return response
  except requests.RequestException as e:
    print(f"Ошибка: {str(e)}")
    return -1

def get_answer(user_message):
  auth_token = get_token(API_KEY).json()["access_token"]

  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  topic = get_topic(auth_token, user_message).json()['choices'][0]['message']['content']

  context = find_context_by_topic(topic)

  prompt = f"Ты - помощник для абитуриентов НИУ ВШЭ Нижний Новгород. Ответь на вопрос пользователя в 3-5 предложений используя контекст. Обязательно дай в конце ссылку на источник. Вопрос пользователя: {user_message}. Контекст для ответа: {context}."

  payload = json.dumps({
      "model": "GigaChat",
      "messages": [
          {
              "role": "user",
              "content": prompt
          }
      ],
      "temperature": 0.7,
      "top_p": 0.1,
      "n": 1,
      "stream": False,
      "max_tokens": 2000,
      "repetition_penalty": 1,
      "update_interval": 0
  })

  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {auth_token}'
  }

  try:
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    print(f"[LOG] {response.json()['choices'][0]['message']['content']}")
    return response
  except requests.RequestException as e:
    print(f"Ошибка: {str(e)}")
    return -1

answer = get_answer("Куда я могу написать по поводу общежития?")
print(answer.json()['choices'][0]['message']['content'])