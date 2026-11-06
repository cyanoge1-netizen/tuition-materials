# 📚 Tuition Materials

A complete, ad-free digital repository of Bangladesh National Curriculum (NCTB) textbooks, Dakhil Madrasah textbooks, and chapter-wise guide books (Panjeree / Lecture) for primary and secondary classes.

---

## 🗂️ Repository Structure

```text
tuition-materials/
├── manifest.json              # Catalog index with file paths, sizes and download URLs
├── download_materials.py       # Standalone interactive & CLI downloader
├── Curriculum/                # Primary Curriculum & Assessment Guidelines 2026
├── Class 3/                   # Class 3 NCTB Textbooks & Syllabus Plan
├── Class 4/                   # Class 4 NCTB Textbooks & Syllabus Plan
├── Class 5/                   # Class 5 NCTB Textbooks & Syllabus Plan
└── Class 6/
    ├── Textbooks/             # Class 6 NCTB General Textbooks (All 16 Subjects)
    ├── Dakhil/                # Class 6 Dakhil Madrasah Textbooks (Quran, Aqaid, Arabic)
    └── Guides/                # Chapter-wise Guide Books (Panjeree / Lecture)
        ├── গণিত_পাঞ্জারি/
        ├── তথ্য_ও_যোগাযোগ_প্রযুক্তি_পাঞ্জারি/
        └── দাখিল_কুরআন_মাজিদ_ও_তাজভিদ/
```

---

## 🚀 How to Download (Ad-Free & App-Independent)

### Method 1: Interactive Downloader (Recommended)
Run the script without arguments for an interactive menu with progress bars:

```bash
python3 download_materials.py
```

### Method 2: Command-Line Flags
You can download specific classes or categories directly:

```bash
# Download a specific class
python3 download_materials.py --class 5
python3 download_materials.py --class 6

# Download only Dakhil books
python3 download_materials.py --dakhil

# Download only guide books
python3 download_materials.py --guides

# Download everything (1.45 GB)
python3 download_materials.py --all

# Custom destination directory
python3 download_materials.py --class 6 --dest /sdcard/Documents/TUITION
```

### Method 3: Direct Download via `curl` / `wget`
Any individual file can be downloaded directly from GitHub:
```bash
curl -O "https://raw.githubusercontent.com/cyanoge1-netizen/tuition-materials/main/Class%206/Textbooks/Class_6_%E0%A6%97%E0%A6%A3%E0%A6%BF%E0%A6%A4.pdf"
```

---

## 📊 Summary of Materials

| Category | Files | Total Size |
| :--- | :---: | :---: |
| **Curriculum** | 7 files | 16.3 MB |
| **Class 3** | 7 files | 208.9 MB |
| **Class 4** | 7 files | 264.7 MB |
| **Class 5** | 7 files | 327.0 MB |
| **Class 6 Textbooks** | 16 files | 367.6 MB |
| **Class 6 Dakhil** | 4 files | 171.9 MB |
| **Class 6 Guides** | 8 files | 101.4 MB |
| **Total** | **56 files** | **1,457.85 MB (~1.46 GB)** |
