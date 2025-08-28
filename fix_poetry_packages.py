import os
import toml

def fix_pyproject_toml(path):
    pyproject_path = os.path.join(path, "pyproject.toml")
    if not os.path.isfile(pyproject_path):
        return

    try:
        with open(pyproject_path, "r", encoding="utf-8") as f:
            data = toml.load(f)

        poetry_config = data.get("tool", {}).get("poetry", {})
        if not poetry_config:
            print(f"[!] 'tool.poetry' bölümü eksik: {pyproject_path}")
            return

        if "packages" in poetry_config:
            print(f"[=] Zaten 'packages' tanımlı: {pyproject_path}")
            return

        # 'src/app/' klasörü var mı?
        if not os.path.isdir(os.path.join(path, "src", "app")):
            print(f"[!] 'src/app/' klasörü bulunamadı: {path}")
            return

        # 'packages' alanını ekle
        poetry_config["packages"] = [{"include": "app", "from": "src"}]
        data["tool"]["poetry"] = poetry_config

        with open(pyproject_path, "w", encoding="utf-8") as f:
            toml.dump(data, f)

        print(f"[✓] 'packages' eklendi: {pyproject_path}")

    except Exception as e:
        print(f"[!!] Hata oluştu: {pyproject_path} — {e}")

def main():
    root_dir = "servisler"
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "pyproject.toml" in filenames:
            fix_pyproject_toml(dirpath)

if __name__ == "__main__":
    main()
