import os
import shutil
import toml

def migrate_app_to_src(service_path):
    app_path = os.path.join(service_path, "app")
    src_path = os.path.join(service_path, "src")
    dest_path = os.path.join(src_path, "app")
    pyproject_path = os.path.join(service_path, "pyproject.toml")

    if not os.path.exists(app_path):
        print(f"[!] 'app/' klasörü yok, atlanıyor: {service_path}")
        return

    # src klasörü oluştur
    os.makedirs(src_path, exist_ok=True)

    # Hedefte zaten app varsa sil (opsiyonel/güvenlik amaçlı)
    if os.path.exists(dest_path):
        print(f"[!] 'src/app/' zaten var, yeniden taşıyacağım: {dest_path}")
        shutil.rmtree(dest_path)

    # app → src/app taşı
    shutil.move(app_path, dest_path)
    print(f"[✓] Taşındı: {app_path} → {dest_path}")

    # pyproject.toml güncelle
    if not os.path.exists(pyproject_path):
        print(f"[!] pyproject.toml bulunamadı: {service_path}")
        return

    with open(pyproject_path, "r", encoding="utf-8") as f:
        data = toml.load(f)

    poetry_config = data.get("tool", {}).get("poetry", {})
    if "packages" in poetry_config:
        print(f"[=] packages zaten tanımlı, dokunulmadı: {pyproject_path}")
    else:
        poetry_config["packages"] = [{"include": "app", "from": "src"}]
        data["tool"]["poetry"] = poetry_config
        with open(pyproject_path, "w", encoding="utf-8") as f:
            toml.dump(data, f)
        print(f"[✓] pyproject.toml güncellendi: {pyproject_path}")

def main():
    servisler_dizini = "servisler"
    for servis_ad in os.listdir(servisler_dizini):
        servis_yolu = os.path.join(servisler_dizini, servis_ad)
        if os.path.isdir(servis_yolu):
            migrate_app_to_src(servis_yolu)

if __name__ == "__main__":
    main()
