# Pandas Sales Data Project

Projet réalisé pour **pratiquer Pandas et les bonnes pratiques de traitement de données** à partir d'un dataset de ventes.

Le pipeline nettoie les données, applique des contrôles de qualité, calcule des agrégations, puis stocke les résultats dans **PostgreSQL**. Tout tourne dans **Docker** via **Docker Compose**.

## Architecture

```text
sales.csv  →  Python + Pandas (conteneur)  →  PostgreSQL 16 (conteneur)
```

## Structure du projet

```text
pandas_project/
├── app/
│   ├── main.py               # point d'entrée du pipeline
│   ├── clean.py              # nettoyage + data quality
│   ├── database.py           # connexion et écriture PostgreSQL
│   ├── aggregate_product.py  # agrégation par produit
│   ├── aggregate_city.py     # agrégation par ville
│   └── aggregate_date.py     # agrégation par mois
├── data/
│   └── sales.csv
├── output/
├── Dockerfile
├── compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## Dataset

`data/sales.csv` contient :

| Colonne | Description |
|---|---|
| `order_id` | Identifiant de la commande |
| `customer_id` | Identifiant du client |
| `product` | Produit acheté |
| `quantity` | Quantité |
| `unit_price` | Prix unitaire |
| `order_date` | Date de commande |
| `city` | Ville |
| `country` | Pays |
| `email` | Email du client |

## Ce que j'ai pratiqué

- Lecture et manipulation de données avec **Pandas**
- Gestion des valeurs manquantes et des doublons
- Contrôles de qualité des données
- Nettoyage et transformation
- Agrégations par produit, ville et date (`groupby`)
- Calcul de métriques de vente
- Écriture des résultats dans **PostgreSQL** (SQLAlchemy)
- Conteneurisation avec **Docker** et **Docker Compose**

## Tables créées dans PostgreSQL

Base : `sales`

| Table | Contenu |
|---|---|
| `orders_cleaned` | Commandes nettoyées (données de base après cleaning) |
| `sales_by_product` | Quantité totale et chiffre d'affaires par produit |
| `sales_by_city` | Ventes agrégées par ville |
| `sales_by_month` | Ventes agrégées par mois |

Exemple : `SELECT * FROM sales_by_product;`

| product | total_quantity | total_revenue |
|---|---|---|
| keyboard | 21 | 945 |
| laptop | 20 | 16607.69 |
| monitor | 14 | 3500 |
| mouse | 35 | 892.5 |

## Lancer le projet

Depuis la racine du projet :

```bash
docker compose up --build
```

Arrêter :

```bash
docker compose down
```

Arrêter et supprimer aussi les données PostgreSQL (volume) :

```bash
docker compose down -v
```

## Vérifier les résultats

```bash
docker exec -it postgres-db psql -U postgres -d sales
```

Dans `psql` :

```sql
\dt
SELECT * FROM orders_cleaned LIMIT 10;
SELECT * FROM sales_by_product;
```

> Ne pas oublier le `;` à la fin de chaque requête SQL. Sans lui, `psql` attend la suite de la commande.

## Problèmes rencontrés et solutions

**1. Emplacement du dossier `data`**
Le CSV est dans `data/`, mais le script lit `sales.csv`. Dans le `Dockerfile`, `COPY data/ .` copie le contenu de `data/` dans `/app`, à côté de `main.py`, donc `pd.read_csv("sales.csv")` fonctionne.

**2. `syntax error at or near "SELECT"` dans psql**
Une requête sans `;` n'est pas exécutée, et la suivante est concaténée avec elle. Toujours terminer par `;`.

**3. `docker ps` n'affiche pas le conteneur Python**
Le conteneur du pipeline s'arrête après son exécution. Utiliser `docker ps -a` (sans espace entre `-` et `a`) pour voir les conteneurs terminés, et `docker logs pandas-python` pour voir les erreurs.

**4. Conteneur qui sort avec `Exited (1)`**
Signifie une erreur Python. Causes classiques :
- PostgreSQL pas encore prêt quand le script démarre (`depends_on` n'attend pas la disponibilité de la base)
- host de connexion incorrect : dans Docker il faut utiliser le nom du service (`postgres-db`), pas `localhost`
- nom de module incorrect (`main.py` importe `clean`, le fichier doit s'appeler `clean.py`)

**5. Ordre des services**
`depends_on` garantit seulement l'ordre de démarrage. Amélioration possible : ajouter un `healthcheck` à PostgreSQL et `condition: service_healthy`.

## Améliorations possibles

- Healthcheck PostgreSQL dans `compose.yml`
- Variables d'environnement dans un fichier `.env` (identifiants DB)
- Tests unitaires sur les fonctions de nettoyage
- Logging à la place des `print`

## Technologies

**Python 3.12 · Pandas · SQLAlchemy · PostgreSQL 16 · Docker · Docker Compose**

## Auteur

**ABOUELOUAFA ZAKARIA**
GitHub : [abouelouafaZakaria](https://github.com/abouelouafaZakaria)
