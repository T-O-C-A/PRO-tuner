# src/main.py — centrale entrypoint voor PyInstaller builds

import sys
from pathlib import Path

# Zorg dat zowel root als src op sys.path staan (voor veiligheid)
ROOT = Path(__file__).resolve().parents[1]
SRC  = ROOT / "src"
for p in (str(ROOT), str(SRC)):
    if p not in sys.path:
        sys.path.insert(0, p)

# Probeer de run-functie uit onze GUI-app te importeren
# (we dekken beide varianten af: losse modules of package)
try:
    from gui import run_app
except Exception:
    try:
        from pro_tuner.gui import run_app  # als je code in een package zit
    except Exception as e:
        # Laat zien welke bestanden we hebben voor snelle debug
        print("[FOUT] Kon run_app niet importeren:", e)
        print("Bestanden in src/:", list(SRC.glob('*.py')))
        sys.exit(1)

if __name__ == "__main__":
    run_app()
