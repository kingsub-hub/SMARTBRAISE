# 🌍 EcoMakala RDC

## Présentation
EcoMakala RDC est une application web de gestion de production, de stock, de commandes et de livraison de braises écologiques.  
L'application permet aux clients de commander des sacs de braise en ligne tandis que les gestionnaires suivent les ventes, les stocks, les paiements et les opérations de production à travers une interface centralisée.  
Le projet vise à moderniser la gestion des activités liées à la production et à la commercialisation de braises en République Démocratique du Congo.

---

## Problématique
Dans de nombreuses entreprises de production de braises, la gestion est encore réalisée manuellement :
- suivi du stock dans des cahiers ;
- enregistrement manuel des commandes ;
- difficulté à contrôler les livraisons ;
- risque de perte ou de vol de marchandises ;
- absence de statistiques fiables.

EcoMakala RDC propose une solution numérique permettant d'automatiser et de sécuriser ces opérations.

---

## Objectif général
Développer une plateforme de gestion intégrée permettant de contrôler les activités de production et de vente de braises.

---

## Objectifs spécifiques
- Authentifier les utilisateurs ;
- Gérer les clients ;
- Enregistrer les commandes ;
- Suivre les paiements ;
- Gérer les livraisons ;
- Contrôler les stocks ;
- Suivre la production ;
- Générer des statistiques ;
- Détecter les niveaux de stock faibles.

---

## Fonctionnalités
### Espace Client
- Création de compte
- Connexion
- Consultation des produits
- Passation de commande
- Suivi des commandes
- Choix de livraison ou retrait

### Espace Administrateur
- Gestion des utilisateurs
- Gestion des produits
- Gestion du stock
- Gestion des commandes
- Gestion des paiements
- Gestion des livraisons
- Tableau de bord statistique

### Module Production
- Création de lots de production
- Suivi des matières premières
- Mise à jour automatique du stock

---

## Cas d’utilisation
### Client
- S’inscrire
- Se connecter
- Commander des braises
- Payer un acompte
- Suivre sa commande

### Administrateur
- Gérer les produits
- Gérer le stock
- Valider les commandes
- Organiser les livraisons
- Consulter les statistiques

---

## Valeur ajoutée du projet
EcoMakala RDC permet de réduire les erreurs de gestion, d’améliorer le suivi des commandes, de sécuriser le stock et de faciliter la relation entre les producteurs de braises et leurs clients grâce à une plateforme numérique moderne adaptée au contexte congolais.

---

## Architecture du projet

EcoMakala_RDC/
├── manage.py
├── smartmakala/
│   ├── settings.py
│   ├── urls.py
│   └── …
├── accounts/
├── clients/
├── commandes/
├── stock/
├── production/
├── templates/
├── static/
└── db.sqlite3

---

## Technologies utilisées
### Backend
- Python
- Django

### Base de données
- SQLite

### Frontend
- HTML5
- CSS3
- JavaScript

### Outils
- VS Code
- Git
- GitHub

---

## Installation
1. Cloner le projet  
   ```bash
   git clone <url_du_projet>
   cd EcoMakala_RDC