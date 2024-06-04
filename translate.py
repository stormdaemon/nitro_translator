import json
import time
import re
import multiprocessing as mp
from functools import partial
from googletrans import Translator
from tqdm import tqdm
import requests

def clean_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Supprimer les commentaires JSON
    content = re.sub(r'//.*\n', '\n', content)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # Supprimer les virgules en trop
    content = re.sub(r',(\s*[}\]])', r'\1', content)

    # Remplacer les valeurs manquantes par des chaînes vides
    content = re.sub(r':\s*,', ': "",', content)
    content = re.sub(r':\s*}', ': ""}', content)

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Erreur JSON dans {file_path}: {e}")
        with open(file_path.replace('.json', '_cleaned.json'), 'w', encoding='utf-8') as f:
            f.write(content)
        return None

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return data

def translate_with_deepl(text, target_lang):
    api_key = "YOUR_API_KEY"  # Remplacez par votre clé API DeepL
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": api_key,
        "text": text,
        "target_lang": "FR" if target_lang == 'fr' else target_lang.upper()
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        return response.json()['translations'][0]['text']
    return None

