# Mise en place d'une pipeline de test pour comparer les résultats

Pour que cette pipline de test sois efficace elle devra possèder plusieurs pool de questions. Chaque pool de questions aura un différent nombre de variables. Voici les pools de questions :

- Pool 1 : 1 faculté, 1 année
- Pool 2 : 2 faculté, 1 année
- Pool 3 : 2 faculté, n années.

## Pool 1

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

## Pool 2

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

## Pool 3

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
