# OS2 0.1.0 - Modern AI Asistan Kurulum Rehberi

## 🚀  Başlangıç

### 1. Yeni GitHub Deposu Oluşturma

# Yeni dizin oluştur
mkdir os2
cd os2

# Git repository başlat
git init
git branch -M main

# GitHub'da yeni repo oluştur ve bağla
# https://github.com/new adresinden "eyay-2.0" adında repo oluştur
git remote set-url origin git@github.com:barutben61/os2.git

### 2. Proje Yapısını Oluştur

```bash
# Ana dizinler
mkdir -p .github/workflows
mkdir -p servisler/{yetkilendirme-servisi,dil-isleme-servisi,konusma-servisi,hafiza-servisi,sohbet-servisi,analiz-servisi,}
mkdir -p önyüz/{web,mobil,desktop}
mkdir -p altyapı/{docker,kubernetes,helm}
mkdir -p ortak/{schemas,yardımcı,types}
mkdir -p belgeler testler kurulumlar

# Her servis için temel yapı
for service in yetkilendirme-servisi dil-isleme-servisi konusma-servisi hafiza-servisi sohbet-servisi analiz-servisi ; do
    mkdir -p servisler/$service/{app,test,migrations}
    touch servisler/$service/{pyproject.toml,Dockerfile,README.md}
done
```

### 3. Poetry ve Bağımlılık Yönetimi

```bash
# Poetry kurulumu 
curl -sSL https://install.python-poetry.org | python3 -

# Ana proje için pyproject.toml
poetry init --name eyay-2.0 --version 0.1.0 --description "Modern Turkish AI Assistant"
```

### 4. Docker Compose ile Development Environment

```bash
# docker-compose.yml oluştur
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: root
      POSTGRES_PASSWORD: 123As456
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  postgres_data:
  qdrant_data:
EOF
```

### 5. GitHub Actions CI/CD

```bash
# .github/workflows/ci.yml
mkdir -p .github/workflows
cat > .github/workflows/ci.yml << 'EOF'
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install Poetry
      uses: snok/install-poetry@v1
    
    - name: Install dependencies
      run: poetry install
    
    - name: Run tests
      run: poetry run pytest
    
    - name: Run linting
      run: |
        poetry run black --check .
        poetry run ruff check .

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    - name: Build Docker images
      run: |
        docker build -t eyay-2.0:latest .
EOF
```

### 6. Pre-commit Hooks

```bash
# .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.287
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
EOF

# Pre-commit kurulumu
poetry add --group dev pre-commit
poetry run pre-commit install
```

### 7. İlk Commit

```bash
# Temel dosyaları oluştur
echo "# EYAY 2.0 - Modern Turkish AI Assistant" > README.md
echo "__pycache__/\n*.pyc\n.env\n.venv/\nnode_modules/" > .gitignore

# İlk commit
git add .
git commit -m "🎉 Modern mimariye geçişim"
git push -u origin main
```

## 📋 Sonraki Adımlar

1. **Auth Service** geliştirmeye başla
2. **NLP Service** için Turkish models entegre et
3. **Frontend** için React/Next.js setup yap
4. **Docker** containerization tamamla
5. **Kubernetes** deployment hazırla

## 🔗 Faydalı Linkler

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Hugging Face Turkish Models](https://huggingface.co/models?language=tr)
