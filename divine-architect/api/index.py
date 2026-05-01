from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
import os, urllib.parse, json, random, requests, base64

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SYSTEM_PROMPT = """Anda adalah Divine Architect Agent, spesialis pembuatan karakter dewa-dewi bergaya Manhwa/Novel High-Fantasy.

Hasilkan OUTPUT JSON seperti ini (langsung JSON, tanpa teks lain):
{
  "nama": "Nama Dewa Lengkap",
  "domain": "Domain1, Domain2, Domain3",
  "power_level": "BEYOND CONCEPT",
  "lore": "3-4 paragraf puitis Bahasa Indonesia, pisah dengan \\n\\n",
  "quote": "Satu kutipan ikonik Bahasa Indonesia",
  "abilities": [
    {"name": "Nama Ability", "desc": "Deskripsi singkat"},
    {"name": "Nama Ability", "desc": "Deskripsi singkat"},
    {"name": "Nama Ability", "desc": "Deskripsi singkat"},
    {"name": "Nama Ability", "desc": "Deskripsi singkat"},
    {"name": "Nama Ability", "desc": "Deskripsi singkat"}
  ],
  "image_prompt": "1 male/female god, [deskripsikan: warna rambut, warna mata, kostum detail, pose, elemen unik seperti multiple eyes/black hole chest/celestial chains/floating halos], cosmic nebula background, divine light rays, manhwa style, anime illustration, masterpiece, best quality, ultra detailed, 8k, sharp focus, perfect anatomy, beautiful face, glowing ethereal aura",
  "negative_prompt": "lowres, bad anatomy, blurry, ugly, deformed, extra limbs, missing fingers, worst quality, realistic photo, 3d render, watermark, text"
}"""

class GenerateRequest(BaseModel):
    concept: str
    model: str = "llama-3.3-70b-versatile"

@app.get("/api/health")
async def health():
    return {"status": "online", "message": "Divine Architect AI is ready."}

@app.post("/api/generate")
async def generate(req: GenerateRequest):
    groq_key = os.environ.get("GROQ_API_KEY")
    hf_token = os.environ.get("HF_TOKEN")
    if not groq_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not set")

    try:
        from groq import Groq
        client = Groq(api_key=groq_key)
        completion = client.chat.completions.create(
            model=req.model,
            max_tokens=2000,
            temperature=0.9,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Buat karakter dewa: {req.concept}"}
            ],
            response_format={"type": "json_object"}
        )
        data = json.loads(completion.choices[0].message.content)

        img_prompt = data.get("image_prompt", req.concept)
        neg_prompt = data.get("negative_prompt", "lowres, bad anatomy, blurry")

        # Coba Hugging Face dulu (kualitas lebih bagus)
        if hf_token:
            try:
                hf_url = "https://api-inference.huggingface.co/models/cagliostrolab/animagine-xl-3.1"
                hf_res = requests.post(
                    hf_url,
                    headers={"Authorization": f"Bearer {hf_token}"},
                    json={
                        "inputs": img_prompt + ", masterpiece, best quality, ultra detailed, sharp focus",
                        "parameters": {
                            "negative_prompt": neg_prompt,
                            "width": 832,
                            "height": 1216,
                            "num_inference_steps": 28,
                            "guidance_scale": 7,
                            "seed": random.randint(1, 999999)
                        }
                    },
                    timeout=60
                )
                if hf_res.status_code == 200 and hf_res.headers.get("content-type","").startswith("image"):
                    img_b64 = base64.b64encode(hf_res.content).decode()
                    data["image_url"] = f"data:image/jpeg;base64,{img_b64}"
                    data["image_source"] = "animagine-xl"
                    return JSONResponse(content=data)
            except Exception:
                pass  # Fallback ke Pollinations

        # Fallback: Pollinations
        seed = random.randint(1, 999999)
        encoded = urllib.parse.quote(img_prompt + ", manhwa illustration, masterpiece, best quality, 8k")
        encoded_neg = urllib.parse.quote(neg_prompt)
        data["image_url"] = (
            f"https://image.pollinations.ai/prompt/{encoded}"
            f"?width=832&height=1216&model=flux&seed={seed}&nologo=true&enhance=true&negative={encoded_neg}"
        )
        data["image_source"] = "pollinations"
        return JSONResponse(content=data)

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"JSON parse error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
