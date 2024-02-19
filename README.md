# Mise en place d'une pipeline de test pour comparer les résultats

## Introduction

Dans ce répo je vais mettre en place une pipeline de test pour comparer les résultats de assistant api et du finetuning d'un modèle d'openai.

Pour que cette pipline de test sois efficace elle devra possèder plusieurs pool de questions. Chaque pool de questions aura un différent nombre de variables. Voici les pools de questions :

- Pool 1 : 1 faculté, 1 année
- Pool 2 : 2 faculté, 1 année
- Pool 3 : 2 faculté, n années

## Préréquis

- Python 3.8
- environnement virtuel python
- pip
- git
- un compte openai
- un fichier .env avec
  - OPENAI_API_KEY
  - SYSTEM_MESSAGE

## Installation

1. Cloner le répo
2. Créer un environnement virtuel python
   1. faire `python3 -m venv venv` pour créer l'environnement virtuel
   2. activer l'environnement virtuel avec `source venv/bin/activate`
3. Installer les dépendances avec `pip install -r requirements.txt`

## Utilisation

1. Activer l'environnement virtuel avec `source venv/bin/activate`

## Pool de questions

### Pool 1

Pour le pool 1 voici un exemple de questions :

```json
{
    "name":"pool1",
    "description":"pool de questions contenant les des questons portant sur une seule faculté et une seule année",
    "questions": [
        "Combien d'étudiants {sexe} étaient inscrits à la faculté de {faculté} en {année} ?",
        "Combien d'étudiant suisse il y avait à la faculté de {faculté} en {année} ?",
        "Combien d'étudiants internationaux il y avait à la faculté de {faculté} en {année} ?",
        "Combien d'étudiants étaient inscrits à la faculté de {faculté} en {année} ?",
        "Quelle était la proportion d'étudiants internationaux à la faculté de {faculté} en {année} ?",
        "Quelle était la proportion d'étudiants suisses à la faculté de {faculté} en {année} ?"
    ]
}
```

### Pool 2

Pour le pool 2 voici un exemple de questions :

```json
{
    "name" :"pool2",
    "description": "pool de questions contenant les des questons portant sur plusieurs facultés et une seule année",
    "questions": [
        "Comparez le nombre total d'étudiants inscrits dans les facultés de {faculté 1} et {faculté 2} en {année}.",
        "Quel pourcentage du total des étudiants inscrits en {année} était représenté par les étudiants de {faculté 1} et {faculté 2} respectivement ?", 
        "En {année}, quelle faculté entre {faculté 1} et {faculté 2} avait la plus grande proportion d'étudiants internationaux ?",
        "Quelle était la différence dans la répartition des étudiants par sexe entre les facultés de {faculté 1} et {faculté 2} en {année} ?",
        "En {année}, quelle faculté entre {faculté 1} et {faculté 2} avait une plus grande diversité de nationalités parmi les étudiants inscrits ?"
    ]
}
```

### Pool 3

Pour le pool 3 voici un exemple de questions :

```json
{
    "name" :"pool3",
    "description": "pool de questions contenant les des questons portant sur plusieurs facultés et plusieurs années",
    "questions": [
        "Comment a évolué le nombre total d'étudiants inscrits à la faculté de {faculté} de {année de début} à {année de fin} ?",
        "Quelle a été la tendance de la proportion d'étudiants internationaux à la faculté de {faculté} entre {année de début} et {année de fin} ?",
        "Entre {année de début} et {année de fin}, quelle a été l'évolution de la répartition des étudiants par sexe à la faculté de {faculté} ?",
        "Quelle faculté de {faculté} a connu la plus grande croissance en termes de nombre d'étudiants de {année de début} à {année de fin} ?"
    ]
}
```

## Création de la pipeline de test

Maintenant que j'ai les pools de questions je vais pouvoir créer la pipeline de test. La première étape sera de pouvoir crée un dataset de questions réponse pour chaque pool de questions en se basant sur les données contenue dans les fchiers json. Pour cela je me suis aidé de assistant api. Chaque paire question réponse sera sous la forme suivante :

```json
[
    {
        "question": "question",
        "answer": {
            "value": ["value1", ...]
        }
    }
]
```

Ensuite pour chaque pool il faudra crée des fichiers `jsonl` pour le finetuning (un de train et un de test). Pour cela je vais utiliser le script `create_json_finetuning.py`. Ce script va prendre en entrée un dossier contenant les fichiers json des pools de questions et va créer 2 fichier par pool de questions. Un fichier de train et un fichier de validation qui sont les 2 requis par openai pour le finetuning. Les fichiers sont sous la forme suivante :

```json
{"messages": [{"role": "system", "content": "Tu es un data scientist. On te pose des questions concernant les étudiants inscrits au semestre d’automne, par faculté selon le sexe. Les réponses doivent être sous forme de JSON. {'value': valeur_statistique}"}, {"role": "user", "content": "Quelle était la proportion d'étudiants internationaux à la faculté de HEC en 2016 ?"}, {"role": "assistant", "content": "{'value': 0.4126}"}]}
```

A noté que les données de finetuning représente 80% des données et les données de validation 20% des données. Et que toutes les paires questions réponses requièrent un message système qui est le même pour toutes les paires questions réponses.

`"Tu es un data scientist. On te pose des questions concernant les étudiants inscrits au semestre d’automne, par faculté selon le sexe. Les réponses doivent être sous forme de JSON. {'value': valeur_statistique}"`

Pour lancer le script il faut faire `python3 create_json_finetuning.py --path_to_pool_data <path_to_pool_data>`

## Finetuning

Pour le finetuning j'ai utilisé le script `finetune.py` qui est exactement le même que j'ai utiliser pour mes test de finetuning. Pour lancer le finetuning il faut faire `python3 finetune.py --td <path_to_train_data> --vd <path_to_validation_data> --epochs <number_of_epochs>`

## Test finetuning

Pour tester le finetuning j'ai utilisé le script `test_finetuning.py`. Il prend en entrée un répertoire contenant les pool ou il peut aussi prendre en entrée un seul fichier de pool de questions. Il va ensuite prendre un nombre de questions passé en paramètre pour les tester dans le modèle finetuner et ensuite comparer les résultats optenu avec les vrai résultats et ensuite crée un fichier de log en json qui contient les résultats de chaque question et un pourcentage de réussite. Pour lancer le script il faut faire `python3 test_finetuning.py --data <path_to_data> --nb_questions <number_of_questions>`

## Test assistant api

## Assistant API

Petit problème avec in id not found erreur 400 pour gérer ça je vais essayer de faire une base de données pour tester si l'id existe ou pas dans les données. Pour cela je vais utiliser une base de données sqlite3.

J'ai pu crée une fonction qui test si un id est dans les fichier courant mais j'ai pas encore tester a faire.

Tout ne marche pas bien j'ai pu noté une erreur lors ce que une question n'est pas possible il répond bien un tableau vide mais il n'arrive plus a répondres a toutes les questions suivantes. Il faut que je trouve un moyen de gérer ça.

problème de l'erreur 400 peut aussi étre du au multi-function-calling, que je ne gère pas pour le moment.

j'ai noté que avec `gpt-4-turbo-preview` il marche bien cepandant il ne load que 5 fichiers et après ne charge plus rien. Il faut que je trouve un moyen de gérer ça.

### SQLite
