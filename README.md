# 🍽️ RAG Food Database System

A **Retrieval-Augmented Generation (RAG)** system for querying a comprehensive food database containing 100 items across Filipino, Thai, Vietnamese, Indian, Chinese, and healthy international cuisines.

## 🎯 Three Architecture Options

This project offers **three deployment options** from fully local to fully cloud-native:

| Version | Vector DB | LLM | Speed | Cost | Dependencies |
|---------|-----------|-----|-------|------|--------------|
| **Local** | ChromaDB | Ollama | 5-15s | $0 | ChromaDB + Ollama |
| **Hybrid** | ☁️ Upstash | Ollama | 5-15s | $0 | Ollama only |
| **Full Cloud** ⭐ | ☁️ Upstash | 🚀 Groq | **0.5-1.5s** | $0.04-$4/mo | **None** |

**📖 See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for detailed comparison and setup instructions.**

---

## ⚡ Quick Start (Recommended: Full Cloud)

```bash
# 1. Clone repository
cd Cloud_Version

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up .env file
UPSTASH_VECTOR_REST_URL=your_upstash_url
UPSTASH_VECTOR_REST_TOKEN=your_upstash_token
GROQ_API_KEY=your_groq_api_key

# 4. Run automated tests
python test_groq.py

# 5. Start interactive mode
python rag_run_groq.py
```

**Expected Performance:**
- ⚡ Query time: 0.5-1.5 seconds
- 🚀 Generation: 500-800 tokens/sec
- 💰 Cost: ~$0.000068 per query
- ✅ Zero local dependencies

---

## 📊 Test Results

```
🧪 TESTING FULL CLOUD RAG SYSTEM
======================================================================
☁️  Vector DB: Upstash Vector
🚀 LLM: Groq API (llama-3.1-8b-instant)
======================================================================

Test 1/3: Tell me about Filipino food
   - Search time: 0.23s
   - Generation time: 1.01s
   - Total time: 1.25s
   - Tokens: 1,395
   - Cost: $0.000091

Test 2/3: What are healthy breakfast options?
   - Search time: 0.24s
   - Generation time: 0.47s
   - Total time: 0.71s
   - Tokens: 920
   - Cost: $0.000060

Test 3/3: Suggest vegetarian dishes from India
   - Search time: 0.24s
   - Generation time: 0.52s
   - Total time: 0.76s
   - Tokens: 838
   - Cost: $0.000054

📊 SUMMARY: 3 queries, 3,153 tokens, $0.000205 total
✅ All tests passed!
```

---

## 🏗️ Architecture

### Full Cloud Stack (Recommended)
```
User Query
    ↓
rag_run_groq.py
    ↓
┌───────────────┬─────────────────┐
│ Upstash Vector│     Groq API    │
│ (Retrieval)   │  (Generation)   │
│ • Auto-embed  │ • llama-3.1-8b  │
│ • 1024D       │ • 500-800 tok/s │
│ • Cosine sim  │ • Streaming     │
└───────────────┴─────────────────┘
```

**Benefits:**
- 🚀 **10x faster** than local Ollama
- ☁️ **Zero dependencies** (no local installs)
- 💰 **Ultra-low cost** ($0.04-$4/month)
- 📈 **Infinite scalability**
- 🛡️ **Production-ready**

---

## 📁 Project Structure

```
ragfood_database_wk3/
│
├── 📄 README.md                          # This file
├── 📄 MIGRATION_GUIDE.md                 # Architecture comparison & setup
├── 📄 IMPLEMENTATION_SUMMARY.md          # Complete implementation report
├── 📄 fooddatabase.json                  # 100 food items dataset
│
├── 📄 rag_run.py                         # Original local version
├── 📄 requirements.txt                   # Local dependencies
│
├── 📂 Cloud_Version/                     # Cloud implementations ⭐
│   ├── 📄 rag_run_upstash.py            # Hybrid: Upstash + Ollama
│   ├── 📄 rag_run_groq.py               # Full Cloud: Upstash + Groq
│   ├── 📄 test_groq.py                  # Automated test suite
│   ├── 📄 migrate_chroma_to_upstash.py  # Migration utility
│   ├── 📄 requirements.txt              # Cloud dependencies
│   ├── 📄 .env                          # API credentials
│   └── 📄 README.md                     # Cloud version docs
│
└── 📂 Documentation/
    ├── 📄 upstash-migration-prd.md      # ChromaDB → Upstash design
    └── 📄 cloud-hosted-groq-migration-prd.md  # Ollama → Groq design
```

