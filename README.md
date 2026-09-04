# OPCVM Analytics

Application Streamlit dédiée au suivi et à l'analyse des OPCVM Actions.

## Fonctionnalités

### Performance

- Performance YTD
- Performance annualisée
- Classement des OPCVM
- Comparaison avec le MASI RB

### Risque

- Volatilité annualisée
- Tracking Error
- Bêta
- VaR 95%
- Maximum Drawdown

### Performance ajustée du risque

- Ratio de Sharpe
- Ratio de Treynor
- Ratio d'Information

### Reporting

- Import Excel
- Export Excel
- Export PDF (version future)
- Dashboard interactif

---

# Hypothèses

Taux sans risque utilisé :

```text
RF = 2,25 %
```

Annualisation :

```text
52 semaines
```

---

# Structure du projet

```text
opcvm-analytics/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── pages/
│
├── utils/
│
├── data/
│
└── .streamlit/
```

---

# Installation locale

Créer un environnement virtuel :

```bash
python -m venv venv
```

Activer :

Windows :

```bash
venv\\Scripts\\activate
```

Linux/Mac :

```bash
source venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Lancer l'application :

```bash
streamlit run app.py
```

---

# Déploiement GitHub

```bash
git init

git add .

git commit -m "Initial commit"

git branch -M main

git remote add origin https://github.com/<user>/opcvm-analytics.git

git push -u origin main
```

---

# Déploiement Streamlit Cloud

1. Créer un dépôt GitHub.
2. Publier le code.
3. Ouvrir :

https://share.streamlit.io

4. Sélectionner :

```text
Repository : opcvm-analytics
Branch     : main
File       : app.py
```

5. Deploy.

---

# Roadmap

## V1

- Import automatique des VL
- Calcul des métriques
- Dashboard

## V2

- Export PDF
- Benchmarks multiples
- Analyse Attribution de Performance

## V3

- Connexion API BMCE Capital / CDG Capital
- Historisation des données
- Base de données PostgreSQL
- Authentification utilisateurs
