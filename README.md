![Nitro Translator v1](https://habbofont.net/font/habbo_new_big/nitro+translator+v1.gif)

# Nitro Translator v1 🌐

Traduisez facilement vos fichiers JSON de langues avec ce script Python polyvalent. Idéal pour les projets multilingues, il utilise Google Translate et DeepL pour une traduction précise.

## Prérequis 🛠️

![Python Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Python_logo_and_wordmark.svg/1200px-Python_logo_and_wordmark.svg.png)

Python 3 est requis. Assurez-vous de l'avoir installé avant de continuer.

## Configuration de l'API DeepL 🔑

Pour obtenir des traductions de haute qualité, nous utilisons l'API DeepL. Voici comment obtenir votre clé API gratuite :

1. Visitez [DeepL API](https://www.deepl.com/pro-api)
2. Cliquez sur "Créer un compte gratuit"
3. Remplissez le formulaire et validez votre email
4. Une fois connecté, allez dans "Compte" > "Plan et utilisation"
5. Faites défiler jusqu'à "Clé d'authentification" et copiez votre clé API

Maintenant, dans le fichier `translator.py`, remplacez `"YOUR_API_KEY"` par votre clé API DeepL :

api_key = "YOUR_API_KEY"  # Remplacez par votre clé API DeepL

## Installation 💽

1. Clonez ce dépôt :
   git clone https://github.com/votre-nom/nitro-translator.git
   
2. Double-cliquez sur `install.bat` pour installer les dépendances Python nécessaires.

## Utilisation 🚀

1. Placez vos fichiers JSON (`ExternalTexts.json` et `UItexts.json`) dans le même dossier que le script.

2. Double-cliquez sur `start.bat` pour lancer la traduction.

3. Le script nettoiera d'abord les fichiers JSON, puis traduira chaque clé en français (par défaut). Les fichiers traduits seront sauvegardés avec le suffixe `_fr.json`.

## Fonctionnalités ✨

- Nettoyage automatique des fichiers JSON
- Double moteur de traduction (Google Translate + DeepL)
- Barre de progression pour suivre l'avancement
- Gestion des erreurs et des tentatives multiples

## Personnalisation 🛠️

- Modifiez `target_lang` dans `translate_json` pour changer la langue cible (ex: 'es' pour l'espagnol).
- Ajustez `max_retries` dans `translate_with_retry` si vous rencontrez des problèmes de connexion.

## Contribuer 🤝

Les pull requests sont les bienvenues ! N'hésitez pas à signaler des bugs ou à suggérer des améliorations.

Transformez votre projet en une expérience multilingue fluide avec Nitro Translator v1. Traduisez, intégrez, et connectez-vous avec le monde entier ! 🌍✨
