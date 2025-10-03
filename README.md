# 📚 BookScrape - API Clean Architecture

> **Projet de scraping de livres avec API FastAPI refactorisée selon les principes Clean Architecture**

## 🎯 Vue d'ensemble

Ce projet combine :
- **Web Scraping** : Extraction de données de livres avec Scrapy
- **API REST** : FastAPI avec architecture propre et testable
- **Base de données** : SQLite avec 1000+ livres scrapés
- **Architecture Clean** : Séparation des responsabilités en 4 couches

---

## 📁 Structure du projet

```
bookscrape/
├── 🕷️ book_scrape/           # Module Scrapy pour scraper les livres
│   └── book_scrape/
│       ├── spiders/
│       │   └── spiderbook.py # Spider principal pour books.toscrape.com
│       ├── items.py          # Définition des items Scrapy
│       ├── pipelines.py      # Pipeline de transformation
│       └── settings.py       # Configuration Scrapy
│
├── 🚀 book_api/              # API FastAPI - Clean Architecture
│   ├── domain/               # 🏛️ COUCHE DOMAIN
│   │   ├── entities/         # Entités métier (Book, Genre)
│   │   └── value_objects/    # Value objects (Price)
│   │
│   ├── use_cases/            # 💼 COUCHE USE CASES
│   │   ├── interfaces/       # Interfaces abstraites (IRepository, IService)
│   │   └── services/         # Services métier (logique de calculs)
│   │
│   ├── interface/            # 🌐 COUCHE INTERFACE
│   │   ├── api/              # Routes FastAPI (book_router, genre_router)
│   │   └── dto/              # DTOs Pydantic (BookDto, ResponseDto)
│   │
│   ├── infrastructure/       # 🔧 COUCHE INFRASTRUCTURE
│   │   ├── database/         # Connexion DB et modèles SQLAlchemy
│   │   └── repositories/     # Implémentations concrètes des repositories
│   │
│   ├── config/               # ⚙️ CONFIGURATION
│   │   ├── dependencies.py   # Dependency Injection FastAPI
│   │   └── logging.py        # Configuration des logs
│   │
│   ├── tests/                # 🧪 TESTS
│   │   ├── unit/             # Tests unitaires avec mocks
│   │   └── conftest.py       # Fixtures pytest
│   │
│   ├── app/                  # 📦 LEGACY (garde books.db)
│   │   └── books.db          # Base de données SQLite (1000 livres)
│   │
│   └── main.py               # 🚀 Point d'entrée FastAPI Clean
│
├── 📊 Données
│   ├── books.csv             # Export CSV des livres scrapés
│   ├── books.db              # Base de données principale
│   └── book_database.db      # Base alternative
│
└── 📋 Configuration
    ├── requirements.txt      # Dépendances Python globales
    ├── requirements_clean.txt # Dépendances Clean Architecture
    └── run_api.py            # Script de lancement simplifié
```

---

## 🏗️ Architecture Clean - Les 4 couches

### 🏛️ 1. Domain (Métier)
```python
# Entités avec règles métier
class Book:
    def is_in_stock(self) -> bool
    def has_valid_price(self) -> bool
    def calculate_tax_amount(self) -> Decimal
```

### 💼 2. Use Cases (Logique applicative)
```python
# Services métier
class BookService:
    def calculate_average_price_all(self) -> Dict
    def calculate_average_stock_by_genre(self, genre_id) -> Dict
```

### 🌐 3. Interface (API)
```python
# Routes FastAPI propres
@router.get("/books/average_price/all", response_model=AveragePriceResponseDto)
def get_average_price_all(book_service: IBookService = Depends(get_book_service)):
    return book_service.calculate_average_price_all()
```

### 🔧 4. Infrastructure (Technique)
```python
# Repositories concrets
class BookRepository(IBookRepository):
    def get_all(self) -> List[Book]
    def get_by_keyword(self, keyword: str) -> List[Book]
```

---

## 🚀 Démarrage rapide

### 1. Installation
```bash
# Cloner le projet
git clone <repo-url>
cd bookscrape

# Installer les dépendances
pip install -r requirements_clean.txt
```

### 2. Lancer l'API Clean Architecture
```bash
# Démarrage avec uvicorn
uvicorn book_api.main:app --reload --port 8001

# Ou avec le script
python run_api.py
```

