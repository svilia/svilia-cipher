
<div align="center">

```
 ███████╗██╗   ██╗██╗██╗     ██╗ █████╗     ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗
 ██╔════╝██║   ██║██║██║     ██║██╔══██╗   ██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗
 ███████╗╚██╗ ██╔╝██║██║     ██║███████║   ██║     ██║██████╔╝███████║█████╗  ██████╔╝
 ╚════██║ ╚████╔╝ ██║██║     ██║██╔══██║   ██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗
 ███████║  ╚██╔╝  ██║███████╗██║██║  ██║   ╚██████╗██║██║     ██║  ██║███████╗██║  ██║
 ╚══════╝   ╚═╝   ╚═╝╚══════╝╚═╝╚═╝  ╚═╝    ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
```

### *"In cryptography we trust."*

<br>

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge&logo=opensourceinitiative&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-6366f1?style=for-the-badge&logo=gnubash&logoColor=white)
![Zero Deps](https://img.shields.io/badge/Zero_Dependencies-Pure_Python-f59e0b?style=for-the-badge&logo=python&logoColor=white)
![TUI](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-ec4899?style=for-the-badge&logo=windowsterminal&logoColor=white)

<br>

**Classical Cryptography Terminal Suite** — Şifrele, çöz, kır. Terminalde.

</div>

---

## 📦 Features

```
╔══════════════════════════════════════════════════════════════════════╗
║                        SVILIA CIPHER — FEATURES                     ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  ⚔  ENCRYPT       →  8 klasik şifreleme algoritması                 ║
║  🔓  DECRYPT       →  Anahtar tabanlı çözme motoru                  ║
║  💀  AUTO-CRACK    →  Frekans analizi ile otomatik kırma             ║
║  📊  FREQ ANALYSIS →  İngilizce karşılaştırmalı harf dağılımı       ║
║  📖  CIPHER REF    →  Şifre başvuru kılavuzu                        ║
║  🖥️  TUI MODE      →  Tam renkli curses arayüzü                     ║
║  💻  CLI MODE      →  Betik dostu komut satırı modu                 ║
║  🧬  IoC ENGINE    →  Index of Coincidence & Kasiski testi           ║
║  🔤  BIGRAM STATS  →  İkili harf istatistikleri                     ║
║  📄  BASE64 OUT    →  Çıktı otomatik Base64 encode edilir           ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## 🖥️ TUI Preview

```
╔══════════════════════════════════════════════════════════════════════════╗
║                     ⚔  SVILIA CIPHER  ⚔                               ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║   ███████╗██╗   ██╗██╗██╗     ██╗ █████╗                               ║
║   ██╔════╝██║   ██║██║██║     ██║██╔══██╗                              ║
║   ███████╗╚██╗ ██╔╝██║██║     ██║███████║                              ║
║   ╚════██║ ╚████╔╝ ██║██║     ██║██╔══██║                              ║
║   ███████║  ╚██╔╝  ██║███████╗██║██║  ██║                              ║
║   ╚══════╝   ╚═╝   ╚═╝╚══════╝╚═╝╚═╝  ╚═╝                              ║
║                                                                          ║
║         Classical Cryptography Terminal Suite  ·  v1.0.0               ║
║      Caesar · Vigenère · Atbash · Rail Fence · Beaufort · Playfair     ║
║                                                                          ║
║   ╔════════════════════════════════════════╗                            ║
║   ║             MAIN MENU                 ║                            ║
║   ║                                       ║                            ║
║   ║  ▶ ⚔  ENCRYPT                        ║   ← selected               ║
║   ║     🔓  DECRYPT                       ║                            ║
║   ║     💀  AUTO-CRACK / BRUTE            ║                            ║
║   ║     📊  FREQUENCY ANALYSIS            ║                            ║
║   ║     📖  CIPHER REFERENCE              ║                            ║
║   ║     ✖   EXIT                          ║                            ║
║   ╚════════════════════════════════════════╝                            ║
║                                                                          ║
║  ↑↓ Navigate   Enter Select   Q Quit                                    ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 📊 Frequency Analysis — Çıktı Örneği

```
╔══════════════════════════════════════════════════════════════════════╗
║                    FREQUENCY ANALYSIS REPORT                        ║
╠══════════════════════════════════════════════════════════════════════╣
║  Total chars: 312  |  Alpha: 261  |  IoC: 0.06523                  ║
║  → Likely monoalphabetic (Caesar, Atbash, Playfair…)               ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  Letter  Count   %Text   Bar                      exp     diff      ║
║  ─────────────────────────────────────────────────────────────────  ║
║  [E]      33    12.64%  █████████████             12.70%  +0.06%    ║
║  [T]      25     9.58%  ██████████                 9.06%  +0.52%    ║
║  [A]      21     8.05%  ████████                   8.17%  -0.12%    ║
║  [O]      20     7.66%  ████████                   7.51%  +0.15%    ║
║  [I]      18     6.90%  ███████                    6.97%  -0.07%    ║
║  [N]      17     6.51%  ███████                    6.75%  -0.24%    ║
║  ...                                                                 ║
║                                                                      ║
║  TOP BIGRAMS: TH:18  HE:16  IN:14  ER:12  AN:11                    ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## 💀 Auto-Crack — Çıktı Örneği

```
╔══════════════════════════════════════════════════════════════════════╗
║               BRUTE FORCE RESULTS — Caesar                          ║
╠══════════════════════════════════════════════════════════════════════╣
║  Index of Coincidence: 0.06489  (English ≈ 0.065, Random ≈ 0.038) ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  ★ BEST →  Key: 13            Score:   142.87                      ║
║            HELLO WORLD THIS IS A DECRYPTED MESSAGE                  ║
║                                                                      ║
║    #2      Key: 0             Score:    -89.12                      ║
║            URYYB JBEYQ GUVF VF N RAPELCGRQ ZRFFNTR                 ║
║                                                                      ║
║    #3      Key: 7             Score:    -94.45                      ║
║            AXEEH PHKEW MABL BL T LKZKVBMXW FXLLTZX                 ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## 🧠 Cryptanalysis Engine

```
              ┌─────────────────────────┐
              │     INPUT CIPHERTEXT    │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │   Index of Coincidence  │
              │   IoC = Σ(n·(n-1))      │
              │         ─────────       │
              │          N·(N-1)        │
              └──────┬──────────┬───────┘
                     │          │
              IoC≈0.065      IoC≈0.038
                     │          │
         ┌───────────▼──┐  ┌────▼──────────────┐
         │ MONOALPHA    │  │  POLYALPHABETIC    │
         │ Caesar       │  │  Kasiski Test      │
         │ Atbash       │  │  → Key Length Est. │
         │ Playfair     │  │  Friedman Test     │
         └──────┬───────┘  └────┬───────────────┘
                │               │
         ┌──────▼───────────────▼───────┐
         │     FREQUENCY SCORING        │
         │  english_score() per shift   │
         │  Common word bonus (+3 each) │
         └──────────────┬───────────────┘
                        │
         ┌──────────────▼───────────────┐
         │      RANKED RESULTS          │
         │   ★ BEST  ›  Score: 142.87   │
         │      #2   ›  Score:  -89.12  │
         └──────────────────────────────┘
```

---

## 🔐 Supported Ciphers

| # | Cipher | Key Type | Direction | Brute Force |
|---|--------|----------|-----------|-------------|
| 1 | **Caesar** | Number (0–25) | Enc / Dec | ✅ All 26 shifts |
| 2 | **ROT13** | None (fixed) | Symmetric | ✅ Auto |
| 3 | **Atbash** | None | Symmetric | ✅ Auto |
| 4 | **Vigenère** | Keyword | Enc / Dec | ✅ Kasiski + IoC |
| 5 | **Beaufort** | Keyword | Symmetric | ✅ Kasiski |
| 6 | **Rail Fence** | Rails (2–14) | Enc / Dec | ✅ All rail counts |
| 7 | **Columnar** | Keyword | Enc / Dec | ❌ Key required |
| 8 | **Playfair** | Keyword | Enc / Dec | ❌ Key required |

---

## 🚀 Kurulum & Kullanım

```bash
# Bağımlılık yok — pure Python!
git clone https://github.com/svilia/svilia-cipher
cd svilia-cipher

# TUI modunu başlat
python svilia.py

# CLI ile şifrele
python svilia.py -c caesar -e -k 13 -t "Hello World"

# CLI ile çöz
python svilia.py -c vigenere -d -k SECRET -t "Zincs Pgvnu"

# Otomatik kır
python svilia.py -c caesar --crack -t "Khoor Zruog"

# Frekans analizi
python svilia.py --freq -t "Khoor Zruog"

# Tüm şifreleri listele
python svilia.py --list
```

### CLI Seçenekleri

```
usage: svilia.py [-h] [--tui] [-c CIPHER] [-e] [-d] [--crack]
                 [-k KEY] [-t TEXT] [-f FILE] [--freq] [--list]

  --tui          →  İnteraktif TUI'yi başlat
  -c, --cipher   →  Şifre adı (caesar, vigenere, atbash…)
  -e, --encrypt  →  Şifrele
  -d, --decrypt  →  Çöz
  --crack        →  Otomatik kır / brute force
  -k, --key      →  Anahtar (sayı veya kelime)
  -t, --text     →  Giriş metni
  -f, --file     →  Giriş dosyası
  --freq         →  Yalnızca frekans analizi
  --list         →  Tüm şifreleri listele
```

---

## 🛠️ Built With

| Bileşen | Teknoloji | Açıklama |
|---------|-----------|----------|
| **Dil** | Python 3.8+ | Saf Python, sıfır bağımlılık |
| **TUI** | `curses` | Tam renkli terminal arayüzü |
| **Analiz** | `collections.Counter` | Harf frekansı & bigram analizi |
| **Regex** | `re` | Metin temizleme & ayrıştırma |
| **Şifreleme** | El yazımı motorlar | Her şifre sıfırdan implemente edildi |
| **Kriptanaliz** | Kasiski + IoC + Freq | Endüstri standardı teknikler |
| **CLI** | `argparse` | Tam özellikli komut satırı arayüzü |

---

## 📁 Dosya Yapısı

```
svilia-cipher/
├── svilia.py          ← Ana uygulama (TUI + CLI)
├── LICENSE            ← MIT Lisansı
└── README.md          ← Bu dosya
```

---

## 👥 Authors

<div align="center">

<table>
<tr>
<td align="center" width="50%">

### ⚔ svilia
**Lead Developer**

[![GitHub](https://img.shields.io/badge/GitHub-svilia-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/svilia)

```
Cryptography Engine
TUI Architecture
Frequency Analysis
Cipher Core Design
```

*"Kodun kırılmaz, test edilmemiş olduğunda."*

</td>
<td align="center" width="50%">

### 🔥 wortex213433
**Co-Developer**

[![GitHub](https://img.shields.io/badge/GitHub-wortex213433-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/wortex213433)

```
CLI Interface
Testing & QA
Rail Fence Impl.
Columnar Cipher
```

*"Brute force değil, zekâ kullan."*

</td>
</tr>
</table>

</div>

---

## 📜 License

```
MIT License — Copyright (c) 2026 SVILIA CIPHER

Ücretsiz kullanım, değiştirme, dağıtım ve satış hakkı verilmiştir.
Tek şart: telif hakkı bildirimi korunmalıdır.
```

[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)

---

<div align="center">

```
╔══════════════════════════════════════════╗
║                                          ║
║        ⚔  SVILIA CIPHER  v1.0.0  ⚔     ║
║                                          ║
║    "In cryptography we trust."           ║
║                                          ║
║  github.com/svilia  ·  github.com/wortex213433  ║
║                                          ║
╚══════════════════════════════════════════╝
```

*Made with 🔐 and pure Python*

</div>
