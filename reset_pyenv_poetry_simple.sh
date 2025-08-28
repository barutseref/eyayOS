#!/bin/bash

PYTHON_VERSION="3.11.13"
SERVISLER_PATH="./servisler"

echo "🧹 [1/3] Servislerin pyproject.toml dosyalarındaki python versiyonları güncelleniyor..."

find "$SERVISLER_PATH" -type f -name "pyproject.toml" | while read -r toml; do
  echo "  Düzenleniyor: $toml"
  # Orijinal satırı değiştir (python = "...") bu satır yoksa ekle
  if grep -q 'python = ' "$toml"; then
    sed -i -E 's/^python = .*/python = ">=3.11,<3.13"/' "$toml"
  else
    # Eğer yoksa [tool.poetry.dependencies] altında python ekleyebiliriz,
    # ama karmaşık olabilir. Basitçe kullanıcı kontrolü için uyarı ver.
    echo "    ⚠ '$toml' içinde python sürümü tanımı bulunamadı, elle kontrol et!"
  fi
done

echo "🚀 [2/3] Python $PYTHON_VERSION pyenv ile kuruluyor (varsa atlanır)..."
pyenv install -s "$PYTHON_VERSION"

echo "⚙️ [3/3] Poetry ortamları güncelleniyor..."
find "$SERVISLER_PATH" -type f -name "pyproject.toml" | while read -r toml; do
  dir=$(dirname "$toml")
  echo "  Servis: $dir"
  cd "$dir" || continue
  poetry env use "$(pyenv which python)"
  poetry install
  cd - >/dev/null || continue
done

echo "✅ İşlem tamamlandı."
