# RAG Food Database - Cloud Migration Guide

This repository contains **three versions** of a RAG (Retrieval-Augmented Generation) system for a food database with 100 items covering Filipino, Thai, Vietnamese, Indian, Chinese, and healthy international cuisines.

---

## 🏗️ Architecture Options

### 1. **Original Version** (Local Only)
**Location**: Root directory  
**Components**:
- ChromaDB (local vector database)
- Ollama (local LLM - llama3.2)

**Pros**: Zero costs, complete privacy  
**Cons**: Requires local setup, slower performance

---

### 2. **Hybrid Cloud Version** (Cloud Vector DB + Local LLM)
**Location**: `Cloud_Version/` → Use `rag_run_upstash.py`  
**Components**:
- ☁️ Upstash Vector (cloud embeddings + storage)
- 🖥️ Ollama (local LLM - llama3.2)

**Pros**: 
- No manual embedding generation needed
- Automatic vector management
- Free tier available ($0/month)
- Still uses local LLM (no API costs)

**Cons**: Requires internet for vector search, Ollama still needs local setup

**Perfect for**: Users who want cloud vector storage but prefer local LLM control

---

### 3. **Full Cloud Version** ⭐ **RECOMMENDED**
**Location**: `Cloud_Version/` → Use `rag_run_groq.py`  
**Components**:
- ☁️ Upstash Vector (cloud embeddings + storage)
- 🚀 Groq API (ultra-fast cloud LLM - llama-3.1-8b-instant)

**Pros**: 
- **10x faster responses** (0.5-1.5s vs 5-15s)
- **Zero local dependencies** (no Ollama, no ChromaDB)
- **Ultra-low cost** ($0.04-$4/month typical usage)
- **Infinite scalability** (cloud auto-scaling)
- **500-800 tokens/sec** generation speed
- **Production-ready** error handling

**Cons**: Small API costs (~$0.000041 per query)

**Perfect for**: Production deployments, demo applications, or anyone wanting the best performance

---

## 🚀 Quick Start

### Option A: Full Cloud (Recommended)

```bash
# 1. Navigate to Cloud_Version
cd Cloud_Version

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
# Create .env file with:
UPSTASH_VECTOR_REST_URL=your_upstash_url
UPSTASH_VECTOR_REST_TOKEN=your_upstash_token
GROQ_API_KEY=your_groq_api_key

# 4. Run the system
python rag_run_groq.py

# 5. Test with automated script
python test_groq.py
```

