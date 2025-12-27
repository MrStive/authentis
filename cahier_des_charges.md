# CAHIER DES CHARGES TECHNIQUE ET FONCTIONNEL

## PROJET : Authentis - Marketing Analytics Engine

**Version :** 1.0  
**Date :** 27 Décembre 2025  
**Auteur :** Équipe Technique Authentis

---

## 1. PRÉSENTATION DU PROJET

### 1.1 Contexte

Dans un environnement marketing de plus en plus axé sur la donnée ("Data-Driven"), les entreprises ont besoin d'outils capables de centraliser, analyser et activer leurs données clients. Le projet **Authentis - Marketing Analytics Engine** vise à fournir une plateforme unifiée pour l'analyse prédictive, la segmentation client avancée et le reporting automatisé.

### 1.2 Objectifs

L'objectif principal est de fournir une application web performante et intuitive permettant aux décideurs marketing de :

- Monitorer les indicateurs clés de performance (KPI) en temps réel.
- Segmenter la base client via des algorithmes de clustering (RFM).
- Prédire le comportement futur des clients (valeur à vie, risque de churn).
- Simuler le retour sur investissement (ROI) des campagnes marketing.

---

## 2. SPÉCIFICATIONS FONCTIONNELLES

### 2.1 Module Dashboard (Tableau de Bord Exécutif)

- **Visualisation des KPI** : Affichage en temps réel du Chiffre d'Affaires total, Nombre de clients actifs, Panier moyen, LTV (Lifetime Value) moyenne.
- **Analyse Temporelle** : Graphiques interactifs de l'évolution des revenus sur 12 mois.
- **Géographie** : Répartition des utilisateurs par zone géographique.
- **Alerting** : Système de notifications automatiques pour les anomalies (ex: augmentation soudaine du taux de churn).

### 2.2 Module Segmentation & Clustering

- **Analyse RFM** : Segmentation automatique basée sur la Récence, Fréquence et Montant des achats.
- **Clustering 3D** : Visualisation interactive en 3 dimensions des clusters clients.
- **Profilage** : Fiches détaillées par segment (Champions, À risque, Dormants, etc.).
- **Export** : Capacité d'exporter les listes de clients filtrées pour injection dans des outils d'emailing (CSV).

### 2.3 Module Prédictions (IA)

- **Calculateur LTV** : Estimation de la valeur future d'un prospect basée sur ses premiers signaux (canal d'acquisition, premier panier).
- **Détection de Churn** : Identification probabiliste des clients risquant de quitter le service.
- **Simulateur de ROI** : Outil permettant de simuler l'impact financier d'une campagne de rétention sur un segment donné.

### 2.4 Module Data Connectivity

- **Connecteurs Multi-Sources** :
  - **Fichiers Plats** : Import CSV, Excel, Parquet.
  - **Base de Données** : Connexion native PostgreSQL.
  - **API** : Intégration Google Analytics 4 (GA4).
- **Gestion des Données Manuelle** : Interface d'édition type "tableur" pour corriger ou ajouter des données à la volée.

---

## 3. ARCHITECTURE TECHNIQUE

### 3.1 Stack Technologique

L'application repose sur une architecture moderne, conteneurisée et micro-services :

- **Frontend / Interface Utilisateur** :
  - **Framework** : Streamlit (Python) pour une itération rapide et des capacités Data Science natives.
  - **Design System** : Custom CSS (Glassmorphism, Dark UI) avec typographie "Outfit".
- **Backend / Traitement** :
  - **Langage** : Python 3.12.
  - **Bibliothèques** : Pandas (manipulation), Scikit-Learn (ML/Clustering), Plotly (Visualisation), SQLAlchemy (ORM).
- **Base de Données** :
  - **Principale** : PostgreSQL 15 (Persistance des données clients et transactions).
  - **Cache** : Redis 7 (Mise en cache des sessions et résultats d'analyse lourds).
- **Infrastructure** :
  - **Conteneurisation** : Docker & Docker Compose.
  - **Proxy Inverse** : Nginx (Gestion des flux HTTP, Sécurité).

### 3.2 Diagramme d'Architecture (Logique)

```mermaid
graph TD
    Client[Client Navigateur] --> Nginx[Nginx Proxy :80]
    Nginx --> App[Streamlit App :8501]

    subgraph "Docker Network: marketing_net"
        App --> Postgres[(PostgreSQL DB :5432)]
        App --> Redis[(Redis Cache :6379)]
        App --> ExtAPI[Connecteurs API (GA4)]
    end
```

---

## 4. EXIGENCES NON-FONCTIONNELLES (QdS)

### 4.1 Performance

- **Temps de chargement** : L'interface doit charger en < 2 secondes.
- **Traitement de données** : Capacité à traiter des jeux de données jusqu'à 1 million de lignes en moins de 10 secondes grâce à l'optimisation Pandas/Redis.

### 4.2 Sécurité

- **Isolation** : Tous les services tournent dans des conteneurs isolés sur un réseau privé virtuel (Docker Bridge).
- **Gestion des Secrets** : Les identifiants (BDD, Clés API) doivent être injectés via des variables d'environnement, jamais codés en dur.

### 4.3 Maintenabilité

- **Code Modulaire** : Architecture claire séparant la logique métier (`src/`), l'interface (`app/pages/`) et les connecteurs.
- **Environment Reproducible** : Utilisation stricte de `requirements.txt` et `Dockerfile` multi-stage pour garantir des déploiements identiques en dev et prod.

---

## 5. LIVRABLES ATTENDUS

1.  **Code Source** : Dépôt Git complet avec historique.
2.  **Environnement Dockerisé** : Fichiers `Dockerfile` et `docker-compose.yml` fonctionnels.
3.  **Documentation** : README d'installation et Guide Utilisateur.
4.  **Rapport de Tests** : Validation des connecteurs et des algorithmes de clustering.

---

**Approbation :**
_Ce document sert de référence contractuelle pour le développement et la recette de l'application._
