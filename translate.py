import json
import time
import re
import multiprocessing as mp
from functools import partial
from googletrans import Translator, constants
from tqdm import tqdm
import requests

def clean_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Supprimer les commentaires JSON (non standard mais parfois utilisés)
    content = re.sub(r'//.*\n', '\n', content)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # Supprimer les virgules en trop
    content = re.sub(r',(\s*[}\]])', r'\1', content)

    # Remplacer les valeurs manquantes par des chaînes vides
    content = re.sub(r':\s*,', ': "",', content)
    content = re.sub(r':\s*}', ': ""}', content)

    try:
        # Essayer de charger le JSON
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Erreur JSON dans {file_path}: {e}")
        # En cas d'erreur, sauvegarder le contenu modifié pour inspection
        with open(file_path.replace('.json', '_cleaned.json'), 'w', encoding='utf-8') as f:
            f.write(content)
        return None

    # Sauvegarder le JSON nettoyé
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return data

def translate_with_retry(text, target_lang, max_retries=3):
    for _ in range(max_retries):
        try:
            translator = Translator()
            time.sleep(0.1)
            translated = translator.translate(text, dest=target_lang)
            if translated and translated.text:
                return translated.text
        except Exception:
            pass
    return None

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

def translate_item(item, target_lang):
    key, value = item
    if isinstance(value, str):
        translated = translate_with_retry(value, target_lang)
        if not translated:
            translated = translate_with_deepl(value, target_lang)
        if translated:
            return key, translated
    return key, value

def translate_json(file_path, target_lang):
    # Nettoyer et charger le fichier JSON
    data = clean_json_file(file_path)
    if not data:
        print(f"Impossible de traduire {file_path} en raison d'erreurs JSON.")
        return
    
    # Préparer la fonction de traduction avec la langue cible
    translate_func = partial(translate_item, target_lang=target_lang)
    
    # Initialiser la barre de progression
    total_keys = len(data)
    pbar = tqdm(total=total_keys, desc=f"Traduction de {file_path}", unit="clé")
    
    # Traduire chaque valeur dans le JSON
    results = []
    for result in map(translate_func, data.items()):
        results.append(result)
        pbar.update(1)
    
    # Fermer la barre de progression
    pbar.close()
    
    # Reconstruire le dictionnaire à partir des résultats
    translated_data = dict(results)
    
    # Sauvegarder le JSON traduit
    output_path = file_path.replace('.json', f'_{target_lang}.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=4)
    
    print(f"Traduit et sauvegardé dans {output_path}")

# Point d'entrée principal
if __name__ == '__main__':
    print("Traduction des fichiers external_text et ui_text en cours...")

    # Traduire les fichiers en français
    try:
        translate_json('ExternalTexts.json', 'fr')
        translate_json('UItexts.json', 'fr')
    except Exception as e:
        print(f"\nUne erreur est survenue : {e}")

    # Message de fin
    print("Traduction terminée !")