---

## 🎮 Features

### Core Functionality
✅ **Natural Language Queries**: Ask questions in plain English  
✅ **Semantic Search**: Vector similarity for relevant results  
✅ **Context-Aware Answers**: RAG combines retrieval + generation  
✅ **100 Food Items**: Filipino, Thai, Vietnamese, Indian, Chinese, Healthy

### Production Features (Full Cloud)
✅ **Streaming Mode**: Real-time response display  
✅ **Error Handling**: Automatic retries with exponential backoff  
✅ **Usage Tracking**: Token counting and cost estimation  
✅ **Health Checks**: Verify connectivity before queries  
✅ **Rate Limiting**: Respect API limits with graceful handling  

### Interactive Commands
- `health` - Check system status
- `stream` - Toggle streaming mode
- `stats` - View usage statistics
- `exit` - Quit application

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) | **Start here!** Compare all 3 architectures, setup guides |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | Complete implementation report with test results |
| [upstash-migration-prd.md](upstash-migration-prd.md) | Phase 1: ChromaDB → Upstash Vector (916 lines) |
| [cloud-hosted-groq-migration-prd.md](cloud-hosted-groq-migration-prd.md) | Phase 2: Ollama → Groq API (900+ lines) |
| [Cloud_Version/README.md](Cloud_Version/README.md) | Detailed cloud version documentation |

---

## 💰 Cost Analysis

### Full Cloud Version
| Usage | Queries/Day | Monthly Cost |
|-------|-------------|--------------|
| Light | 10 | **$0.04** |
| Moderate | 100 | **$0.40** |
| Heavy | 1,000 | **$4.00** |

**Free Tier:**
- Upstash: 10,000 queries/day
- Groq: 6,000 queries/day (30/min)

**Cost per query: ~$0.000068**  
**Equivalent: 14,706 queries per $1**

---

## 🚀 Performance

### Response Time Comparison
| Version | Avg Response | Speed Improvement |
|---------|--------------|-------------------|
| Local (ChromaDB + Ollama) | 5-15s | Baseline |
| Hybrid (Upstash + Ollama) | 5-15s | No change |
| **Full Cloud (Upstash + Groq)** | **0.5-1.5s** | **10x faster** ⚡ |

### Generation Speed
- **Local Ollama**: 10-30 tokens/sec
- **Groq Cloud**: 500-800 tokens/sec 🚀

---

## 🛠️ Setup

### Option 1: Full Cloud (Recommended)

**Prerequisites**: None! (100% cloud)

```bash
cd Cloud_Version
pip install -r requirements.txt

# Get API keys:
# - Upstash: https://console.upstash.com
# - Groq: https://console.groq.com

# Create .env file:
UPSTASH_VECTOR_REST_URL=your_url
UPSTASH_VECTOR_REST_TOKEN=your_token
GROQ_API_KEY=your_key

# Run:
python rag_run_groq.py
```

### Option 2: Hybrid Cloud

**Prerequisites**: Ollama installed locally

```bash
cd Cloud_Version
pip install upstash-vector python-dotenv requests
ollama pull llama3.2

# .env file (only Upstash):
UPSTASH_VECTOR_REST_URL=your_url
UPSTASH_VECTOR_REST_TOKEN=your_token

# Run:
python rag_run_upstash.py
```

### Option 3: Original Local

**Prerequisites**: ChromaDB + Ollama

