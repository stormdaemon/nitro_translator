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

def translate_batch(texts, target_lang, max_retries=3):
    translator = Translator()
    with requests.Session() as session:
        for _ in range(max_retries):
            try:
                translations = translator.translate(texts, dest=target_lang)
                return [t.text for t in translations]
            except Exception:
                time.sleep(1)
    return [translate_with_deepl(text, target_lang) for text in texts]

def translate_json(file_path, target_lang, batch_size=10):
    data = clean_json_file(file_path)
    if not data:
        print(f"Impossible de traduire {file_path} en raison d'erreurs JSON.")
        return

    items = list(data.items())  # Conversion en liste pour l'indexation
    total_keys = len(items)

    with mp.Pool() as pool:
        batches = [items[i:i+batch_size] for i in range(0, total_keys, batch_size)]
        results = list(tqdm(pool.imap(partial(translate_batch, target_lang=target_lang), batches), 
                            total=len(batches), desc=f"Traduction de {file_path}", unit="batch"))

    translated_data = {}
    for batch_result in results:
        for key, value in batch_result:
            translated_data[key] = value

    output_path = file_path.replace('.json', f'_{target_lang}.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=4)
    print(f"Traduit et sauvegardé dans {output_path}")

if __name__ == '__main__':
    print("Traduction des fichiers external_text et ui_text en cours...")
    try:
        translate_json('ExternalTexts.json', 'fr', batch_size=20)
        translate_json('UItexts.json', 'fr', batch_size=20)
    except Exception as e:
        print(f"\nUne erreur est survenue : {e}")
    print("Traduction terminée !")
