# ✦ Divine Architect Agent

> Awaken Gods Beyond Mortal Imagination — Powered by Groq AI + Pollinations.ai

---

## 🚀 Deploy ke Vercel (5 Menit)

### Step 1 — Upload ke GitHub
1. Buat repo baru di [github.com](https://github.com)
2. Upload semua file ini ke repo tersebut

### Step 2 — Connect ke Vercel
1. Login ke [vercel.com](https://vercel.com)
2. Klik **"Add New"** → **"Project"**
3. Import repo GitHub tadi

### Step 3 — Set Environment Variable
Di Vercel dashboard → **Settings** → **Environment Variables**:

| Key | Value |
|-----|-------|
| `GROQ_API_KEY` | `gsk_xxxxxxxxxxxxxxxxxxxx` |

> Daftar Groq API Key gratis di: https://console.groq.com

### Step 4 — Deploy!
Klik **Deploy** — Vercel otomatis install dependencies dan memberikan URL publik.

---

## 📁 Struktur Project

```
divine-architect/
├── api/
│   └── index.py        # FastAPI backend (Groq + Pollinations)
├── index.html          # Frontend UI (Dark Cosmic Theme)
├── requirements.txt    # Python dependencies
├── vercel.json         # Vercel routing config
└── README.md
```

---

## 🛠 Tech Stack

- **Frontend**: Vanilla HTML/CSS/JS — Zero dependencies
- **Backend**: FastAPI (Python Serverless on Vercel)
- **Lore AI**: [Groq API](https://console.groq.com) — Free tier, llama-3.3-70b
- **Image AI**: [Pollinations.ai](https://pollinations.ai) — **100% Free, No API Key**

---

## 🖼 How It Works

1. User mendeskripsikan konsep dewa
2. FastAPI mengirim ke **Groq** → dapat Lore + Image Prompt (JSON)
3. Image prompt di-encode ke URL **Pollinations.ai**
4. Gambar langsung di-fetch via `<img src="https://image.pollinations.ai/prompt/..."/>`

---

## ✦ Features

- Dark Cosmic UI — Manhwa/High Fantasy aesthetic
- Generate Nama, Domain, Lore Puitis (Bahasa Indonesia)
- Generate 5 Abilities unik
- Auto-generate portrait via Pollinations.ai
- Power Level indicator
- Fully responsive