### 3. Accéder à l'API
- **Documentation** : http://localhost:8001/docs
- **API Alternative** : http://localhost:8001/redoc
- **Health Check** : http://localhost:8001/health

---

## 📡 Endpoints disponibles

### 📚 Livres
| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/books` | GET | Tous les livres |
| `/books/search/{keyword}` | GET | Recherche par mot-clé |
| `/books/by_genre/{genre_id}` | GET | Livres par genre |
| `/books/average_price/all` | GET | Prix moyen global |
| `/books/average_price/genre/{genre_id}` | GET | Prix moyen par genre |
| `/books/average_stock/all` | GET | Stock moyen global |
| `/books/average_stock/genre/{genre_id}` | GET | Stock moyen par genre |

### 🏷️ Genres
| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/genres` | GET | Tous les genres |
| `/genres/{genre_id}` | GET | Genre par ID |

### 🔍 Exemples d'utilisation
```bash
# Tous les livres
curl http://localhost:8001/books

# Prix moyen global (exemple Clean Architecture)
curl http://localhost:8001/books/average_price/all
# Retourne: {"total_books": 1000, "books_with_price": 1000, "average_price": 35.07}

# Recherche
curl http://localhost:8001/books/search/python

# Prix moyen par genre
curl http://localhost:8001/books/average_price/genre/1
```

---

## 🕷️ Web Scraping (Scrapy)

### Lancer le scraping
```bash
cd book_scrape
scrapy crawl spiderbook
```

### Source des données
- **Site scrapé** : [books.toscrape.com](http://books.toscrape.com)
- **Données extraites** : Titre, prix, stock, note, genre, description, UPC
- **Format de sortie** : SQLite + CSV

---

## 🧪 Tests

### Tests unitaires avec mocks
```bash
# Lancer tous les tests
pytest book_api/tests/

# Tests avec couverture
pytest book_api/tests/ --cov=book_api

# Tests spécifiques
pytest book_api/tests/unit/test_book_service.py
```

### Exemples de tests
```python
def test_calculate_average_price_all_with_valid_books(self):
    # Arrange: Mock dependencies
    test_books = [Book(id=1, price_taxed=Decimal("10.00"))]
    self.mock_book_repo.get_all.return_value = test_books

    # Act: Call service
    result = self.service.calculate_average_price_all()

    # Assert: Verify results
    assert result["average_price"] == 10.00
```

---

## 🎯 Design Patterns utilisés

- ✅ **Repository Pattern** : Abstraction de l'accès aux données
- ✅ **Service Layer Pattern** : Logique métier centralisée
- ✅ **Dependency Injection** : Inversion de contrôle avec FastAPI
- ✅ **DTO Pattern** : Séparation entités/transport
- ✅ **Interface Segregation** : Interfaces spécialisées

---

## 📈 Métriques du projet

- **Livres scrapés** : 1000+
- **Genres disponibles** : 50+
- **Couverture de tests** : Entités + Services
- **Endpoints API** : 10+
- **Architecture** : Clean Architecture (4 couches)

---

## 🛠️ Technologies utilisées

### Backend
- **FastAPI** : Framework web moderne et rapide
- **SQLAlchemy** : ORM pour la base de données
- **Pydantic** : Validation et sérialisation des données
- **SQLite** : Base de données légère

### Scraping
- **Scrapy** : Framework de web scraping
- **Pandas** : Manipulation des données (export CSV)

### Tests & Qualité
- **Pytest** : Framework de tests
- **Mock** : Tests unitaires avec mocks
- **Black** : Formatage du code
- **MyPy** : Vérification des types

---

## 🔄 Évolution du projet

### Version 1.0 (Legacy)
- Structure monolithique dans `book_api/app/`
- Logique métier dans les routes
- Couplage fort

### Version 2.0 (Clean Architecture) ✅
- Architecture en 4 couches
- Séparation des responsabilités
- Code testable et maintenable
- Dependency Injection
- DTOs typés

---

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commiter les changes (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Push sur la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrir une Pull Request

---

## 📝 License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👨‍💻 Auteur

Projet développé dans le cadre d'une formation Simplon - Refactorisation selon les principes Clean Code et Clean Architecture.

**🎯 Objectifs pédagogiques atteints :**
- ✅ Clean Architecture
- ✅ Design Patterns
- ✅ Tests unitaires
- ✅ Dependency Injection
- ✅ API REST documentée