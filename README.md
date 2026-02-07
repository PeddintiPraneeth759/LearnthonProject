# Fake News Verification Assistant

AI-powered fact-checking application that verifies news claims using trusted sources.

## Project Structure

```
LearnthonProject/
├── frontend/          # React + Vite frontend
│   └── vercel.json    # Vercel deployment config
├── backend/           # FastAPI + LangChain backend
│   └── render.yaml    # Render deployment config
└── README.md
```

## Deployment

### Frontend (Vercel)
1. Import the repository to Vercel
2. Set root directory to `frontend`
3. Add environment variable: `VITE_API_URL` = your Render backend URL

### Backend (Render)
1. Import the repository to Render
2. Set root directory to `backend`
3. Add environment variables:
   - `GOOGLE_API_KEY`
   - `GOOGLE_CSE_ID`
   - `OPENROUTER_API_KEY`

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Tech Stack
- **Frontend**: React, Vite, Framer Motion
- **Backend**: FastAPI, LangChain, LangGraph
- **AI**: OpenRouter (GPT/Claude models)
- **Search**: Google Custom Search API
