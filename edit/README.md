# Edit: Masak Sardin (edit guna Claude)

Video siap: `../masak-sardin-claude.mp4` (1:03, 1080×1920).

## Susun atur
- `scripts/main.json` – transcript Whisper (word-level) video asal.
- `scripts/edl.json` – senarai potongan (sumber video/audio, speed, caption, grafik, SFX).
- `scripts/finalcut.py` – potong + speed ramp video asal → `hyperframes/cut.mp4` (tidak di-commit, 76MB).
- `scripts/caps.py` – timing caption ikut timeline baru → `caps.json`.
- `scripts/sfx.py` – jana sound FX → `hyperframes/sfx/`.
- `scripts/comp.py` + `comp_template.html` – jana `hyperframes/index.html`.

## Render semula
```bash
python3 scripts/finalcut.py <dir yang ada dl/video.bin>   # hasilkan cut.mp4
cd hyperframes && npx hyperframes@0.8.226 render . -o out.mp4 -q delivery
```

## Gaya (dari video rujukan)
Tajuk Archivo Black warna butter-yellow (#F5D35B) dengan bayang gelap, caption Figtree 800 putih huruf kecil dengan kata kunci kuning, label STEP di atas, pill krim untuk nama bahan.
