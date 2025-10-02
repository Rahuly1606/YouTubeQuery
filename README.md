<div align="center"><div align="center"><div align="center">



# 🎬 QueryTube



### AI-Powered YouTube Semantic Search Engine# 🎬 QueryTube# 🎬 QueryTube



<p align="center">

  <strong>Search YouTube videos using natural language. Find exactly what you're looking for in seconds.</strong>

</p>### AI-Powered YouTube Semantic Search Engine### AI-Powered YouTube Semantic Search Engine



<p align="center">

  <a href="#-features">Features</a> •

  <a href="#-quick-start">Quick Start</a> •<p align="center"><p align="center">

  <a href="#-tech-stack">Tech Stack</a> •

  <a href="#-api-reference">API</a> •  <strong>Search YouTube videos using natural language. Find exactly what you're looking for in seconds.</strong>  <strong>Search YouTube videos using natural language. Find exactly what you're looking for in seconds.</strong>

  <a href="#-deployment">Deploy</a>

</p></p></p>



![Next.js](https://img.shields.io/badge/Next.js-14-black?style=flat-square&logo=next.js)

![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=flat-square&logo=fastapi)

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)<p align="center"><p align="center">

![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=flat-square&logo=typescript)

![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)  <a href="#-features">Features</a> •  <a href="#-features">Features</a> •



</div>  <a href="#-quick-start">Quick Start</a> •  <a href="#-quick-start">Quick Start</a> •



---  <a href="#-tech-stack">Tech Stack</a> •  <a href="#-demo">Demo</a> •



## ✨ Features  <a href="#-api-reference">API</a> •  <a href="#-api-docs">API</a> •



🔍 **Semantic Search** - AI-powered natural language queries using Sentence Transformers    <a href="#-deployment">Deploy</a>  <a href="#-deployment">Deploy</a>

🎯 **Transcript Analysis** - Search actual video content, not just titles or descriptions  

⚡ **Lightning Fast** - FAISS vector index delivers instant results  </p></p>

🎨 **Modern UI** - Beautiful Next.js frontend with Tailwind CSS and smooth animations  

📊 **Rich Results** - View counts, timestamps, relevance scores, and video previews  

🔧 **Easy Setup** - Automated scripts for data collection and indexing  

🐳 **Docker Ready** - Complete containerization with docker-compose  ![Next.js](https://img.shields.io/badge/Next.js-14-black?style=flat-square&logo=next.js)![Next.js](https://img.shields.io/badge/Next.js-14-black?style=flat-square&logo=next.js)

📱 **Responsive** - Works perfectly on desktop, tablet, and mobile

![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=flat-square&logo=fastapi)![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=flat-square&logo=fastapi)

---

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)

## 🚀 Quick Start

![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=flat-square&logo=typescript)![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=flat-square&logo=typescript)

### Prerequisites

