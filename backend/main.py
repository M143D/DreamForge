# backend/main.py
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from io import BytesIO
import base64
import logging

# --- 日志和设备配置 ---
logging.basicConfig(level=logging.INFO)
# 检查是否有可用的CUDA设备 (NVIDIA GPU)，否则使用CPU
# 如果你有 M1/M2 Mac，可以尝试 "mps"
device = "cuda" if torch.cuda.is_available() else "cpu"
logging.info(f"使用的设备: {device}")
if device == "cpu":
    logging.warning("警告: 正在使用CPU进行计算。生成速度会非常慢。推荐使用配备NVIDIA GPU的设备。")

# --- FastAPI 应用初始化 ---
app = FastAPI()

# --- CORS 中间件配置 ---
# 允许所有来源的跨域请求，方便前后端分离开发
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 模型加载 ---
# 在应用启动时加载模型，避免每次请求都重新加载，节省时间
# 模型会从Hugging Face Hub下载并缓存到本地
# 第一次启动会比较慢，因为需要下载几GB的模型文件
model_id = "runwayml/stable-diffusion-v1-5"
pipe = None

@app.on_event("startup")
def load_model():
    global pipe
    logging.info(f"开始加载模型: {model_id}")
    try:
        # torch_dtype=torch.float16 在使用GPU时可以节省显存并加速
        dtype = torch.float16 if device == "cuda" else torch.float32
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id, 
            torch_dtype=dtype,
            use_safetensors=True
        )
        pipe = pipe.to(device)
        logging.info("模型加载成功!")
    except Exception as e:
        logging.error(f"模型加载失败: {e}")
        pipe = None # 确保如果加载失败，pipe为None

# --- API 请求体定义 ---
class ImageRequest(BaseModel):
    prompt: str
    negative_prompt: str = ""
    width: int = 512
    height: int = 512
    num_inference_steps: int = 25
    guidance_scale: float = 7.5

# --- API 端点 ---
@app.get("/")
def read_root():
    return {"status": "DreamForge后端服务正在运行"}

@app.post("/api/generate")
async def generate_image(req: ImageRequest):
    if pipe is None:
        return Response(content='{"error": "模型未加载，服务不可用"}', status_code=503, media_type="application/json")

    logging.info(f"收到生成请求: prompt='{req.prompt}'")
    
    try:
        # 使用 autocast 以获得更好的性能
        with autocast(device):
            image = pipe(
                prompt=req.prompt,
                negative_prompt=req.negative_prompt,
                width=req.width,
                height=req.height,
                num_inference_steps=req.num_inference_steps,
                guidance_scale=req.guidance_scale
            ).images[0]

        # 将图片转换为base64编码以便在JSON中传输
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        logging.info("图片生成成功")
        return {"image_base64": img_str}

    except Exception as e:
        logging.error(f"图片生成时发生错误: {e}")
        return Response(content=f'{{"error": "图片生成失败: {e}"}}', status_code=500, media_type="application/json")

