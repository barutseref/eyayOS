# 🚀 EyAy.OS 2.0 - Kapsamlı Kurulum ve Geliştirme Rehberi

## 📋 İçindekiler

1. [Proje Genel Bakış](#proje-genel-bakış)
2. [Sistem Gereksinimleri](#sistem-gereksinimleri)
3. [Hızlı Başlangıç](#hızlı-başlangıç)
4. [Mikroservis Mimarisi](#mikroservis-mimarisi)
5. [Adım Adım Kurulum](#adım-adım-kurulum)
6. [Geliştirme Ortamı](#geliştirme-ortamı)
7. [Production Deployment](#production-deployment)
8. [İzleme ve Bakım](#izleme-ve-bakım)

## 🎯 Proje Genel Bakış

EyAy.OS 2.0, modern mikroservis mimarisi ile geliştirilmiş Türkçe AI asistan platformudur.

### Temel Özellikler
- **Mikroservis Mimarisi**: 6 bağımsız servis
- **Türkçe AI Desteği**: Özel Türkçe NLP modelleri
- **Gerçek Zamanlı İletişim**: WebSocket desteği
- **Ölçeklenebilir Altyapı**: Docker + Kubernetes
- **Modern Tech Stack**: FastAPI, React, PostgreSQL, Redis

### Servis Listesi
1. **Yetkilendirme Servisi** (Port: 8001) - JWT tabanlı kimlik doğrulama
2. **Dil İşleme Servisi** (Port: 8002) - Türkçe NLP ve AI
3. **Konuşma Servisi** (Port: 8003) - Ses tanıma ve sentezi
4. **Hafıza Servisi** (Port: 8004) - Konuşma hafızası ve vektör DB
5. **Sohbet Servisi** (Port: 8005) - Gerçek zamanlı sohbet
6. **Analiz Servisi** (Port: 8006) - Metrikler ve dashboard

## 💻 Sistem Gereksinimleri

### Minimum Gereksinimler
- **CPU**: 4 core (Intel i5 veya AMD Ryzen 5)
- **RAM**: 8 GB
- **Disk**: 50 GB SSD
- **OS**: Ubuntu 20.04+, macOS 12+, Windows 11

### Önerilen Gereksinimler
- **CPU**: 8 core (Intel i7 veya AMD Ryzen 7)
- **RAM**: 16 GB
- **Disk**: 100 GB NVMe SSD
- **GPU**: NVIDIA GTX 1060+ (AI modelleri için)

### Yazılım Gereksinimleri
- **Python**: 3.11+
- **Node.js**: 18+
- **Docker**: 24.0+
- **Docker Compose**: 2.20+
- **Git**: 2.30+

## ⚡ Hızlı Başlangıç

### 1. Repository Klonlama
```bash
git clone https://github.com/barutseref/EyAy.OS.git
cd EyAy.OS
```

### 2. Geliştirme Ortamını Başlatma
```bash
# Docker Compose ile tüm servisleri başlat
docker-compose up -d

# Servislerin durumunu kontrol et
docker-compose ps

# Logları izle
docker-compose logs -f
```

### 3. Frontend Başlatma
```bash
cd frontend/web-app
npm install
npm run dev
```

### 4. Test Etme
```bash
# Sağlık kontrolü
curl http://localhost:8001/saglik  # Yetkilendirme
curl http://localhost:8002/saglik  # Dil İşleme
curl http://localhost:8003/saglik  # Konuşma
curl http://localhost:8004/saglik  # Hafıza
curl http://localhost:8005/saglik  # Sohbet
curl http://localhost:8006/saglik  # Analiz
```

## 🏗️ Mikroservis Mimarisi

```
┌─────────────────────────────────────────────────────────────┐
│                    EyAy.OS 2.0 Architecture                │
├─────────────────────────────────────────────────────────────┤
│  Frontend Layer                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │   Web App   │ │ Mobile App  │ │Desktop App  │          │
│  │ (React/Next)│ │(React Native│ │ (Electron)  │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
├─────────────────────────────────────────────────────────────┤
│  API Gateway (Kong/Traefik)                                │
├─────────────────────────────────────────────────────────────┤
│  Microservices Layer                                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │Yetkilendirme│ │Dil İşleme   │ │  Konuşma    │          │
│  │   :8001     │ │   :8002     │ │   :8003     │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │   Hafıza    │ │   Sohbet    │ │   Analiz    │          │
│  │   :8004     │ │   :8005     │ │   :8006     │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
├─────────────────────────────────────────────────────────────┤
│  Data Layer                                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │ PostgreSQL  │ │    Redis    │ │   Qdrant    │          │
│  │ (Ana Veri)  │ │  (Cache)    │ │ (Vector DB) │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
├─────────────────────────────────────────────────────────────┤
│  Infrastructure                                            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │   Docker    │ │ Kubernetes  │ │ Monitoring  │          │
│  │ Containers  │ │Orchestration│ │(Prometheus) │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## 📝 Adım Adım Kurulum

### Adım 1: Proje Yapısını Oluşturma

```bash
# Ana dizini oluştur
mkdir EyAy.OS
cd EyAy.OS

# Git repository başlat
git init
git branch -M main

# Proje yapısını oluştur
mkdir -p .github/workflows
mkdir -p hizmetler/{yetkilendirme,dil_isleme,konusma,hafiza,sohbet,analiz}
mkdir -p frontend/{web-app,mobile-app,desktop-app}
mkdir -p infrastructure/{docker,kubernetes,helm}
mkdir -p shared/{schemas,utils,types}
mkdir -p docs tests scripts

# Her servis için temel yapı
for service in yetkilendirme dil_isleme konusma hafiza sohbet analiz; do
    mkdir -p hizmetler/$service/{app,tests,migrations}
    touch hizmetler/$service/{pyproject.toml,Dockerfile,README.md}
done
```

### Adım 2: Ana Docker Compose Dosyası

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Veritabanları
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: eyay
      POSTGRES_USER: eyay
      POSTGRES_PASSWORD: eyay123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - eyay-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - eyay-network

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
    networks:
      - eyay-network

  # Mikroservisler
  yetkilendirme:
    build: ./hizmetler/yetkilendirme
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgresql://eyay:eyay123@postgres:5432/eyay
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    networks:
      - eyay-network

  dil-isleme:
    build: ./hizmetler/dil_isleme
    ports:
      - "8002:8002"
    environment:
      - REDIS_URL=redis://redis:6379/1
    depends_on:
      - redis
    networks:
      - eyay-network

  konusma:
    build: ./hizmetler/konusma
    ports:
      - "8003:8003"
    environment:
      - REDIS_URL=redis://redis:6379/2
    depends_on:
      - redis
    networks:
      - eyay-network

  hafiza:
    build: ./hizmetler/hafiza
    ports:
      - "8004:8004"
    environment:
      - DATABASE_URL=postgresql://eyay:eyay123@postgres:5432/eyay
      - REDIS_URL=redis://redis:6379/3
      - QDRANT_URL=http://qdrant:6333
    depends_on:
      - postgres
      - redis
      - qdrant
    networks:
      - eyay-network

  sohbet:
    build: ./hizmetler/sohbet
    ports:
      - "8005:8005"
    environment:
      - DATABASE_URL=postgresql://eyay:eyay123@postgres:5432/eyay
      - REDIS_URL=redis://redis:6379/4
    depends_on:
      - postgres
      - redis
    networks:
      - eyay-network

  analiz:
    build: ./hizmetler/analiz
    ports:
      - "8006:8006"
    environment:
      - DATABASE_URL=postgresql://eyay:eyay123@postgres:5432/eyay
      - REDIS_URL=redis://redis:6379/5
    depends_on:
      - postgres
      - redis
    networks:
      - eyay-network

  # API Gateway
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./infrastructure/nginx/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - yetkilendirme
      - dil-isleme
      - konusma
      - hafiza
      - sohbet
      - analiz
    networks:
      - eyay-network

volumes:
  postgres_data:
  redis_data:
  qdrant_data:

networks:
  eyay-network:
    driver: bridge
```

### Adım 3: Her Servisi Kurma

#### Yetkilendirme Servisi
```bash
cd hizmetler/yetkilendirme

# pyproject.toml oluştur (template'den kopyala)
cp ../../yetkilendirme-servisi-template.md/pyproject.toml .

# Poetry ile bağımlılıkları yükle
poetry install

# Alembic ile veritabanı migration
poetry run alembic init migrations
poetry run alembic revision --autogenerate -m "Initial migration"
poetry run alembic upgrade head

# Test et
poetry run uvicorn app.eyay:app --reload --port 8001
```

#### Dil İşleme Servisi
```bash
cd ../dil_isleme

# Bağımlılıkları yükle
poetry install

# Türkçe NLP modellerini indir
poetry run python -c "
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer

# Duygu analizi modeli
AutoTokenizer.from_pretrained('savasy/bert-base-turkish-sentiment-cased')
AutoModelForSequenceClassification.from_pretrained('savasy/bert-base-turkish-sentiment-cased')

# Embedding modeli
SentenceTransformer('emrecan/bert-base-turkish-cased-mean-nli-stsb-tr')
"

# Test et
poetry run uvicorn app.eyay:app --reload --port 8002
```

#### Konuşma Servisi
```bash
cd ../konusma

# Bağımlılıkları yükle
poetry install

# Whisper modelini indir
poetry run python -c "import whisper; whisper.load_model('base')"

# Test et
poetry run uvicorn app.eyay:app --reload --port 8003
```

#### Hafıza Servisi
```bash
cd ../hafiza

# Bağımlılıkları yükle
poetry install

# Veritabanı migration
poetry run alembic upgrade head

# Test et
poetry run uvicorn app.eyay:app --reload --port 8004
```

#### Sohbet Servisi
```bash
cd ../sohbet

# Bağımlılıkları yükle
poetry install

# Veritabanı migration
poetry run alembic upgrade head

# Test et
poetry run uvicorn app.eyay:app --reload --port 8005
```

#### Analiz Servisi
```bash
cd ../analiz

# Bağımlılıkları yükle
poetry install

# Veritabanı migration
poetry run alembic upgrade head

# Test et
poetry run uvicorn app.eyay:app --reload --port 8006
```

### Adım 4: Frontend Kurulumu

```bash
cd frontend/web-app

# Next.js projesi oluştur
npx create-next-app@latest . --typescript --tailwind --eslint --app

# EyAy.OS için özel bağımlılıklar
npm install @tanstack/react-query axios socket.io-client
npm install -D @types/node

# Geliştirme sunucusunu başlat
npm run dev
```

### Adım 5: API Gateway Konfigürasyonu

```nginx
# infrastructure/nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream yetkilendirme {
        server yetkilendirme:8001;
    }
    
    upstream dil-isleme {
        server dil-isleme:8002;
    }
    
    upstream konusma {
        server konusma:8003;
    }
    
    upstream hafiza {
        server hafiza:8004;
    }
    
    upstream sohbet {
        server sohbet:8005;
    }
    
    upstream analiz {
        server analiz:8006;
    }

    server {
        listen 80;
        server_name localhost;

        # API routes
        location /api/v1/auth/ {
            proxy_pass http://yetkilendirme/api/v1/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /api/v1/nlp/ {
            proxy_pass http://dil-isleme/api/v1/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /api/v1/speech/ {
            proxy_pass http://konusma/api/v1/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /api/v1/memory/ {
            proxy_pass http://hafiza/api/v1/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /api/v1/chat/ {
            proxy_pass http://sohbet/api/v1/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            
            # WebSocket support
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        location /api/v1/analytics/ {
            proxy_pass http://analiz/api/v1/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Frontend
        location / {
            proxy_pass http://frontend:3000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

## 🔧 Geliştirme Ortamı

### VS Code Konfigürasyonu

```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./hizmetler/yetkilendirme/.venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/node_modules": true
    }
}
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
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
        language_version: python3.11

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.287
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

### GitHub Actions CI/CD

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-services:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [yetkilendirme, dil_isleme, konusma, hafiza, sohbet, analiz]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install Poetry
      uses: snok/install-poetry@v1
    
    - name: Install dependencies
      run: |
        cd hizmetler/${{ matrix.service }}
        poetry install
    
    - name: Run tests
      run: |
        cd hizmetler/${{ matrix.service }}
        poetry run pytest
    
    - name: Run linting
      run: |
        cd hizmetler/${{ matrix.service }}
        poetry run black --check .
        poetry run ruff check .

  build-images:
    needs: test-services
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Login to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push images
      run: |
        for service in yetkilendirme dil_isleme konusma hafiza sohbet analiz; do
          docker build -t eyayos/$service:latest ./hizmetler/$service
          docker push eyayos/$service:latest
        done

  deploy:
    needs: build-images
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to production
      run: |
        echo "Production deployment would happen here"
        # kubectl apply -f infrastructure/kubernetes/
```

## 🚀 Production Deployment

### Kubernetes Deployment

```yaml
# infrastructure/kubernetes/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: eyayos
---
# infrastructure/kubernetes/postgres.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: eyayos
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        env:
        - name: POSTGRES_DB
          value: "eyay"
        - name: POSTGRES_USER
          value: "eyay"
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: eyayos
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
```

### Helm Chart

```yaml
# infrastructure/helm/eyayos/Chart.yaml
apiVersion: v2
name: eyayos
description: EyAy.OS Helm Chart
version: 0.1.0
appVersion: "0.1.0"

# infrastructure/helm/eyayos/values.yaml
replicaCount: 3

image:
  repository: eyayos
  pullPolicy: IfNotPresent
  tag: "latest"

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: "nginx"
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
  hosts:
    - host: eyayos.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: eyayos-tls
      hosts:
        - eyayos.com

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
```

### Monitoring Stack

```yaml
# infrastructure/monitoring/prometheus.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: eyayos
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
    - job_name: 'eyayos-services'
      static_configs:
      - targets: 
        - 'yetkilendirme-service:8001'
        - 'dil-isleme-service:8002'
        - 'konusma-service:8003'
        - 'hafiza-service:8004'
        - 'sohbet-service:8005'
        - 'analiz-service:8006'
```

## 📊 İzleme ve Bakım

### Sağlık Kontrolleri

```bash
#!/bin/bash
# scripts/health-check.sh

services=("yetkilendirme:8001" "dil-isleme:8002" "konusma:8003" "hafiza:8004" "sohbet:8005" "analiz:8006")

echo "🔍 EyAy.OS Sağlık Kontrolü"
echo "=========================="

for service in "${services[@]}"; do
    name=$(echo $service | cut -d: -f1)
    port=$(echo $service | cut -d: -f2)
    
    if curl -s "http://localhost:$port/saglik" > /dev/null; then
        echo "✅ $name servisi çalışıyor"
    else
        echo "❌ $name servisi çalışmıyor"
    fi
done

echo ""
echo "🗄️ Veritabanı Kontrolleri"
echo "========================"

# PostgreSQL kontrolü
if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "✅ PostgreSQL çalışıyor"
else
    echo "❌ PostgreSQL çalışmıyor"
fi

# Redis kontrolü
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis çalışıyor"
else
    echo "❌ Redis çalışmıyor"
fi

# Qdrant kontrolü
if curl -s "http://localhost:6333/health" > /dev/null; then
    echo "✅ Qdrant çalışıyor"
else
    echo "❌ Qdrant çalışmıyor"
fi
```

### Log Toplama

```yaml
# infrastructure/logging/fluentd.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: eyayos
spec:
  selector:
    matchLabels:
      name: fluentd
  template:
    metadata:
      labels:
        name: fluentd
    spec:
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1-debian-elasticsearch
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch.logging.svc.cluster.local"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

### Backup Stratejisi

```bash
#!/bin/bash
# scripts/backup.sh

BACKUP_DIR="/backups/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

echo "🗄️ Veritabanı yedekleme başlıyor..."

# PostgreSQL backup
pg_dump -h localhost -U eyay eyay > $BACKUP_DIR/postgres_backup.sql

# Redis backup
redis-cli --rdb $BACKUP_DIR/redis_backup.rdb

# Qdrant backup
curl -X POST "http://localhost:6333/collections/eyay_hafiza/snapshots" > $BACKUP_DIR/qdrant_backup.json

echo "✅ Yedekleme tamamlandı: $BACKUP_DIR"

# Eski yedekleri temizle (30 günden eski)
find /backups -type d -mtime +30 -exec rm -rf {} \;
```

## 🎯 Sonraki Adımlar

### Faz 1: Temel Kurulum (1-2 Hafta)
- [x] Proje yapısı oluşturma
- [x] Docker Compose konfigürasyonu
- [x] Temel servis template'leri
- [ ] CI/CD pipeline kurulumu

### Faz 2: Servis Geliştirme (3-4 Hafta)
- [ ] Yetkilendirme servisi tamamlama
- [ ] Dil işleme servisi AI entegrasyonu
- [ ] Konuşma servisi Whisper entegrasyonu
- [ ] Hafıza servisi vektör DB entegrasyonu

### Faz 3: Frontend Geliştirme (2-3 Hafta)
- [ ] React/Next.js web uygulaması
- [ ] WebSocket entegrasyonu
- [ ] Responsive tasarım
- [ ] PWA özellikleri

### Faz 4: Production Hazırlık (1-2 Hafta)
- [ ] Kubernetes deployment
- [ ] Monitoring ve logging
- [ ] Security hardening
- [ ] Performance optimization

### Faz 5: Test ve Deployment (1 Hafta)
- [ ] End-to-end testler
- [ ] Load testing
- [ ] Security testing
- [ ] Production deployment

## 📞 Destek ve Katkı

### Geliştirici Topluluğu
- **GitHub**: https://github.com/barutseref/EyAy.OS
- **Discord**: EyAy.OS Geliştirici Sunucusu
- **Email**: barutseref@barutben.com

### Katkıda Bulunma
1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request olu