![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

- **Python 3.8+** and **Node.js 16+**

- **YouTube Data API Key** - [Get one free here](https://console.cloud.google.com/apis/credentials)



### ⚡ Installation (5 Minutes)</div></div>



```bash

# 1️⃣ Clone the repository

git clone https://github.com/Rahuly1606/YouTubeQuery.git------

cd YouTubeQuery



# 2️⃣ Backend Setup

cd backend## ✨ Features## ✨ Features

python -m venv venv

source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

🔍 **Semantic Search** - AI-powered natural language queries using Sentence Transformers  🔍 **Semantic Search** - AI-powered natural language queries  

# 3️⃣ Set YouTube API Key

export YOUTUBE_API_KEY="your_api_key"  # Windows: $env:YOUTUBE_API_KEY="your_api_key"🎯 **Transcript Analysis** - Search actual video content, not just titles or descriptions  🎯 **Transcript Analysis** - Search actual video content, not just titles  



# 4️⃣ Collect Videos (Example: Python tutorials)⚡ **Lightning Fast** - FAISS vector index delivers instant results  ⚡ **Lightning Fast** - FAISS vector index for instant results  

python scripts/collect_youtube.py --channel-id UCCezIgC97PvUuR4_gbFUs5g --max-results 30

🎨 **Modern UI** - Beautiful Next.js frontend with Tailwind CSS and smooth animations  🎨 **Modern UI** - Beautiful Next.js frontend with smooth animations  

# 5️⃣ Fetch Transcripts

python scripts/get_transcripts.py --delay 2.5📊 **Rich Results** - View counts, timestamps, relevance scores, and video previews  📊 **Rich Results** - View counts, timestamps, and relevance scores  



# 6️⃣ Generate AI Search Index🔧 **Easy Setup** - Automated scripts for data collection and indexing  🔧 **Easy Setup** - Automated scripts for data collection  

python scripts/embed_and_index.py

🐳 **Docker Ready** - Complete containerization with docker-compose  🐳 **Docker Ready** - Complete containerization included## 📋 Prerequisites

# 7️⃣ Start Backend

uvicorn app.main:app --reload📱 **Responsive** - Works perfectly on desktop, tablet, and mobile



# 8️⃣ Start Frontend (new terminal)

cd ../frontend

npm install---

npm run dev

```---### Required API Keys & Accounts



**🎉 Open http://localhost:3000 and start searching!**## 🚀 Quick Start



---



## 🐳 Docker Setup (Recommended)### Prerequisites



```bash## ✨ Features1. **Google Cloud / YouTube Data API v3**

# One command to start everything

docker-compose up --build- **Python 3.8+** and **Node.js 16+**



# ✅ Frontend: http://localhost:3000- **YouTube Data API Key** - [Get one free here](https://console.cloud.google.com/apis/credentials)   - Go to [Google Cloud Console](https://console.cloud.google.com/)

# ✅ Backend API: http://localhost:8000

# ✅ API Docs: http://localhost:8000/docs

```

### ⚡ Installation (5 Minutes)- 🔍 **Semantic Search** - Natural language queries using AI embeddings   - Create a new project or select existing

---



## 💻 Tech Stack

```bash- 🎯 **Transcript-Based** - Search actual video content, not just titles   - Enable "YouTube Data API v3"

### Frontend

- **Next.js 14** - React framework with App Router# 1️⃣ Clone the repository

- **TypeScript** - Type safety and better DX

- **Tailwind CSS** - Utility-first stylinggit clone https://github.com/Rahuly1606/YouTubeQuery.git- ⚡ **Fast** - FAISS vector index for instant results   - Create API Key (Credentials → Create Credentials → API Key)

- **Framer Motion** - Smooth animations

- **Heroicons** - Beautiful icon librarycd YouTubeQuery



### Backend- 🎨 **Modern UI** - Clean Next.js frontend with real-time search   - Copy the key for `YOUTUBE_API_KEY` in `.env`

- **FastAPI** - Modern Python web framework

- **Sentence-Transformers** - AI embeddings (all-MiniLM-L6-v2)# 2️⃣ Backend Setup

- **FAISS** - Facebook's vector similarity search

- **Pydantic** - Data validationcd backend- 🔧 **Easy Setup** - Automated scripts for data collection

- **Uvicorn** - Lightning-fast ASGI server

python -m venv venv

### Data Pipeline

- **YouTube Data API v3** - Video metadatasource venv/bin/activate  # Windows: venv\Scripts\activate- 📊 **Real-time Analytics** - View counts, timestamps, and relevance scores2. **HuggingFace Token** (Optional - only for private models)

- **yt-dlp** - Reliable transcript extraction

- **pandas** - Data processingpip install -r requirements.txt

- **numpy** - Numerical operations

   - Go to [HuggingFace Settings](https://huggingface.co/settings/tokens)

---

# 3️⃣ Set YouTube API Key

## 📊 Recommended YouTube Channels

export YOUTUBE_API_KEY="your_api_key"  # Windows: $env:YOUTUBE_API_KEY="your_api_key"---   - Create a read token

Channels with high transcript availability for better results:



| Channel | ID | Topic | Success Rate |

|---------|-----|-------|--------------|# 4️⃣ Collect Videos (Example: Python tutorials from Corey Schafer)   - Add to `HF_TOKEN` in `.env`

| Corey Schafer | `UCCezIgC97PvUuR4_gbFUs5g` | Python | 90%+ |

| Fireship | `UCsBjURrPoezykLs9EqgamOA` | Tech | 85%+ |python scripts/collect_youtube.py --channel-id UCCezIgC97PvUuR4_gbFUs5g --max-results 30

| TED-Ed | `UCsooa4yRKGN_zEE8iknghZA` | Education | 95%+ |

| Khan Academy | `UCvjgXvBlbQiydffTU1ulV5w` | Math/Science | 90%+ |## 🚀 Quick Start

| freeCodeCamp | `UC8butISFwT-Wl7EV0hUK0BQ` | Programming | 80%+ |

# 5️⃣ Fetch Transcripts

### Collect Videos

python scripts/get_transcripts.py --delay 2.53. **Pinecone** (Optional - for production vector store)

```bash

# From a channel

python scripts/collect_youtube.py --channel-id CHANNEL_ID --max-results 50

# 6️⃣ Generate AI Search Index### Prerequisites   - Sign up at [Pinecone](https://www.pinecone.io/)

# From a playlist

python scripts/collect_youtube.py --playlist-id PLAYLIST_ID --max-results 100python scripts/embed_and_index.py

```

   - Get API key and environment

---

# 7️⃣ Start Backend (Terminal 1)

## 🔍 API Reference

uvicorn app.main:app --reload- Python 3.8+   - Add to `.env` if using Pinecone instead of FAISS

### Search Endpoint



```http

POST /api/search# 8️⃣ Start Frontend (Terminal 2 - new terminal)- Node.js 16+

Content-Type: application/json

cd ../frontend

{

  "query": "machine learning tutorial",npm install- YouTube Data API v3 Key ([Get one here](https://console.cloud.google.com/))## 🛠️ Tech Stack

  "top_k": 10,

  "metric": "cosine"npm run dev

}

``````



**Response:**

```json

{**🎉 Open http://localhost:3000 and start searching!**### Setup in 5 Minutes### Frontend

  "query": "machine learning tutorial",

  "results": [

    {

      "video_id": "abc123",---- **Next.js 14** (TypeScript, App Router)

      "title": "Complete Machine Learning Course",

      "channel": "Tech Channel",

      "score": 0.89,

      "snippet": "...relevant transcript...",## 🐳 Docker Setup (Recommended)```bash- **Tailwind CSS** - Styling

      "thumbnail_url": "https://...",

      "view_count": 125000,

      "duration": "PT15M30S"

    }```bash# 1. Backend Setup- **Framer Motion** - Animations

  ],

  "total": 10,# One command to start everything

  "took_ms": 45.2

}docker-compose up --buildcd backend- **Headless UI** - Accessible components

```



### Available Endpoints

# ✅ Frontend: http://localhost:3000python -m venv venv- **React Query** - Data fetching & caching

```bash

GET  /api/video/{video_id}      # Get video details# ✅ Backend API: http://localhost:8000

GET  /api/health                # Health check

POST /api/ingest/collect        # Collect videos# ✅ API Docs: http://localhost:8000/docs.\venv\Scripts\Activate.ps1  # Windows

POST /api/ingest/transcripts    # Fetch transcripts

POST /api/index/embed           # Build search index```

```

# source venv/bin/activate    # Mac/Linux### Backend

**📖 Interactive API Docs:** http://localhost:8000/docs

---

---

pip install -r requirements.txt- **FastAPI** - Python web framework

## 🔧 Configuration

## 💻 Tech Stack

### Environment Variables

- **Sentence-Transformers** - Embedding generation (all-MiniLM-L6-v2)

Create a `.env` file in the root:

### Frontend

```env

# Required- **Next.js 14** - React framework with App Router# 2. Set API Key- **FAISS** - Vector similarity search

YOUTUBE_API_KEY=your_youtube_api_key_here

- **TypeScript** - Type safety

# Optional

VECTOR_STORE=faiss- **Tailwind CSS** - Utility-first styling$env:YOUTUBE_API_KEY = "your_youtube_api_key_here"- **Pydantic** - Data validation

DATABASE_URL=sqlite:///./querytube.db

BACKEND_PORT=8000- **Framer Motion** - Smooth animations

NEXT_PUBLIC_API_URL=http://localhost:8000

```- **Heroicons** - Beautiful icons- **Uvicorn** - ASGI server



### Custom Embedding Models



```bash### Backend# 3. Collect Videos (choose a channel with good transcripts)

# Default (fast, 384 dimensions)

python scripts/embed_and_index.py --model all-MiniLM-L6-v2- **FastAPI** - Modern Python web framework



# Better quality (slower, 768 dimensions)- **Sentence-Transformers** - AI embeddings (all-MiniLM-L6-v2)python scripts/collect_youtube.py --channel-id UCCezIgC97PvUuR4_gbFUs5g --max-results 30### Data Pipeline

python scripts/embed_and_index.py --model all-mpnet-base-v2

- **FAISS** - Facebook's vector similarity search

# Multilingual support

python scripts/embed_and_index.py --model paraphrase-multilingual-MiniLM-L12-v2- **Pydantic** - Data validation- **google-api-python-client** - YouTube API

```

- **Uvicorn** - Lightning-fast ASGI server

---

# 4. Fetch Transcripts- **youtube-transcript-api** - Transcript extraction

## 🐛 Troubleshooting

### Data & AI

### "429 Too Many Requests"

YouTube is rate limiting. Use slower delays:- **YouTube Data API v3** - Video metadatapython scripts/get_transcripts.py --delay 2.5 --max-retries 5- **pandas** - Data processing

```bash

python scripts/get_transcripts.py --delay 5.0 --max-retries 3- **youtube-transcript-api** / **yt-dlp** - Transcript extraction

```

- **pandas** - Data processing- **SQLite/PostgreSQL** - Metadata storage

### "No transcripts found"

Not all videos have transcripts. Expected success rate: 30-90% depending on channel. Try educational channels for best results.- **numpy** - Numerical operations



### "YOUTUBE_API_KEY not set"# 5. Generate Search Index

Set the environment variable:

```bash---

# Windows PowerShell

$env:YOUTUBE_API_KEY = "your_key"python scripts/embed_and_index.py## 📁 Project Structure



# Mac/Linux## 📊 Data Collection

export YOUTUBE_API_KEY="your_key"

```



### Frontend Can't Connect### Recommended YouTube Channels (High Transcript Availability)

1. Check backend is running: http://localhost:8000/health

2. Verify `.env` has: `NEXT_PUBLIC_API_URL=http://localhost:8000`# 6. Start Backend```

3. Clear browser cache and restart dev server

| Channel | ID | Topic | Success Rate |

---

|---------|-----|-------|--------------|uvicorn app.main:app --reloadYoutube-Query/

## 🚢 Deployment

| Corey Schafer | `UCCezIgC97PvUuR4_gbFUs5g` | Python | 90%+ |

### Vercel (Frontend)

| Fireship | `UCsBjURrPoezykLs9EqgamOA` | Tech | 85%+ |├── backend/

```bash

cd frontend| TED-Ed | `UCsooa4yRKGN_zEE8iknghZA` | Education | 95%+ |

npm i -g vercel

vercel --prod| Khan Academy | `UCvjgXvBlbQiydffTU1ulV5w` | Math/Science | 90%+ |# 7. In NEW terminal - Start Frontend│   ├── app/



# Set in Vercel dashboard:| freeCodeCamp | `UC8butISFwT-Wl7EV0hUK0BQ` | Programming | 80%+ |

# NEXT_PUBLIC_API_URL=https://your-backend.railway.app

```cd frontend│   │   ├── main.py              # FastAPI application



### Railway (Backend)### Collect from Channel



```bashnpm install│   │   ├── api/                 # API endpoints

cd backend

npm i -g @railway/cli```bash

railway login

railway initpython scripts/collect_youtube.py --channel-id CHANNEL_ID --max-results 50npm run dev│   │   │   ├── search.py

railway up

```

# Add in Railway dashboard:

# YOUTUBE_API_KEY=your_key│   │   │   ├── ingest.py

```

### Collect from Playlist

### Docker Hub

# 8. Open http://localhost:3000 🎉│   │   │   └── video.py

```bash

# Build and push```bash

docker build -t your-username/querytube-backend ./backend

docker build -t your-username/querytube-frontend ./frontendpython scripts/collect_youtube.py --playlist-id PLAYLIST_ID --max-results 100```│   │   ├── models/              # Pydantic models

docker push your-username/querytube-backend

docker push your-username/querytube-frontend```

```

│   │   ├── services/            # Business logic

---

---

## 📈 Performance Tips

---│   │   │   ├── vector_search.py

1. **Start Small** - Test with 20-30 videos first

2. **Choose Wisely** - Educational channels = better transcripts## 🔍 API Reference

3. **Rate Limiting** - Use `--delay 2.5` minimum

4. **Batch Processing** - Collect in batches with breaks│   │   │   └── youtube_service.py

5. **Monitor Logs** - Check errors in console output

### Search Endpoint

---

## 📦 Installation│   │   └── config.py            # Configuration

## 🎯 Search Query Examples

```http

Try these queries to test your setup:

POST /api/search│   ├── Dockerfile

- "explain async await in python"

- "what is machine learning"Content-Type: application/json

- "how to center a div in CSS"

- "best practices for API design"### Backend│   ├── requirements.txt

- "introduction to neural networks"

- "debugging tips and tricks"{

- "python decorators tutorial"

- "react hooks explained"  "query": "machine learning tutorial",│   └── tests/



---  "top_k": 10,



## 🤝 Contributing  "metric": "cosine"```bash├── frontend/



Contributions are welcome! Here's how:}



1. Fork the repository```cd backend│   ├── src/

2. Create feature branch: `git checkout -b feature/AmazingFeature`

3. Commit changes: `git commit -m 'Add AmazingFeature'`

4. Push to branch: `git push origin feature/AmazingFeature`

5. Open a Pull Request**Response:**python -m venv venv│   │   ├── app/                 # Next.js pages



---```json



## 📄 License{│   │   ├── components/          # React components



MIT License - see [LICENSE](LICENSE) file for details.  "query": "machine learning tutorial",



---  "results": [# Activate virtual environment│   │   │   ├── SearchBar.tsx



## 🙏 Acknowledgments    {



- [Sentence-Transformers](https://www.sbert.net/) - State-of-the-art embeddings      "video_id": "abc123",.\venv\Scripts\Activate.ps1    # Windows PowerShell│   │   │   ├── ResultCard.tsx

- [FAISS](https://github.com/facebookresearch/faiss) - Efficient similarity search

- [YouTube Data API](https://developers.google.com/youtube/v3) - Video metadata      "title": "Complete Machine Learning Course",

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python framework

- [Next.js](https://nextjs.org/) - React framework for production      "channel": "Tech Channel",# source venv/bin/activate      # Mac/Linux│   │   │   ├── VideoPlayer.tsx



---      "score": 0.89,



## 📞 Support      "snippet": "...relevant transcript snippet...",│   │   │   └── ThemeToggle.tsx



- **Issues:** [GitHub Issues](https://github.com/Rahuly1606/YouTubeQuery/issues)      "thumbnail_url": "https://...",

- **Discussions:** [GitHub Discussions](https://github.com/Rahuly1606/YouTubeQuery/discussions)

- **Email:** support@querytube.com      "view_count": 125000,pip install -r requirements.txt│   │   └── lib/                 # Utilities



---      "duration": "PT15M30S"



<div align="center">    }```│   ├── public/



**Built with ❤️ using Python, TypeScript, and AI**  ],



⭐ **Star this repo if you find it helpful!** ⭐  "total": 10,│   ├── Dockerfile



[Report Bug](https://github.com/Rahuly1606/YouTubeQuery/issues) ·   "took_ms": 45.2

[Request Feature](https://github.com/Rahuly1606/YouTubeQuery/issues) · 

[View Demo](https://querytube-demo.vercel.app)}**Key Dependencies:**│   └── package.json



</div>```


- `fastapi` - Web framework├── scripts/

### Other Endpoints

- `sentence-transformers` - AI embeddings│   ├── collect_youtube.py       # YouTube data collection

```bash

GET  /api/video/{video_id}      # Get video details- `faiss-cpu` - Vector search│   ├── get_transcripts.py       # Transcript extraction

GET  /api/health                # Health check

POST /api/ingest/collect        # Collect videos- `youtube-transcript-api` - Transcript fetching│   ├── embed_and_index.py       # Embedding & indexing

POST /api/ingest/transcripts    # Fetch transcripts

POST /api/index/embed           # Build search index- `google-api-python-client` - YouTube API│   └── run_full_pipeline.sh     # Complete pipeline

```

- `pandas` - Data handling├── notebooks/

**📖 Full API Documentation:** http://localhost:8000/docs (Swagger UI)

│   └── eda.ipynb                # Exploratory data analysis

---

### Frontend├── data/                        # Generated data files

## 🔧 Configuration

│   ├── videos.parquet

### Environment Variables

```bash│   ├── transcripts.parquet

Create a `.env` file:

cd frontend│   ├── embeddings.parquet

```env

# Requirednpm install│   └── index.faiss

YOUTUBE_API_KEY=your_youtube_api_key_here

```├── docker-compose.yml

# Optional

HF_TOKEN=your_huggingface_token├── .env.example

VECTOR_STORE=faiss

DATABASE_URL=sqlite:///./querytube.db**Key Dependencies:**└── README.md



# Backend- `next` - React framework```

BACKEND_PORT=8000

BACKEND_HOST=0.0.0.0- `typescript` - Type safety



# Frontend- `tailwindcss` - Styling## 🚀 Quick Start

NEXT_PUBLIC_API_URL=http://localhost:8000

```



### Change Embedding Model---### 1. Clone and Setup



```bash

# Default (fast, 384 dimensions)

python scripts/embed_and_index.py --model all-MiniLM-L6-v2## ⚙️ Configuration```bash



# Better quality (slower, 768 dimensions)# Clone repository

python scripts/embed_and_index.py --model all-mpnet-base-v2

### Get YouTube API Keycd Youtube-Query

# Multilingual

python scripts/embed_and_index.py --model paraphrase-multilingual-MiniLM-L12-v2

```

1. Go to [Google Cloud Console](https://console.cloud.google.com/)# Copy environment template

---

2. Create a new projectcp .env.example .env

## 🐛 Troubleshooting

3. Enable **YouTube Data API v3**

### "429 Too Many Requests"

4. Create credentials → API Key# Edit .env and add your YOUTUBE_API_KEY

YouTube is rate limiting. Use slower delays:

5. Copy the key```

```bash

python scripts/get_transcripts.py --delay 5.0 --max-retries 3

```

### Set Environment Variable### 2. Environment Variables

### "No transcripts found"



Not all videos have transcripts. Try educational channels (TED, Khan Academy). Expected success rate: 30-90% depending on channel.

```bashCreate a `.env` file in the root directory:

### "YOUTUBE_API_KEY not set"

# Windows PowerShell

Set the environment variable:

$env:YOUTUBE_API_KEY = "your_api_key_here"```env

```bash

# Windows PowerShell# Required

$env:YOUTUBE_API_KEY = "your_key_here"

# Mac/LinuxYOUTUBE_API_KEY=your_youtube_api_key_here

# Mac/Linux

export YOUTUBE_API_KEY="your_key_here"export YOUTUBE_API_KEY="your_api_key_here"

```

# Optional

### Frontend Can't Connect to Backend

# Or create .env file in backend/HF_TOKEN=your_huggingface_token

1. Check backend is running: `http://localhost:8000/health`

2. Verify API URL in frontend `.env`: `NEXT_PUBLIC_API_URL=http://localhost:8000`echo "YOUTUBE_API_KEY=your_api_key_here" > backend/.envVECTOR_STORE=faiss

3. Check browser console for CORS errors

```DATABASE_URL=sqlite:///./querytube.db

---



## 🚢 Deployment

---# For Pinecone (optional)

### Deploy Frontend to Vercel

PINECONE_API_KEY=your_pinecone_key

```bash

cd frontend## 🎯 UsagePINECONE_ENVIRONMENT=us-west1-gcp

npm i -g vercel

vercel --prod



# Set environment variable in Vercel dashboard:### 1. Collect Videos# Backend

# NEXT_PUBLIC_API_URL=https://your-backend.railway.app

```BACKEND_PORT=8000



### Deploy Backend to Railway#### From a YouTube ChannelBACKEND_HOST=0.0.0.0



```bash

cd backend

npm i -g @railway/cli```bash# Frontend

railway login

railway initpython scripts/collect_youtube.py --channel-id CHANNEL_ID --max-results 30NEXT_PUBLIC_API_URL=http://localhost:8000

railway up

``````

# Add environment variables in Railway dashboard:

# YOUTUBE_API_KEY=your_key

```

**Recommended Channels (Good Transcript Availability):**### 3. Docker Setup (Recommended)

### Deploy with Docker



```bash

# Build images| Channel | ID | Topic |```bash

docker build -t querytube-backend:latest ./backend

docker build -t querytube-frontend:latest ./frontend|---------|-----|-------|# Build and start all services



# Push to Docker Hub| Corey Schafer | `UCCezIgC97PvUuR4_gbFUs5g` | Python |docker-compose up --build

docker tag querytube-backend your-username/querytube-backend

docker push your-username/querytube-backend| Fireship | `UCsBjURrPoezykLs9EqgamOA` | Tech |

```

| TED-Ed | `UCsooa4yRKGN_zEE8iknghZA` | Education |# Frontend: http://localhost:3000

---

| Khan Academy | `UCvjgXvBlbQiydffTU1ulV5w` | Math/Science |# Backend API: http://localhost:8000

## 📈 Performance Tips

| Traversy Media | `UC29ju8bIPH5as8OGnQzwJyA` | Web Dev |# API Docs: http://localhost:8000/docs

1. **Start Small** - Begin with 20-30 videos for testing

2. **Choose Wisely** - Educational channels have better transcript availability| freeCodeCamp | `UC8butISFwT-Wl7EV0hUK0BQ` | Programming |```

3. **Rate Limiting** - Use `--delay 2.5` minimum to avoid API blocks

4. **Batch Processing** - Collect in batches with breaks to stay under quota

5. **Monitor Logs** - Check `data/transcript_errors.log` for failures

#### From a Playlist### 4. Manual Setup

---



## 🎯 Usage Examples

```bash#### Backend

### Search Queries to Try

python scripts/collect_youtube.py --playlist-id PLAYLIST_ID --max-results 50

- "explain async await in python"

- "what is machine learning"``````bash

- "how to center a div in CSS"

- "best practices for API design"cd backend

- "introduction to neural networks"

- "debugging tips and tricks"**Finding IDs:**



---- **Channel ID:** YouTube channel → About → Share → Channel ID# Create virtual environment



## 🤝 Contributing- **Playlist ID:** Playlist URL → `list=PLAYLIST_ID`python -m venv venv



Contributions are welcome! Please feel free to submit a Pull Request.source venv/bin/activate  # Windows: venv\Scripts\activate



1. Fork the repository### 2. Fetch Transcripts

2. Create your feature branch (`git checkout -b feature/AmazingFeature`)

3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)# Install dependencies

4. Push to the branch (`git push origin feature/AmazingFeature`)

5. Open a Pull Request```bashpip install -r requirements.txt



---# Standard (recommended)



## 📄 Licensepython scripts/get_transcripts.py --delay 2.5 --max-retries 5# Run server



This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.uvicorn app.main:app --reload --port 8000



---# Conservative (for large batches)```



## 🙏 Acknowledgmentspython scripts/get_transcripts.py --delay 3.5 --max-retries 5



- [Sentence-Transformers](https://www.sbert.net/) - State-of-the-art text embeddings#### Frontend

- [FAISS](https://github.com/facebookresearch/faiss) - Efficient similarity search by Facebook AI

- [YouTube Data API](https://developers.google.com/youtube/v3) - Access to YouTube metadata# Fetch specific videos only

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework

- [Next.js](https://nextjs.org/) - The React framework for productionpython scripts/get_transcripts.py --video-ids VIDEO_ID1 VIDEO_ID2```bash



---cd frontend



## 📞 Support# Force re-fetch all



- **Issues:** [GitHub Issues](https://github.com/Rahuly1606/YouTubeQuery/issues)python scripts/get_transcripts.py --force# Install dependencies

- **Discussions:** [GitHub Discussions](https://github.com/Rahuly1606/YouTubeQuery/discussions)

```npm install

---



<div align="center">

**Important:** # Run development server

**Built with ❤️ using Python, TypeScript, and AI**

- Not all videos have transcriptsnpm run dev

⭐ Star this repo if you find it helpful!

- Expected success rate: 30-70%

</div>

- Educational channels work best# Open http://localhost:3000

- Script includes automatic rate-limit handling```



### 3. Generate Search Index### 5. Run Data Pipeline



```bash```bash

python scripts/embed_and_index.py# Make script executable (Unix/Mac)

```chmod +x scripts/run_full_pipeline.sh



This creates:# Run complete pipeline

- `data/embeddings.parquet` - Embedding vectors./scripts/run_full_pipeline.sh

- `data/index.faiss` - Search index

# Or run individual steps:

### 4. Check Statuspython scripts/collect_youtube.py --channel-id UC_x5XG1OV2P6uZZ5FSM9Ttw --max-results 100

python scripts/get_transcripts.py

```bashpython scripts/embed_and_index.py

python status.py```

```

## 📊 Data Collection

Shows:

- ✅ Videos collected### Collect YouTube Videos

- ✅ Transcripts fetched  

- ✅ Index generated```bash

- 📝 Next steps if something is missingpython scripts/collect_youtube.py \

  --channel-id UC_x5XG1OV2P6uZZ5FSM9Ttw \

### 5. Start Application  --max-results 100 \

  --output data/videos.parquet

```bash```

# Terminal 1 - Backend

cd backend### Extract Transcripts

uvicorn app.main:app --reload

```bash

# Terminal 2 - Frontendpython scripts/get_transcripts.py \

cd frontend  --input data/videos.parquet \

npm run dev  --output data/transcripts.parquet

``````



### 6. Search!### Generate Embeddings & Index



Open **http://localhost:3000** and try:```bash

- "how to use async await in python"python scripts/embed_and_index.py \

- "explain decorators"  --input data/transcripts.parquet \

- "best practices for API design"  --model all-MiniLM-L6-v2 \

- "introduction to type hints"  --output-index data/index.faiss \

  --output-embeddings data/embeddings.parquet

---```



## 📁 Project Structure## 🔍 API Endpoints



```### Search

Youtube-Query/

├── backend/```bash

│   ├── app/POST /api/search

│   │   ├── main.py              # FastAPI appContent-Type: application/json

│   │   ├── config.py            # Configuration

│   │   ├── models.py            # Data models{

│   │   ├── api/  "query": "machine learning tutorial",

│   │   │   ├── search.py        # Search endpoints  "top_k": 5,

│   │   │   ├── video.py         # Video endpoints  "metric": "cosine"

│   │   │   └── admin.py         # Admin endpoints}

│   │   └── services/```

│   │       ├── vector_search.py # Embeddings & search

│   │       └── youtube_service.py # YouTube API### Ingest Data

│   ├── scripts/

│   │   ├── collect_youtube.py   # Collect videos```bash

│   │   ├── get_transcripts.py   # Fetch transcripts# Collect videos

│   │   └── embed_and_index.py   # Generate indexPOST /api/ingest/collect

│   ├── data/{

│   │   ├── videos.parquet       # Video metadata  "channel_id": "UC_x5XG1OV2P6uZZ5FSM9Ttw",

│   │   ├── transcripts.parquet  # Transcripts  "max_results": 100

│   │   ├── embeddings.parquet   # Embedding data}

│   │   └── index.faiss          # FAISS index

│   ├── status.py                # Status checker# Fetch transcripts

│   └── requirements.txt         # DependenciesPOST /api/ingest/transcripts

├── frontend/

│   ├── src/# Build index

│   │   ├── app/POST /api/index/embed

│   │   │   ├── page.tsx         # Home page```

│   │   │   └── layout.tsx       # Layout

│   │   ├── lib/### Get Video Details

│   │   │   └── api.ts           # API utilities

│   │   └── types/```bash

│   │       └── index.ts         # TypeScript typesGET /api/video/{video_id}

│   └── package.json             # Dependencies```

└── README.md                    # This file

```### Check Status



---```bash

GET /api/status

## 🐛 Troubleshooting```



### "429 Too Many Requests"## 🎨 Frontend Features



**Problem:** YouTube rate limiting.- **Search Bar**: Autocomplete with query suggestions

- **Results Grid**: Beautiful cards with thumbnails, metadata, and scores

**Solution:**- **Video Player**: Embedded YouTube player with transcript timestamps

```bash- **Transcript Viewer**: Searchable transcript with "jump to" functionality

# Use slower rate- **Theme Toggle**: Dark/Light mode support

python scripts/get_transcripts.py --delay 5.0 --max-retries 3- **Admin Panel**: Trigger ingestion jobs and monitor status

- **Responsive Design**: Mobile-first, accessible UI

# Or wait 30-60 minutes and retry

```## 🧪 Testing



The script now includes automatic retry with exponential backoff.### Backend Tests



### "No transcripts found"```bash

cd backend

**Problem:** Videos don't have transcripts available.pytest tests/ -v

```

**Solution:**

- Use educational channels (better transcript availability)### Frontend Tests

- Try recommended channels above

- Check `data/transcript_errors.log` for details```bash

- Expected: 30-70% success ratecd frontend

npm test

### "Index not found"npm run test:e2e

```

**Problem:** Search index not generated.

## 🚢 Deployment

**Solution:**

```bash### Frontend (Vercel)

python scripts/embed_and_index.py

``````bash

cd frontend

### "YOUTUBE_API_KEY not set"

# Install Vercel CLI

**Problem:** API key not configured.npm i -g vercel



**Solution:**# Deploy

```bashvercel --prod

$env:YOUTUBE_API_KEY = "your_key_here"

# Or create .env file# Set environment variables in Vercel dashboard

```# NEXT_PUBLIC_API_URL=https://your-backend.railway.app

```

### Frontend Won't Connect

### Backend (Railway/Render)

**Problem:** Backend not running or wrong URL.

**Railway:**

**Solution:**

- Ensure backend is running: `uvicorn app.main:app --reload````bash

- Check URL: Should be `http://localhost:8000`cd backend

- Check browser console for errors

# Install Railway CLI

### Low Transcript Success Ratenpm i -g @railway/cli



**Problem:** Many videos don't have transcripts.# Login and deploy

railway login

**Solution:**railway init

- This is normal! Not all creators enable captionsrailway up

- Try educational channels (Khan Academy, TED-Ed)

- 30-70% is expected depending on channel# Add environment variables in Railway dashboard

```

### Check Logs

**Render:**

```bash

# View errors1. Connect your GitHub repository

cat data/transcript_errors.log2. Create new Web Service

3. Set build command: `pip install -r requirements.txt`

# Check data files exist4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

ls data/5. Add environment variables



# Verify data### Docker Hub (Optional)

python status.py

``````bash

# Build images

---docker build -t querytube-backend:latest ./backend

docker build -t querytube-frontend:latest ./frontend

## 📡 API Reference

# Push to Docker Hub

### Interactive Docsdocker tag querytube-backend your-username/querytube-backend

docker push your-username/querytube-backend

Once backend is running:```

- **Swagger UI:** http://127.0.0.1:8000/docs

- **ReDoc:** http://127.0.0.1:8000/redoc## 🔧 Configuration



### Main Endpoints### Switch Vector Store to Pinecone



#### Search VideosIn `.env`:



```http```env

POST /api/searchVECTOR_STORE=pinecone

Content-Type: application/jsonPINECONE_API_KEY=your_key

PINECONE_ENVIRONMENT=us-west1-gcp

{PINECONE_INDEX_NAME=querytube

  "query": "python async programming",```

  "top_k": 10

}### Change Embedding Model

```

```bash

**Response:**python scripts/embed_and_index.py \

```json  --model sentence-transformers/all-mpnet-base-v2

{```

  "results": [

    {Available models:

      "video_id": "oAkLSJNr5zY",- `all-MiniLM-L6-v2` (default, fast, 384 dims)

      "title": "Python Tutorial: AsyncIO",- `all-mpnet-base-v2` (best quality, 768 dims)

      "channel": "Corey Schafer",- `multi-qa-MiniLM-L6-cos-v1` (optimized for Q&A)

      "score": 0.87,

      "snippet": "...async and await...",## 📈 Performance & Scalability

      "thumbnail_url": "https://...",

      "view_count": 40898,- **Batch Processing**: Process videos in batches to avoid API quota limits

      "published_at": "2024-01-15T10:00:00Z"- **Caching**: Results cached with React Query

    }- **Rate Limiting**: Implemented in backend to prevent abuse

  ],- **Database Indexing**: Optimized queries with proper indexes

  "query": "python async programming",- **CDN**: Frontend assets served via Vercel Edge Network

  "total_results": 10

}## 🐛 Troubleshooting

```

### YouTube API Quota Exceeded

#### Get Video Details

```bash

```http# Check quota usage in Google Cloud Console

GET /api/video/{video_id}# Default quota: 10,000 units/day

```# Each search: 100 units, each video detail: 1 unit

```

#### Health Check

### Transcripts Not Available

```http

GET /api/healthMany YouTube videos have disabled transcripts. The pipeline logs failures in `data/transcript_errors.log`.

```

### FAISS Index Issues

---

```bash

## 🔧 Advanced Usage# Rebuild index

rm data/index.faiss

### Custom Embedding Modelspython scripts/embed_and_index.py

```

```bash

# More accurate (slower)## 🤝 Contributing

python scripts/embed_and_index.py --model all-mpnet-base-v2

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

# Multilingual

python scripts/embed_and_index.py --model paraphrase-multilingual-MiniLM-L12-v2## 📄 License



# Faster (default)MIT License - see LICENSE file for details.

python scripts/embed_and_index.py --model all-MiniLM-L6-v2

```## 🙏 Acknowledgments



### Adding More Content- [Sentence-Transformers](https://www.sbert.net/)

- [FAISS](https://github.com/facebookresearch/faiss)

```bash- [YouTube Data API](https://developers.google.com/youtube/v3)

# Append new videos- [FastAPI](https://fastapi.tiangolo.com/)

python scripts/collect_youtube.py --channel-id NEW_CHANNEL --max-results 50- [Next.js](https://nextjs.org/)

python scripts/get_transcripts.py --delay 2.5

python scripts/embed_and_index.py## 📞 Support



# Replace all dataFor issues and questions:

rm data/*.parquet data/*.faiss- GitHub Issues: [Create an issue](https://github.com/yourusername/querytube/issues)

python scripts/collect_youtube.py --channel-id CHANNEL --max-results 30- Documentation: [Wiki](https://github.com/yourusername/querytube/wiki)

python scripts/get_transcripts.py --delay 2.5

python scripts/embed_and_index.py---

```

Built with ❤️ using Python, TypeScript, and AI

### Batch Processing

For large datasets:

```bash
# Collect in batches
python scripts/collect_youtube.py --channel-id CH1 --max-results 50
# Wait 1 hour
python scripts/collect_youtube.py --channel-id CH2 --max-results 50
# Wait 1 hour
python scripts/collect_youtube.py --channel-id CH3 --max-results 50

# Fetch transcripts with conservative rate
python scripts/get_transcripts.py --delay 5.0 --max-retries 3

# Generate index
python scripts/embed_and_index.py
```

---

## 📊 Performance Tips

1. **Start Small:** Begin with 20-30 videos
2. **Choose Wisely:** Educational channels have better transcripts
3. **Rate Limiting:** Use `--delay 2.5` minimum
4. **Batch Collection:** Collect in batches with breaks
5. **Monitor:** Check `data/transcript_errors.log` regularly

---

## 🤝 Contributing

Contributions welcome! Feel free to submit Pull Requests.

---

## 📄 License

MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- **sentence-transformers** - Embedding models
- **youtube-transcript-api** - Transcript access
- **FastAPI** - Backend framework
- **Next.js** - Frontend framework
- **FAISS** - Vector search

---

**Built with ❤️ for efficient YouTube content discovery**

**Last Updated:** October 2, 2025
