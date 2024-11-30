from django.conf import settings
import requests
import time

headers = {"Authorization": "Bearer " + settings.EDENAI_BEARER_TOKEN}
url = "https://api.edenai.run/v2/workflow/c92c5ade-a4be-4ccf-b3c5-6b298c4e18c1/execution/"


def call_execution_service(ingredients: str) -> str | None:
    payload = {
        "text": ingredients,
    }
    response = requests.post(url, json=payload, headers=headers)
    if not response.ok:
        return

    result = response.json()
    return result['id']


def get_execution_result_service(id_: str) -> str | None:
    response = requests.post(url+id_, headers=headers)
    if not response.ok:
        return
    
    result = response.json()
    if result['content']['status'] == 'success':
        return result['content']['results']['text__chat']['results'][0]['generated_text']
    return


def finally_get_execution_result_service(ingredients: str) -> str:
    id_ = call_execution_service(ingredients)
    receipes = ""
    while True:
        time.sleep(1)
        receipes = get_execution_result_service(id_)
        if receipes:
            break
    
    return receipes


def parse_recipes(raw_response):
    recipes = []
    raw_parts = raw_response.split('\n')
    
    for part in raw_parts:
        if "**Название рецепта:**" in part:
            name = part.split("**Название рецепта:**")[1].split('-')[0].strip()
            ingredients = part.split("**Необходимые ингредиенты:**")[1].split('-')[0].strip()
            description = part.split("**Описание:**")[1].strip()
            
            recipes.append({
                'name': name,
                'ingredients': ingredients,
                'description': description,
            })
    return recipes
