from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import urllib.parse
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = """Anda adalah Divine Architect Agent, spesialis pembuatan karakter dewa-dewi bergaya Manhwa/Novel High-Fantasy.

Dari konsep yang diberikan, hasilkan OUTPUT dalam format JSON PERSIS seperti ini (tanpa teks lain):
{
  "nama": "Nama Dewa",
  "domain": "Domain1, Domain2, Domain3",
  "power_level": "BEYOND CONCEPT",
  "lore": "Paragraf lore puitis dalam Bahasa Indonesia. 3-4 paragraf, pisahkan dengan \\n\\n",
  "quote": "Kutipan ikonik sang dewa dalam Bahasa Indonesia",
  "abilities": [
    {"name": "Ability Name", "desc": "Deskripsi singkat dalam Bahasa Indonesia"},
    {"name": "Ability Name", "desc": "Deskripsi singkat"},
    {"name": "Ability Name", "desc": "Deskripsi singkat"},
    {"name": "Ability Name", "desc": "Deskripsi singkat"},
    {"name": "Ability Name", "desc": "Deskripsi singkat"}
  ],
  "image_prompt": "detailed english prompt for stable diffusion: character appearance, cosmic elements, manhwa style, masterpiece, ethereal glow, cosmic background, 8k, highly detailed, intricate attire, multiple glowing eyes, celestial chains, floating halos, black hole chest core",
  "negative_prompt": "lowres, bad anatomy, blurry, watermark, signature, ugly, deformed, bad proportions"
}"""

class GenerateRequest(BaseModel):
    concept: str
    model: str = "llama-3.3-70b-versatile"

@app.get("/api/health")
async def health():
    return {"status": "online", "message": "Divine Architect AI is ready."}

@app.post("/api/generate")
async def generate(req: GenerateRequest):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")

    try:
        from groq import Groq
        client = Groq(api_key=api_key)

        completion = client.chat.completions.create(
            model=req.model,
            max_tokens=2000,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Buat karakter dewa dengan konsep: {req.concept}"}
            ],
            response_format={"type": "json_object"}
        )

        import json
        raw = completion.choices[0].message.content
        data = json.loads(raw)

        # Build Pollinations image URL
        img_prompt = data.get("image_prompt", req.concept)
        encoded_prompt = urllib.parse.quote(img_prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&enhance=true&model=flux"

        data["image_url"] = image_url
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
