# 🎨 DreamForge - 你的个人AI绘画工坊

DreamForge 是一个开源的AI图片生成平台，基于你的项目计划书创建。它让你可以轻松地在本地或服务器上部署一个功能强大的文生图工具。

![示例图片](https://placehold.co/800x400/1e293b/ffffff?text=DreamForge%20UI)

## ✨ 核心功能 (v0.1)

- **文生图 (Text-to-Image):** 输入文本描述，生成图片。
- **API 优先:** 所有功能都通过RESTful API提供。
- **Docker 一键部署:** 使用 Docker Compose，一条命令即可启动整个应用。
- **简洁前端:** 提供一个简单易用的Web界面进行操作。

## 📁 项目结构

```
dreamforge/
├── backend/
│   ├── main.py           # FastAPI 后端服务
│   └── requirements.txt  # Python 依赖
├── frontend/
│   └── index.html        # 前端界面 (HTML, CSS, JS)
└── docker-compose.yml    # Docker 编排文件
```

## 🚀 如何运行

我们强烈推荐使用 Docker 运行项目，这是最简单快捷的方式。

### 使用 Docker (推荐)

**前提:** 你已经安装了 [Docker](https://www.docker.com/get-started) 和 [Docker Compose](https://docs.docker.com/compose/install/)。

1.  **克隆或下载项目文件:** 将 `backend` 目录, `frontend` 目录, 和 `docker-compose.yml` 文件放在同一个项目根目录下。

2.  **启动服务:** 在项目根目录（包含 `docker-compose.yml` 的地方）打开终端，运行以下命令：

    ```bash
    docker-compose up --build
    ```

3.  **开始使用:**
    * 前端界面: 打开浏览器访问 `http://localhost:8080`
    * 后端API文档: 访问 `http://localhost:8000/docs`

### 本地开发 (不使用 Docker)

如果你想在本地直接运行和开发，请按以下步骤操作。

**1. 启动后端服务:**

```bash
# 进入后端目录
cd backend

# 创建并激活虚拟环境 (推荐)
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动 FastAPI 服务
uvicorn main:app --host 0.0.0.0 --port 8000
```

**2. 启动前端:**

直接用浏览器打开 `frontend/index.html` 文件即可。

## 🛠️ 技术栈

- **后端:** Python, FastAPI, Diffusers, PyTorch
- **前端:** HTML, Tailwind CSS, JavaScript
- **部署:** Docker, Docker Compose