**Getting API Keys:**
1. **Upstash Vector**: Sign up at [console.upstash.com](https://console.upstash.com)
   - Create a new Vector Index
   - Choose `mixedbread-ai/mxbai-embed-large-v1` model
   - Copy REST URL and token
   - Free tier: 10,000 queries/day

2. **Groq API**: Sign up at [console.groq.com](https://console.groq.com)
   - Create API key
   - Free tier: 30 requests/minute, 6,000 requests/day

---

### Option B: Hybrid Cloud

```bash
# 1. Navigate to Cloud_Version
cd Cloud_Version

# 2. Install dependencies (excluding groq)
pip install upstash-vector python-dotenv requests

# 3. Install and run Ollama locally
# Windows: Download from ollama.com
ollama pull llama3.2

# 4. Set up .env (only Upstash credentials)
UPSTASH_VECTOR_REST_URL=your_upstash_url
UPSTASH_VECTOR_REST_TOKEN=your_upstash_token

# 5. Run hybrid version
python rag_run_upstash.py
```

---

### Option C: Original Local Version

```bash
# 1. Install dependencies
pip install chromadb requests

# 2. Install and run Ollama
ollama pull llama3.2

# 3. Run original version
python rag_run.py
```

---

## 📊 Performance Comparison

| Metric | Local (Ollama) | Hybrid (Upstash + Ollama) | Full Cloud (Upstash + Groq) |
|--------|----------------|---------------------------|------------------------------|
| **Response Time** | 5-15 seconds | 5-15 seconds | **0.5-1.5 seconds** ⚡ |
| **Generation Speed** | 10-30 tokens/sec | 10-30 tokens/sec | **500-800 tokens/sec** 🚀 |
| **Setup Time** | 30 minutes | 10 minutes | **2 minutes** ✅ |
| **Dependencies** | ChromaDB + Ollama | Ollama only | **None** 🎯 |
| **Monthly Cost** | $0 | $0 | **$0.04-$4** 💰 |
| **Scalability** | Single user | Single user | **Unlimited** 📈 |
| **Internet Required** | No | Yes (search only) | **Yes** |
| **Privacy** | 100% local | Hybrid | Cloud-based |

---

## 💰 Cost Analysis (Full Cloud)

### Per Query Cost
- Average query: ~1000 tokens
- Cost: ~$0.000041 per query
- **2,439 queries per $0.10**

### Monthly Estimates
| Usage Level | Queries/Day | Monthly Cost |
|-------------|-------------|--------------|
| Light | 10 | **$0.04** |
| Moderate | 100 | **$0.40** |
| Heavy | 1,000 | **$4.00** |

**Free Tier Limits:**
- Upstash: 10,000 queries/day
- Groq: 30 requests/min, 6,000 requests/day

---

## 📁 File Structure

```
ragfood_database_wk3/
│
├── 📄 rag_run.py                      # Original local version
├── 📄 fooddatabase.json               # 100 food items dataset
├── 📄 requirements.txt                # Original dependencies
│
├── 📂 Cloud_Version/
│   ├── 📄 rag_run_upstash.py         # Hybrid: Upstash + Ollama
│   ├── 📄 rag_run_groq.py            # Full Cloud: Upstash + Groq ⭐
│   ├── 📄 test_groq.py               # Automated test suite
│   ├── 📄 migrate_chroma_to_upstash.py  # Migration utility
│   ├── 📄 requirements.txt           # Cloud dependencies
│   ├── 📄 .env                       # API credentials (not in git)
│   └── 📄 README.md                  # Cloud version docs
│
├── 📄 upstash-migration-prd.md       # ChromaDB → Upstash design doc
├── 📄 cloud-hosted-groq-migration-prd.md  # Ollama → Groq design doc
└── 📄 MIGRATION_GUIDE.md             # This file
```

---

## 🎯 Which Version Should I Use?

### Choose **Full Cloud** (rag_run_groq.py) if:
- ✅ You want the **fastest possible responses** (10x faster)
- ✅ You're okay with **tiny API costs** ($0.04-$4/month)
- ✅ You want **zero local setup** (no Ollama installation)
- ✅ You need **production-ready** deployment
- ✅ You want **unlimited concurrent users**

### Choose **Hybrid Cloud** (rag_run_upstash.py) if:
- ✅ You want **$0 monthly costs**
- ✅ You prefer **local LLM control**
- ✅ You're okay with **slower responses** (5-15s)
- ✅ You already have Ollama installed

### Choose **Original Local** (rag_run.py) if:
- ✅ You want **100% local/private** processing
- ✅ You have **no internet** or unreliable connection
- ✅ You're okay with **manual embedding** generation
- ✅ You want to **experiment with different embedding models**

---

## 🧪 Testing the Full Cloud Version

### Quick Test
```bash
cd Cloud_Version
python test_groq.py
```

This runs 3 automated tests:
1. "Tell me about Filipino food"
2. "What are healthy breakfast options?"
3. "Suggest vegetarian dishes from India"

**Expected Results:**
- ✅ Search time: ~0.2-0.3s
- ✅ Generation time: ~0.5-1.0s
- ✅ Total time: ~0.7-1.3s
- ✅ Cost per query: ~$0.00004-0.00009

### Interactive Mode
```bash
cd Cloud_Version
python rag_run_groq.py
```

**Available Commands:**
- `health` - Check Upstash and Groq connectivity
- `stream` - Toggle streaming mode (real-time response)
- `stats` - View token usage and costs
- `exit` - Quit the application

---

## 📚 Documentation

- **Upstash Migration**: See [upstash-migration-prd.md](upstash-migration-prd.md)
- **Groq Migration**: See [cloud-hosted-groq-migration-prd.md](cloud-hosted-groq-migration-prd.md)
- **Cloud Version README**: See [Cloud_Version/README.md](Cloud_Version/README.md)

---

## 🔧 Troubleshooting

### Full Cloud Version

**"Invalid API key"**
- Verify `.env` file has correct keys
- No extra quotes or spaces
- Regenerate keys if needed

**"Rate limit exceeded"**
- Free tier: 30 requests/min (Groq)
- Wait 60 seconds or upgrade to paid tier

**Slow responses**
- Check internet connection
- Verify not hitting rate limits
- Try streaming mode for better UX

### Hybrid Version

**"Connection refused to Ollama"**
- Ensure Ollama is running: `ollama serve`
- Check port 11434 is available
- Verify model is downloaded: `ollama list`

---

## 🎓 Learn More

### Design Documents
Both migrations are fully documented with:
- Architecture diagrams
- Implementation plans
- Code examples
- Cost analysis
- Performance benchmarks
- Migration checklists

### Key Features
- ✅ **Automatic embeddings** (Upstash)
- ✅ **Ultra-fast inference** (Groq)
- ✅ **Error handling** (retry logic, rate limiting)
- ✅ **Usage tracking** (token counting, cost estimation)
- ✅ **Streaming support** (real-time responses)
- ✅ **Health checks** (connectivity verification)

---

## 📈 Next Steps

1. **Try Full Cloud**: `cd Cloud_Version && python test_groq.py`
2. **Compare versions**: Run same query on all 3 versions
3. **Monitor costs**: Check usage after first day/week
4. **Production deploy**: Add monitoring, caching, rate limiting
5. **Optimize**: Implement caching for common queries

---

## ✅ Success Metrics

After migration to Full Cloud, you should see:
- ⚡ **10x faster** responses (0.5-1.5s vs 5-15s)
- 🚀 **500-800 tokens/sec** (vs 10-30 local)
- 💰 **< $5/month** for typical usage
- 🎯 **Zero local dependencies**
- 📈 **Unlimited scalability**

---

**Questions?** Check the design documents or test with `python test_groq.py`!

**Last Updated**: December 9, 2024
