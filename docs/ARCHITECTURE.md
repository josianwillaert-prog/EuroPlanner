# EuroPlanner - Architecture

## Objectif

EuroPlanner est une application permettant de transformer les catalogues PDF Eurostar en objets métier, puis en planning et en calendrier ICS.

L'objectif principal est de disposer d'un moteur de lecture fiable, maintenable et extensible.

---

# Pipeline général

```text
PDF
    ↓
PdfLayoutReader
    ↓
DiagramLocator
    ↓
DiagramFactory
    ↓
Diagram
    ↓
JourneeService.from_diagram()
    ↓
Planning
    ↓
ICSGenerator
    ↓
Planning.ics
```

---

# Responsabilités

## PdfLayoutReader

Responsabilité unique :

* lire un PDF ;
* produire des PageWord et PageLine.

Il ne contient aucune logique métier.

---

## DiagramLocator

Responsabilité unique :

* localiser les diagrammes dans le PDF.

Il ne lit pas les horaires.

Il ne construit aucun objet métier.

---

## DiagramFactory

Responsabilité unique :

* transformer les PageWord en objets Diagram.

Il segmente le document.

Il ne connaît pas JourneeService.

---

## Diagram

Diagram représente un diagramme Eurostar complet.

Il contient :

* code
* page
* mots
* x_min
* x_max
* y_min
* y_max

Il expose des propriétés calculées :

* book_on
* book_off
* duration
* effective_working_time
* out_of_home
* out_of_home_code

Plus tard :

* trains
* observations

Diagram est le seul objet métier autorisé à manipuler directement les PageWord.

---

## GeometryReader

GeometryReader est une bibliothèque de fonctions géométriques.

Il ne possède aucun état métier.

Il est utilisé uniquement par Diagram.

---

## JourneeService

JourneeService représente la journée de service utilisée par le reste de l'application.

Il est créé avec :

* from_diagram(diagram)

JourneeService ne connaît pas le PDF.

---

## Catalogue

Catalogue ne réalise aucun parsing.

Il orchestre simplement :

* lecture ;
* création des Diagram ;
* conversion en JourneeService.

---

## ICSGenerator

ICSGenerator ne manipule jamais le PDF.

Il travaille uniquement avec des objets JourneeService.

---

# Règles d'architecture

## Règle 1

Aucune classe ne doit parcourir directement les PageWord sauf :

* PdfLayoutReader
* DiagramFactory
* Diagram

---

## Règle 2

Une classe = une responsabilité.

---

## Règle 3

Toute nouvelle fonctionnalité doit être ajoutée dans la couche métier appropriée.

---

## Règle 4

Le reste de l'application ignore totalement pdfplumber.

---

## Règle 5

Aucune modification ne doit dégrader cette architecture.

En cas de doute, privilégier l'ajout d'une nouvelle classe plutôt que de mélanger plusieurs responsabilités.

---

# Plan de migration

1. Introduire DiagramFactory.
2. Introduire Diagram.
3. Ajouter JourneeService.from_diagram().
4. Migrer progressivement Catalogue.
5. Comparer les résultats entre ancien et nouveau moteur.
6. Supprimer DiagramParser.
7. Supprimer DiagramBlockExtractor.
8. Ajouter les trains.
9. Ajouter les observations.
10. Ajouter les statistiques.

---

Ce document est la référence architecturale du projet.

Toute modification du code doit être compatible avec cette architecture.
