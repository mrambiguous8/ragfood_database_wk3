# 🚀 Quick Reference Card - RAG Food Database

## Choose Your Version

### 🏆 Full Cloud (Best Performance)
```bash
cd Cloud_Version
python rag_run_groq.py
```
- ⚡ **Speed**: 0.5-1.5s per query
- 💰 **Cost**: $0.04-$4/month
- 🎯 **Dependencies**: None
- 📦 **Stack**: Upstash + Groq

### 💪 Hybrid Cloud (Free Forever)
```bash
cd Cloud_Version
python rag_run_upstash.py
```
- ⚡ **Speed**: 5-15s per query
- 💰 **Cost**: $0/month
- 🎯 **Dependencies**: Ollama
- 📦 **Stack**: Upstash + Ollama

### 🏠 Original Local (100% Private)
```bash
python rag_run.py
```
- ⚡ **Speed**: 5-15s per query
- 💰 **Cost**: $0/month
- 🎯 **Dependencies**: ChromaDB + Ollama
- 📦 **Stack**: ChromaDB + Ollama

---

## Environment Setup (.env)

### Full Cloud
```env
UPSTASH_VECTOR_REST_URL=https://your-index.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your_token
GROQ_API_KEY=gsk_your_key
```

### Hybrid Cloud
```env
UPSTASH_VECTOR_REST_URL=https://your-index.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your_token
```

### Local
```env
# No .env needed
```

---

## Commands

### In Application
- **health** - System status check
- **stream** - Toggle streaming mode
- **stats** - Usage statistics
- **exit** - Quit

### Testing
```bash
# Automated test (Full Cloud only)
python Cloud_Version/test_groq.py

# Expected: 3 tests pass in ~3 seconds, cost ~$0.0002
```

---

## API Keys

### Upstash Vector (All Cloud Versions)
1. Go to https://console.upstash.com
2. Create Vector Index
3. Select: `mixedbread-ai/mxbai-embed-large-v1`
4. Copy REST URL and Token
5. Free tier: 10,000 queries/day

### Groq API (Full Cloud Only)
1. Go to https://console.groq.com
2. Create API Key
3. Copy key (starts with `gsk_`)
4. Free tier: 30 req/min, 6,000 req/day

---

## Performance at a Glance

| Metric | Local | Hybrid | Full Cloud |
|--------|-------|--------|------------|
| **Response Time** | 5-15s | 5-15s | **0.5-1.5s** ⚡ |
| **Setup Time** | 30 min | 10 min | **2 min** |
| **Monthly Cost** | $0 | $0 | **$0.04-$4** |
| **Scalability** | 1 user | 1 user | **Unlimited** |
| **Dependencies** | 2 local | 1 local | **None** |

---

## Cost Calculator (Full Cloud)

### Per Query
- **~1000 tokens** = **$0.000068**
- **14,706 queries per $1**

### Monthly
| Daily Queries | Monthly Cost |
|---------------|--------------|
| 10 | $0.04 |
| 50 | $0.20 |
| 100 | $0.40 |
| 500 | $2.04 |
| 1000 | $4.08 |

---

## Example Queries

```
✅ Tell me about Filipino food
✅ What are healthy breakfast options?
✅ Suggest vegetarian dishes from India
✅ What Thai dishes use coconut?
✅ Recommend high-protein meals
✅ What's the cultural significance of pho?
✅ Give me gluten-free options
✅ What are popular Chinese dumplings?
```

---

## Troubleshooting

### "Invalid API key"
- Check `.env` format (no quotes)
- Regenerate at console

### "Rate limit exceeded"
- Wait 60 seconds
- Free tier: 30 req/min

### "Connection refused"
- For Ollama: Run `ollama serve`
- Check port 11434

### Slow responses
- Check internet
- Try `stream` mode

---

## Quick Test

```bash
cd Cloud_Version
python test_groq.py
```

**Expected:**
```
Test 1/3: Tell me about Filipino food
   - Total time: 1.25s ✅
   - Cost: $0.000091 ✅

Test 2/3: What are healthy breakfast options?
   - Total time: 0.71s ✅
   - Cost: $0.000060 ✅

Test 3/3: Suggest vegetarian dishes from India
   - Total time: 0.76s ✅
   - Cost: $0.000054 ✅

📊 SUMMARY: $0.000205 total
✅ All tests passed!
```

---

## File Locations

```
ragfood_database_wk3/
├── README.md                    # Main documentation
├── MIGRATION_GUIDE.md           # Detailed architecture guide
├── IMPLEMENTATION_SUMMARY.md    # Complete implementation report
│
├── rag_run.py                   # Original local version
│
└── Cloud_Version/
    ├── rag_run_groq.py         # Full Cloud ⭐
    ├── rag_run_upstash.py      # Hybrid Cloud
    ├── test_groq.py            # Automated tests
    └── requirements.txt         # Dependencies
```

---

## Decision Matrix

**Choose Full Cloud if:**
- ✅ You want 10x faster responses
- ✅ You're okay with $0.04-$4/month
- ✅ You want zero local setup
- ✅ You need production deployment

**Choose Hybrid if:**
- ✅ You want $0/month forever
- ✅ You prefer local LLM control
- ✅ You're okay with slower speed
- ✅ You already have Ollama

**Choose Local if:**
- ✅ You want 100% privacy
- ✅ No internet dependency
- ✅ You're experimenting/learning
- ✅ You have time for setup

---

## Documentation Links

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Project overview |
| [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) | Architecture comparison & setup |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | Implementation report |
| [upstash-migration-prd.md](upstash-migration-prd.md) | Phase 1 design doc |
| [cloud-hosted-groq-migration-prd.md](cloud-hosted-groq-migration-prd.md) | Phase 2 design doc |

---

## One-Line Summary

**Full Cloud**: ⚡ 10x faster, 💰 $0.04-$4/mo, 🎯 zero dependencies, 🚀 production-ready

---

**Last Updated**: December 9, 2024  
**Recommendation**: Use Full Cloud (rag_run_groq.py) for best experience