```bash
pip install chromadb requests
ollama pull llama3.2

# Run:
python rag_run.py
```

---

## 🧪 Testing

### Automated Tests
```bash
cd Cloud_Version
python test_groq.py
```

Tests 3 queries:
1. "Tell me about Filipino food"
2. "What are healthy breakfast options?"
3. "Suggest vegetarian dishes from India"

**Expected Results:**
- ✅ All 3 tests pass
- ⚡ Total time: ~2-4 seconds
- 💰 Total cost: ~$0.0002

### Manual Testing
```bash
cd Cloud_Version
python rag_run_groq.py

# Try these queries:
You: Tell me about Filipino food
You: What are healthy breakfast options?
You: Suggest vegetarian dishes from India
You: health
You: stats
```

---

## 🎯 Example Queries

```
✅ "Tell me about Filipino food"
✅ "What are healthy breakfast options?"
✅ "Suggest vegetarian dishes from India"
✅ "What Thai dishes can I make with coconut?"
✅ "Recommend high-protein meals"
✅ "What's the cultural significance of pho?"
✅ "Give me gluten-free options"
✅ "What are popular Chinese dumplings?"
```

---

## 🔧 Troubleshooting

### Full Cloud Issues

**"Invalid API key"**
- Check `.env` file format (no quotes, no spaces)
- Regenerate keys at console.upstash.com or console.groq.com

**"Rate limit exceeded"**
- Free tier: 30 requests/min (Groq)
- Wait 60 seconds or upgrade

**Slow responses**
- Check internet connection
- Try `stream` mode for better UX

### Hybrid/Local Issues

**"Connection refused to Ollama"**
```bash
ollama serve
ollama list  # Verify llama3.2 is downloaded
```

**"ChromaDB error"**
```bash
pip install --upgrade chromadb
# Delete chroma_db/ folder and re-run
```

---

## 📈 Roadmap

### ✅ Completed
- [x] Original local RAG system
- [x] ChromaDB → Upstash migration
- [x] Ollama → Groq migration
- [x] Automated testing
- [x] Comprehensive documentation
- [x] Production error handling
- [x] Usage tracking & cost estimation

### 🎯 Future Enhancements (Optional)
- [ ] Redis caching for common queries
- [ ] Web UI (FastAPI + Streamlit)
- [ ] Multi-language support
- [ ] Image recognition for food photos
- [ ] Recipe recommendations
- [ ] Nutritional calculations

---

## 🤝 Contributing

This is an educational project demonstrating RAG architectures. Contributions welcome!

**Areas for contribution:**
- Additional food items/cuisines
- Performance optimizations
- UI improvements
- Additional test cases
- Documentation improvements

---

## 📝 License

This project is for educational purposes.

---

## 🙏 Acknowledgments

- **Upstash Vector**: Cloud-native vector database with auto-embeddings
- **Groq**: Ultra-fast LLM inference API
- **Ollama**: Local LLM deployment made easy
- **ChromaDB**: Simple local vector database

---

## 📞 Support

**Documentation:**
- Quick Start: This README
- Architecture Guide: [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- Implementation Report: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

**Testing:**
```bash
python Cloud_Version/test_groq.py  # Automated
python Cloud_Version/rag_run_groq.py  # Interactive
```

**Need Help?**
1. Check troubleshooting section above
2. Run `health` command to diagnose
3. Review documentation links
4. Check API key configuration

---

## 🎉 Quick Win

**Want to see it in action RIGHT NOW?**

```bash
cd Cloud_Version
python test_groq.py
```

This runs 3 automated tests in ~3 seconds and shows you:
- ⚡ Lightning-fast responses (0.5-1.5s each)
- 🎯 Accurate food recommendations
- 💰 Minimal costs (~$0.0002 total)
- ✅ All systems working perfectly

**That's it! You're ready to go!** 🚀

---

**Last Updated**: December 9, 2024  
**Status**: ✅ Production Ready  
**Performance**: ⚡ 10x faster than local  
**Cost**: 💰 $0.04-$4/month
