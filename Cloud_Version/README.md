# 🍽️ RAG Food Database - Cloud Version

A **Retrieval-Augmented Generation (RAG)** system for querying a comprehensive food database with **three deployment architectures** - from fully local to fully cloud-native.

**Enhanced by Dennis Bonnici** with 100 food items covering:
- 🇵🇭 Filipino cuisine (Adobo, Sinigang, Bibingka)
- 🇹🇭 Thai cuisine (Tom Yum, Pad Thai, Green Curry)
- 🇻🇳 Vietnamese cuisine (Pho, Banh Mi, Spring Rolls)
- 🇮🇳 Indian cuisine (Biryani, Palak Paneer, Rajma)
- 🇨🇳 Chinese cuisine (Dim Sum, Hot Pot, Peking Duck)
- 🥗 Healthy international dishes with nutritional benefits

---

## 🏗️ Cloud Migration Overview

This directory contains **three versions** demonstrating the evolution from local to cloud-native architecture:

### Architecture Evolution

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 0: ORIGINAL LOCAL                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User Query → rag_run.py → ChromaDB (local) → Ollama (local)   │
│                              ↓                      ↓            │
│                         Manual Embed           10-30 tok/s      │
│                         384D vectors           5-15 seconds     │
│                                                                  │
│  ✅ Pros: $0 cost, 100% private, offline capable                │
│  ❌ Cons: Slow, manual setup, single user only                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                  PHASE 1: HYBRID CLOUD                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User Query → rag_run_upstash.py → Upstash Vector → Ollama     │
│                                          ↓              ↓        │
│                                    Auto-Embed      10-30 tok/s  │
│                                    1024D vectors   5-15 seconds │
│                                    Cloud storage   Local LLM    │
│                                                                  │
│  ✅ Pros: Auto-embeddings, $0 cost, cloud storage               │
│  ❌ Cons: Still slow, needs Ollama, single user                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              PHASE 2: FULL CLOUD ⭐ RECOMMENDED                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User Query → rag_run_groq.py → Upstash Vector → Groq API      │
│                                       ↓              ↓           │
│                                 Auto-Embed    500-800 tok/s ⚡  │
│                                 1024D vectors 0.5-1.5 seconds   │
│                                 Cloud storage Cloud LLM         │
│                                                                  │
│  ✅ Pros: 10x faster, zero dependencies, unlimited scale        │
│  ❌ Cons: Tiny API cost ($0.04-$4/month)                        │
└─────────────────────────────────────────────────────────────────┘
```

### Migration Journey
- **Phase 0 → 1**: Migrated vector storage from ChromaDB to Upstash (automatic embeddings)
- **Phase 1 → 2**: Migrated LLM inference from Ollama to Groq (10x speed boost)
- **Result**: Fully cloud-native RAG system with zero local dependencies

---

## 🎯 Choose Your Version

### Version 1: Original Local (`rag_run.py`)
**Stack**: ChromaDB + Ollama  
**Speed**: 5-15 seconds per query  
**Cost**: $0/month  
**Dependencies**: ChromaDB + Ollama  
**Best for**: Privacy-focused, offline use

### Version 2: Hybrid Cloud (`rag_run_upstash.py`)
**Stack**: Upstash Vector + Ollama  
**Speed**: 5-15 seconds per query  
**Cost**: $0/month  
**Dependencies**: Ollama only  
**Best for**: Cloud storage with local LLM control

### Version 3: Full Cloud (`rag_run_groq.py`) ⭐ **RECOMMENDED**
**Stack**: Upstash Vector + Groq API  
**Speed**: 0.5-1.5 seconds per query ⚡  
**Cost**: $0.04-$4/month  
**Dependencies**: None (100% cloud)  
**Best for**: Production, demos, best performance

---

## � Setup Instructions

### Option A: Full Cloud (Recommended) ⭐

**Prerequisites**: None! (100% cloud-based)

#### Step 1: Install Dependencies
```bash
cd Cloud_Version
pip install -r requirements.txt
```

#### Step 2: Get API Keys

**Upstash Vector** (Free Tier: 10,000 queries/day):
1. Sign up at [console.upstash.com](https://console.upstash.com)
2. Click "Create Vector Index"
3. Configure:
   - **Name**: food-rag-db (or any name)
   - **Region**: Choose closest to you
   - **Embedding Model**: `mixedbread-ai/mxbai-embed-large-v1`
   - **Dimensions**: 1024 (auto-set by model)
   - **Metric**: Cosine
4. Click "Create"
5. Copy **REST URL** and **REST TOKEN** from dashboard

**Groq API** (Free Tier: 30 req/min, 6,000 req/day):
1. Sign up at [console.groq.com](https://console.groq.com)
2. Navigate to API Keys section
3. Click "Create API Key"
4. Copy the key (starts with `gsk_`)

#### Step 3: Configure Environment Variables
Create `.env` file in `Cloud_Version/` directory:

```bash
# Upstash Vector Configuration
UPSTASH_VECTOR_REST_URL=https://resolved-pig-86020-us1-vector.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your_token_here

# Groq API Configuration
GROQ_API_KEY=gsk_your_groq_api_key_here
```

#### Step 4: Run the System
```bash
# Automated test (recommended first)
python test_groq.py

# Interactive mode
python rag_run_groq.py
```

**Expected First Run**:
```
🔍 Checking for existing documents in Upstash...
🆕 Adding 100 documents to Upstash Vector...
✅ Successfully added 100 documents!

🏥 Running health checks...
✅ Upstash Vector: Connected (100 vectors, 1024D)
✅ Groq API: Connected (llama-3.1-8b-instant)

💬 Ask a question about food (type 'exit' to quit):
You: 
```

---

### Option B: Hybrid Cloud (Free Forever)

**Prerequisites**: Ollama installed locally

#### Step 1: Install Ollama
**Windows**: Download from [ollama.com](https://ollama.com)  
**macOS**: `brew install ollama`  
**Linux**: `curl -fsSL https://ollama.com/install.sh | sh`

#### Step 2: Download Model
```bash
ollama pull llama3.2
```

#### Step 3: Install Python Dependencies
```bash
cd Cloud_Version
pip install upstash-vector python-dotenv requests
```

#### Step 4: Get Upstash Credentials
Follow Step 2 from Option A (Upstash only, skip Groq)

#### Step 5: Configure Environment
Create `.env` file:
```bash
# Upstash Vector Configuration (only these two)
UPSTASH_VECTOR_REST_URL=https://your-index.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your_token_here
```

#### Step 6: Run Hybrid Version
```bash
python rag_run_upstash.py
```

---

### Option C: Original Local (100% Private)

**Prerequisites**: ChromaDB + Ollama

#### Step 1: Install Ollama
See Option B, Step 1

#### Step 2: Download Model
```bash
ollama pull llama3.2
```

#### Step 3: Install Dependencies
```bash
pip install chromadb requests
```

#### Step 4: Run Local Version
```bash
# From project root (not Cloud_Version)
cd ..
python rag_run.py
```

---

## 🔐 Environment Variables Configuration Guide

### Required Variables by Version

| Variable | Local | Hybrid | Full Cloud |
|----------|-------|--------|------------|
| `UPSTASH_VECTOR_REST_URL` | ❌ | ✅ | ✅ |
| `UPSTASH_VECTOR_REST_TOKEN` | ❌ | ✅ | ✅ |
| `GROQ_API_KEY` | ❌ | ❌ | ✅ |

### `.env` File Format

**Full Cloud**:
```bash
# Upstash Vector (Cloud Vector Database)
UPSTASH_VECTOR_REST_URL=https://resolved-pig-86020-us1-vector.upstash.io
UPSTASH_VECTOR_REST_TOKEN=ABYFMHJlc29sdmVkLXBpZy04NjAyMA==

# Groq API (Cloud LLM)
GROQ_API_KEY=gsk_K52QgacVQHN0zAT8zgwXWGdyb3FY
```

**Hybrid Cloud**:
```bash
# Upstash Vector (Cloud Vector Database)
UPSTASH_VECTOR_REST_URL=https://resolved-pig-86020-us1-vector.upstash.io
UPSTASH_VECTOR_REST_TOKEN=ABYFMHJlc29sdmVkLXBpZy04NjAyMA==

# No Groq key needed - uses local Ollama
```

**Local**:
```bash
# No .env file needed - fully local
```

### Security Best Practices

✅ **DO**:
- Keep `.env` file in `.gitignore` (already configured)
- Use environment-specific keys (dev vs production)
- Rotate API keys regularly
- Use secrets managers in production (AWS Secrets Manager, Azure Key Vault)

❌ **DON'T**:
- Commit `.env` to version control
- Share API keys in chat/email
- Use production keys for development
- Hard-code credentials in source files

### Troubleshooting Environment Variables

**"Invalid API key" error**:
```bash
# Check if .env file exists
ls -la .env

# Verify no extra quotes or spaces
cat .env | grep GROQ_API_KEY
# Should show: GROQ_API_KEY=gsk_xxxxx
# NOT: GROQ_API_KEY="gsk_xxxxx" or GROQ_API_KEY = gsk_xxxxx
```

**Environment not loading**:
```python
# Test in Python
from dotenv import load_dotenv
import os

load_dotenv()
print(os.getenv("GROQ_API_KEY"))  # Should print your key
print(os.getenv("UPSTASH_VECTOR_REST_URL"))  # Should print URL
```

---

## � Comparison Table: Local vs Cloud

| Feature | Original Local | Hybrid Cloud | Full Cloud ⭐ |
|---------|----------------|--------------|---------------|
| **Response Time** | 5-15 seconds | 5-15 seconds | **0.5-1.5 seconds** ⚡ |
| **Generation Speed** | 10-30 tokens/sec | 10-30 tokens/sec | **500-800 tokens/sec** 🚀 |
| **Setup Time** | 30 minutes | 10 minutes | **2 minutes** ✅ |
| **Monthly Cost** | $0 (+ electricity) | $0 | **$0.04-$4** 💰 |
| **Dependencies** | ChromaDB + Ollama | Ollama only | **None** 🎯 |
| **Internet Required** | No ✅ | Yes (search only) | Yes |
| **Privacy** | 100% local ✅ | Hybrid | Cloud-based |
| **Scalability** | 1 user | 1 user | **Unlimited** 📈 |
| **Concurrent Users** | 1-2 | 1-2 | **Infinite** |
| **Auto-Embeddings** | No (manual) | Yes ✅ | Yes ✅ |
| **Streaming Support** | No | No | Yes ✅ |
| **Error Handling** | Basic | Basic | **Advanced** ⭐ |
| **Usage Tracking** | No | No | Yes ✅ |
| **Production Ready** | No | No | **Yes** ⭐ |
| **Maintenance** | Regular updates | Ollama updates | **Zero** ✅ |
| **Model Updates** | Manual | Manual | **Automatic** |
| **API Limits (Free)** | N/A | 10K queries/day | 6K queries/day |

### Performance Benchmarks

**Test Query**: "Tell me about Filipino food"

| Metric | Local | Hybrid | Full Cloud |
|--------|-------|--------|------------|
| **Vector Search** | 0.1-0.2s | 0.2-0.3s | 0.2-0.3s |
| **LLM Generation** | 5-15s | 5-15s | **0.5-1.0s** ⚡ |
| **Total Time** | 5.1-15.2s | 5.2-15.3s | **0.7-1.3s** |
| **Tokens Generated** | ~400 | ~400 | ~400 |
| **Cost per Query** | $0 | $0 | **$0.000068** |

### Cost Analysis (Monthly)

| Usage Level | Queries/Day | Local | Hybrid | Full Cloud |
|-------------|-------------|-------|--------|------------|
| **Light** | 10 | $0 | $0 | **$0.04** |
| **Moderate** | 100 | $0 | $0 | **$0.40** |
| **Heavy** | 1,000 | $0 | $0 | **$4.00** |

**Notes**:
- Local version has hidden costs (electricity, hardware wear)
- Hybrid and Full Cloud benefit from free tiers
- Full Cloud scales infinitely without hardware investment

---

## 🍜 Enhanced Food Database Showcase

Our database contains **100 carefully curated food items** across multiple categories:

### Database Statistics

| Category | Count | Example Items |
|----------|-------|---------------|
| **Filipino Cuisine** | 15 | Adobo, Sinigang, Lechon, Bibingka, Pancit |
| **Thai Cuisine** | 15 | Tom Yum, Pad Thai, Green Curry, Mango Sticky Rice |
| **Vietnamese Cuisine** | 15 | Pho, Banh Mi, Spring Rolls, Bun Cha |
| **Indian Cuisine** | 15 | Biryani, Palak Paneer, Butter Chicken, Samosas |
| **Chinese Cuisine** | 15 | Peking Duck, Dim Sum, Hot Pot, Mapo Tofu |
| **Healthy Foods** | 15 | Greek Yogurt Parfait, Quinoa Bowl, Avocado Toast |
| **International** | 10 | Tacos, Pizza, Sushi, Paella |

### Data Structure

Each food item includes:

```json
{
  "id": "food_001",
  "name": "Adobo",
  "category": "Main Dish",
  "category_group": "Filipino Cuisine",
  "origin": "Philippines",
  "description": "Savory-sour stew with meat in soy sauce and vinegar",
  "ingredients": ["pork or chicken", "soy sauce", "vinegar", "garlic", "bay leaves"],
  "preparation_method": "Simmer meat in marinade until tender",
  "cooking_time_minutes": 45,
  "dietary_classifications": ["Gluten-Free", "Dairy-Free"],
  "nutritional_highlights": "High in protein, moderate fat",
  "cultural_significance": "National dish of the Philippines",
  "serving_suggestions": "Served with steamed rice",
  "flavor_profile": ["Savory", "Tangy", "Umami"]
}
```

### Featured Highlights

**Most Popular Dishes**:
1. 🇵🇭 **Adobo** - Filipino savory-sour stew (5-star comfort food)
2. 🇹🇭 **Pad Thai** - Iconic Thai stir-fried noodles
3. 🇻🇳 **Pho** - Vietnamese aromatic soup with rice noodles
4. 🇮🇳 **Biryani** - Layered rice with aromatic spices
5. 🇨🇳 **Peking Duck** - Crispy-skinned roasted duck

**Healthiest Options**:
1. 🥗 **Quinoa Buddha Bowl** - Complete protein, fiber-rich
2. 🍓 **Greek Yogurt Parfait** - Probiotics, antioxidants
3. 🥑 **Avocado Toast** - Healthy fats, vitamins
4. 🍲 **Vietnamese Pho** - Low-fat, nutrient-dense
5. 🥬 **Palak Paneer** - Iron, calcium, protein

**Vegetarian Favorites**:
- 🇮🇳 Palak Paneer, Rajma, Dal Makhani
- 🇹🇭 Green Curry (veggie version), Pad See Ew
- 🇨🇳 Mapo Tofu, Vegetable Spring Rolls
- 🥗 Buddha Bowls, Smoothies, Parfaits

**Quick & Easy (<30 min)**:
- Pad Thai, Banh Mi, Tacos, Spring Rolls, Avocado Toast

---

## 🔍 Advanced Query Examples and Expected Responses

### Example 1: Cultural Cuisine Exploration

**Query**: `"Tell me about Filipino food"`

**Expected Response**:
```
🔍 Searching vector database...
⚡ Vector search completed in 0.23s

🧠 Retrieved relevant information:
🔹 Source 1: Name: Adobo (score: 0.8533)
🔹 Source 2: Name: Bibingka (score: 0.8507)
🔹 Source 3: Name: Sinigang (score: 0.8434)

🤖 Generating answer with Groq (ultra-fast)...
⚡ Generation completed in 1.01s
✅ Total query time: 1.25s

📊 Tokens used: 1395 (prompt: 953, completion: 442)

🤖 Answer:
Filipino food is a vibrant and diverse culinary tradition that reflects the 
country's rich cultural heritage. It's characterized by bold flavors combining 
sweet, sour, salty, and umami tastes. 

Key dishes include:
- **Adobo**: The national dish, a savory-sour stew made with meat, soy sauce, 
  vinegar, and spices. It represents Filipino resourcefulness and comfort food.
- **Sinigang**: A tangy soup using tamarind as a souring agent, often made with 
  pork or fish and various vegetables.
- **Bibingka**: A traditional rice cake made with coconut milk, often served 
  during Christmas season.

Filipino cuisine emphasizes:
- Sharing and community (meals are social events)
- Balance of flavors (sweet, sour, salty)
- Local ingredients (coconut, rice, seafood)
- Spanish and Chinese influences from colonial history
```

---

### Example 2: Dietary Requirements

**Query**: `"What are healthy breakfast options?"`

**Expected Response**:
```
🔍 Searching vector database...
⚡ Vector search completed in 0.24s

🧠 Retrieved relevant information:
🔹 Source 1: Name: Spinach and Mushroom Omelet (score: 0.8326)
🔹 Source 2: Name: Greek Yogurt Parfait (score: 0.8248)
🔹 Source 3: Name: Berry Oat Smoothie (score: 0.8037)

🤖 Answer:
Based on our database, here are three excellent healthy breakfast options:

1. **Spinach and Mushroom Omelet**
   - High in protein and B vitamins
   - Rich in iron from spinach
   - Ready in just 10 minutes
   - Gluten-free and vegetarian
   
2. **Greek Yogurt Parfait**
   - Excellent source of probiotics for gut health
   - Packed with antioxidants from berries
   - High protein content keeps you full
   - Quick to assemble (5 minutes)
   
3. **Berry Oat Smoothie**
   - High fiber from oats
   - Polyphenols from mixed berries
   - Omega-3s from ground flaxseed
   - Portable option for busy mornings

All three options are gluten-free, vegetarian, and provide sustained energy 
throughout the morning without the sugar crash.
```

---

### Example 3: Cuisine Comparison

**Query**: `"Compare Thai and Vietnamese cuisine"`

**Expected Response**:
```
🧠 Retrieved relevant information:
🔹 Source 1: Name: Pad Thai (score: 0.8654)
🔹 Source 2: Name: Pho (score: 0.8521)
🔹 Source 3: Name: Tom Yum (score: 0.8443)

🤖 Answer:
Thai and Vietnamese cuisines share Southeast Asian roots but have distinct 
characteristics:

**Thai Cuisine:**
- **Flavors**: Bold, spicy, sweet, and aromatic
- **Key ingredients**: Coconut milk, lemongrass, galangal, Thai basil
- **Cooking methods**: Stir-frying, curries, quick high-heat cooking
- **Signature dishes**: Pad Thai (stir-fried noodles), Tom Yum (hot & sour soup)
- **Profile**: Rich, creamy, intensely flavored

**Vietnamese Cuisine:**
- **Flavors**: Fresh, light, herbaceous, balanced
- **Key ingredients**: Fish sauce, fresh herbs (cilantro, mint), lime
- **Cooking methods**: Broth-based soups, fresh rolls, quick stir-fries
- **Signature dishes**: Pho (noodle soup), Banh Mi (sandwich), Spring Rolls
- **Profile**: Clean, refreshing, subtle

**Key Differences:**
- Thai food tends to be richer and spicier
- Vietnamese food emphasizes freshness and lightness
- Thai uses more coconut milk and curry pastes
- Vietnamese focuses on herbs and clear broths
```

---

### Example 4: Ingredient-Based Search

**Query**: `"What dishes use coconut?"`

**Expected Response**:
```
🧠 Retrieved relevant information:
🔹 Source 1: Name: Thai Green Curry (score: 0.8876)
🔹 Source 2: Name: Bibingka (score: 0.8654)
🔹 Source 3: Name: Mango Sticky Rice (score: 0.8543)

🤖 Answer:
Many delicious dishes feature coconut as a key ingredient:

**Savory Dishes:**
- **Thai Green Curry**: Uses coconut milk for a rich, creamy base combined with 
  green curry paste, vegetables, and protein.
- **Rendang**: Indonesian slow-cooked curry with meat in coconut milk
- **Laksa**: Malaysian spicy coconut curry noodle soup

**Sweet Dishes:**
- **Bibingka**: Filipino rice cake made with coconut milk, creating a moist, 
  slightly chewy texture. Often topped with salted egg and cheese.
- **Mango Sticky Rice**: Thai dessert pairing glutinous rice cooked in coconut 
  milk with fresh mango slices.

**Why coconut?**
- Adds richness without dairy
- Provides healthy medium-chain fatty acids
- Creates creamy texture in curries and desserts
- Common in tropical Southeast Asian cuisines
```

---

### Example 5: Meal Planning

**Query**: `"Suggest a vegetarian meal plan from Indian cuisine"`

**Expected Response**:
```
🧠 Retrieved relevant information:
🔹 Source 1: Name: Palak Paneer (score: 0.8765)
🔹 Source 2: Name: Rajma (score: 0.8654)
🔹 Source 3: Name: Dal Makhani (score: 0.8543)

🤖 Answer:
Here's a delicious vegetarian Indian meal plan:

**Breakfast:**
- Paratha (whole wheat flatbread) with yogurt
- Chai tea

**Lunch:**
- **Rajma** (red kidney bean curry)
  - High in protein and fiber
  - Served with basmati rice
  - Rich in iron and folate
  
**Dinner:**
- **Palak Paneer** (spinach with Indian cheese)
  - Creamy spinach base with paneer cubes
  - Excellent source of calcium and iron
  - Served with roti or naan
  
**Sides:**
- **Dal Makhani** (black lentils in creamy sauce)
- Cucumber raita (cooling yogurt sauce)
- Pickled vegetables

**Nutritional Benefits:**
- Complete proteins from legume-grain combinations
- High fiber content aids digestion
- Rich in vitamins A, C, and K from spinach
- Calcium from paneer and yogurt
- All vegetarian and can be made vegan (substitute paneer)

**Cooking Tips:**
- Use moderate spices for milder flavor
- Fresh ginger and garlic enhance taste and aid digestion
- Serve with basmati rice or whole wheat rotis
```

---

### Example 6: Dietary Restrictions

**Query**: `"Show me gluten-free options"`

**Expected Response**:
```
🧠 Retrieved relevant information:
🔹 Source 1: Name: Vietnamese Pho (score: 0.8876)
🔹 Source 2: Name: Adobo (score: 0.8765)
🔹 Source 3: Name: Quinoa Buddha Bowl (score: 0.8654)

🤖 Answer:
We have many delicious gluten-free options across various cuisines:

**Asian Cuisine (naturally gluten-free):**
- **Vietnamese Pho**: Rice noodles in aromatic broth
- **Filipino Adobo**: Meat stew with soy sauce (use tamari for GF)
- **Thai Green Curry**: Rice served with coconut curry
- **Spring Rolls**: Rice paper wraps with fresh vegetables

**Healthy Options:**
- **Quinoa Buddha Bowl**: Complete protein, nutrient-dense
- **Greek Yogurt Parfait**: Probiotic-rich breakfast
- **Avocado Toast**: Use GF bread
- **Smoothie Bowls**: Naturally gluten-free

**Main Dishes:**
- Most rice-based Asian dishes
- Grilled meats and seafood
- Vegetable curries
- Egg-based dishes (omelets, frittatas)

**Important Note:**
- Always verify soy sauce is gluten-free (use tamari)
- Check for cross-contamination in restaurants
- Rice noodles are naturally gluten-free
- Most curries are safe if thickened naturally
```

---

## �️ Interactive Commands

All versions support these commands:

| Command | Description | Available In |
|---------|-------------|--------------|
| `health` | Check system connectivity | All versions |
| `stream` | Toggle streaming mode | Full Cloud only |
| `stats` | View usage statistics | Full Cloud only |
| `exit` | Quit application | All versions |

### Usage Examples

```bash
You: health
🏥 Running health checks...
✅ Upstash Vector: Connected (100 vectors, 1024D)
✅ Groq API: Connected (llama-3.1-8b-instant)

You: stream
🔄 Streaming mode: ON

You: stats
📊 Usage Statistics:
   Queries: 15
   Total tokens: 12,450
   Avg tokens/query: 830
   Estimated cost: $0.000811

You: Tell me about Thai food
[Streaming response appears in real-time...]
```

---

## 📁 File Structure

```
Cloud_Version/
├── .env                          # API credentials (create this)
├── fooddatabase.json             # 100 food items database
│
├── 🟢 rag_run_groq.py            # Full Cloud (Upstash + Groq) ⭐
├── 🟡 rag_run_upstash.py         # Hybrid (Upstash + Ollama)
├── ⚪ rag_run.py                 # Original (ChromaDB + Ollama)
│
├── test_groq.py                  # Automated test suite
├── migrate_chroma_to_upstash.py  # Migration utility
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🚀 Advanced Features

### Full Cloud Version (`rag_run_groq.py`)

**Production Features**:
- ✅ **Streaming Responses**: Real-time token generation
- ✅ **Error Handling**: Automatic retries with exponential backoff
- ✅ **Rate Limiting**: Respects API limits (30 req/min)
- ✅ **Usage Tracking**: Token counting and cost estimation
- ✅ **Health Checks**: Pre-flight connectivity verification
- ✅ **Concurrent Support**: Handles unlimited simultaneous users

**Error Recovery**:
```python
# Automatic retry on failure
RateLimitError → Wait 2^n seconds → Retry
APITimeoutError → Immediate retry (max 3 attempts)
APIError → Log and return informative message
```

**Usage Tracking**:
```python
usage_stats = {
    "queries": 15,
    "total_tokens": 12450,
    "prompt_tokens": 8320,
    "completion_tokens": 4130
}
# Estimated cost: $0.000811
```

### Hybrid Version (`rag_run_upstash.py`)

**Features**:
- ✅ **Auto-Embeddings**: Upstash handles vectorization
- ✅ **Cloud Storage**: No local database management
- ✅ **Batch Upsert**: Efficient data uploads (100 items/batch)
- ✅ **Error Handling**: Network failure recovery
- ✅ **Health Checks**: Upstash + Ollama connectivity

### Migration Tools

**Migrate from ChromaDB to Upstash**:
```bash
# Preview migration (no changes)
python migrate_chroma_to_upstash.py --dry-run

# Execute migration
python migrate_chroma_to_upstash.py

# Custom batch size
python migrate_chroma_to_upstash.py --batch-size 50

# Validate after migration
python migrate_chroma_to_upstash.py --validate
```

**Migration Features**:
- Preserves all metadata
- Validates data integrity
- Progress tracking
- Rollback capability

---

## 💰 Cost Analysis

### Free Tier Limits

**Upstash Vector**:
- ✅ 10,000 queries/day
- ✅ 10,000 vectors storage
- ✅ Unlimited read operations
- **Our usage**: 100 vectors (1% of limit)

**Groq API**:
- ✅ 30 requests/minute
- ✅ 6,000 requests/day
- ✅ 7,000 requests/week
- **Estimate**: ~100-500 requests/day typical

### Paid Usage (if exceeded)

**Groq Pricing**:
- Input: $0.05 per 1M tokens
- Output: $0.08 per 1M tokens
- Average query: ~1000 tokens
- **Cost per query**: ~$0.000068

**Monthly Estimates**:
| Daily Queries | Monthly Queries | Cost |
|---------------|-----------------|------|
| 10 | 300 | $0.04 |
| 50 | 1,500 | $0.20 |
| 100 | 3,000 | $0.40 |
| 500 | 15,000 | $2.04 |
| 1,000 | 30,000 | $4.08 |

**Cost Comparison**:
- **Local**: $0/month + electricity (~$10-50 for GPU)
- **Hybrid**: $0/month (free tiers)
- **Full Cloud**: $0.04-$4/month (scales with usage)

---

## 🔧 Troubleshooting Guide for Common Cloud Setup Issues

### Issue 1: "Invalid API Key" or Authentication Errors

**Symptoms**:
```
❌ Groq API: Failed (401 Unauthorized)
❌ Upstash Vector: Failed (Authentication failed)
```

**Solutions**:

✅ **Check .env file format**:
```bash
# CORRECT format (no quotes, no spaces around =)
GROQ_API_KEY=gsk_xxxxx
UPSTASH_VECTOR_REST_TOKEN=ABYFxxxx

# WRONG formats
GROQ_API_KEY = "gsk_xxxxx"  # ❌ Has quotes and spaces
GROQ_API_KEY="gsk_xxxxx"    # ❌ Has quotes
GROQ_API_KEY = gsk_xxxxx    # ❌ Has spaces
```

✅ **Verify keys are valid**:
```bash
# Test Groq key
curl -X POST https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer YOUR_GROQ_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"llama-3.1-8b-instant","messages":[{"role":"user","content":"Hello"}]}'

# Test Upstash (check console for correct URL/token)
curl -X GET YOUR_UPSTASH_URL/info \
  -H "Authorization: Bearer YOUR_UPSTASH_TOKEN"
```

✅ **Regenerate keys if needed**:
- Groq: [console.groq.com](https://console.groq.com) → API Keys → Create New
- Upstash: [console.upstash.com](https://console.upstash.com) → Vector → Your Index → Copy Token

---

### Issue 2: "Rate Limit Exceeded"

**Symptoms**:
```
⚠️ Rate limited. Retrying in 2s...
❌ Rate limit exceeded. Please try again in a few moments.
```

**Solutions**:

✅ **Wait and retry** (automatic in Full Cloud version):
```python
# System automatically waits with exponential backoff
Attempt 1: Wait 2 seconds
Attempt 2: Wait 4 seconds
Attempt 3: Wait 8 seconds
```

✅ **Check free tier limits**:
- Groq: 30 requests/minute, 6,000/day
- Upstash: 10,000 queries/day

✅ **Upgrade if needed**:
- Groq: [console.groq.com/settings/billing](https://console.groq.com/settings/billing)
- Upstash: Pay-as-you-go automatically scales

✅ **Implement request throttling**:
```python
import time
queries = ["query1", "query2", "query3"]
for query in queries:
    rag_query(query)
    time.sleep(2)  # Wait 2 seconds between queries
```

---

### Issue 3: "Connection Timeout" or Network Errors

**Symptoms**:
```
❌ Request timed out. Please try again.
ConnectionError: Failed to establish connection
```

**Solutions**:

✅ **Check internet connectivity**:
```bash
# Test connectivity
ping console.groq.com
ping console.upstash.com

# Test with curl
curl -I https://api.groq.com
curl -I https://your-index.upstash.io
```

✅ **Check firewall/proxy settings**:
```bash
# Verify no firewall blocking
# Allow outbound HTTPS (port 443) to:
# - *.groq.com
# - *.upstash.io
```

✅ **Increase timeout (if slow connection)**:
```python
# In rag_run_groq.py, modify:
groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    timeout=60.0,  # Increase from 30 to 60 seconds
    max_retries=3
)
```

✅ **Use local fallback**:
```bash
# If cloud is down, use hybrid version
python rag_run_upstash.py  # Uses local Ollama for LLM
```

---

### Issue 4: "Module Not Found" or Import Errors

**Symptoms**:
```
ModuleNotFoundError: No module named 'groq'
ModuleNotFoundError: No module named 'upstash_vector'
```

**Solutions**:

✅ **Install all dependencies**:
```bash
pip install -r requirements.txt

# Or install individually
pip install groq upstash-vector python-dotenv requests
```

✅ **Check Python version**:
```bash
python --version  # Should be 3.8 or higher

# If using Python 3.7 or lower, upgrade
```

✅ **Use virtual environment (recommended)**:
```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

✅ **Clear pip cache if corrupted**:
```bash
pip cache purge
pip install --no-cache-dir -r requirements.txt
```

---

### Issue 5: "Ollama Connection Refused" (Hybrid Version)

**Symptoms**:
```
❌ Error: Could not connect to Ollama at http://localhost:11434
ConnectionRefusedError: [Errno 111] Connection refused
```

**Solutions**:

✅ **Start Ollama service**:
```bash
# Start Ollama
ollama serve

# In separate terminal, run app
python rag_run_upstash.py
```

✅ **Verify Ollama is installed**:
```bash
ollama --version

# If not installed:
# Windows: Download from ollama.com
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.com/install.sh | sh
```

✅ **Check model is downloaded**:
```bash
ollama list

# If llama3.2 not listed:
ollama pull llama3.2
```

✅ **Verify port is not blocked**:
```bash
# Check if port 11434 is in use
netstat -ano | findstr :11434  # Windows
lsof -i :11434                 # macOS/Linux

# Kill process if needed and restart Ollama
```

---

### Issue 6: "No Documents Found" or Empty Results

**Symptoms**:
```
🔍 Searching vector database...
⚠️ No documents found matching your query
```

**Solutions**:

✅ **Check if data was uploaded**:
```python
# In Python
from upstash_vector import Index
import os
from dotenv import load_dotenv

load_dotenv()
index = Index(
    url=os.getenv("UPSTASH_VECTOR_REST_URL"),
    token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
)

info = index.info()
print(f"Vector count: {info.vector_count}")  # Should be 100
```

✅ **Re-upload data**:
```bash
# Delete chroma_db folder if exists
rm -rf chroma_db

# Run script again to re-upload
python rag_run_groq.py
```

✅ **Verify Upstash index configuration**:
- Login to [console.upstash.com](https://console.upstash.com)
- Check Vector Index settings
- Model should be: `mixedbread-ai/mxbai-embed-large-v1`
- Dimensions: 1024

---

### Issue 7: "Slow Performance" in Full Cloud Version

**Symptoms**:
```
⚡ Total query time: 15.5s  (Expected: 0.5-1.5s)
```

**Solutions**:

✅ **Check internet speed**:
```bash
# Run speed test
speedtest-cli

# Minimum recommended: 10 Mbps download
```

✅ **Use streaming mode for better UX**:
```bash
You: stream
🔄 Streaming mode: ON

# Now responses appear as they're generated
```

✅ **Reduce context size if needed**:
```python
# In rag_run_groq.py, modify:
results = index.query(
    data=question,
    top_k=2,  # Reduce from 3 to 2
    include_metadata=True
)
```

✅ **Check Groq API status**:
- Visit [status.groq.com](https://status.groq.com)
- If degraded, wait or use hybrid version

---

### Issue 8: "Unexpected High Costs"

**Symptoms**:
```
📊 Estimated cost: $15.00  (Expected: $0.40)
```

**Solutions**:

✅ **Check usage statistics**:
```bash
You: stats
📊 Usage Statistics:
   Queries: 15,000  # ← Too many queries!
   Total tokens: 15,000,000
   Estimated cost: $15.00
```

✅ **Implement caching for common queries**:
```python
# Cache responses for repeated questions
cache = {}
def cached_query(question):
    if question in cache:
        return cache[question]
    answer = rag_query(question)
    cache[question] = answer
    return answer
```

✅ **Reduce max_tokens**:
```python
# In rag_run_groq.py, modify:
completion = groq_client.chat.completions.create(
    model=GROQ_MODEL,
    messages=[...],
    max_tokens=512,  # Reduce from 1024
    temperature=0.7
)
```

✅ **Set up usage alerts**:
- Groq: [console.groq.com/settings/billing](https://console.groq.com/settings/billing) → Set spending limits

---

### Quick Diagnostic Script

Run this to check all systems:

```python
# diagnostic.py
import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 SYSTEM DIAGNOSTICS\n")

# Check environment variables
print("1. Environment Variables:")
vars_to_check = [
    "UPSTASH_VECTOR_REST_URL",
    "UPSTASH_VECTOR_REST_TOKEN",
    "GROQ_API_KEY"
]
for var in vars_to_check:
    value = os.getenv(var)
    if value:
        print(f"   ✅ {var}: {'*' * 20} (set)")
    else:
        print(f"   ❌ {var}: Not set")

# Check Upstash
print("\n2. Upstash Vector:")
try:
    from upstash_vector import Index
    index = Index(
        url=os.getenv("UPSTASH_VECTOR_REST_URL"),
        token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
    )
    info = index.info()
    print(f"   ✅ Connected: {info.vector_count} vectors, {info.dimension}D")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Check Groq
print("\n3. Groq API:")
try:
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Hi"}],
        max_tokens=5
    )
    print(f"   ✅ Connected: {response.model}")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print("\n✅ Diagnostics complete!")
```

Run with: `python diagnostic.py`

---

## � Additional Resources

### Documentation
- **[../README.md](../README.md)** - Main project overview
- **[../MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md)** - Architecture comparison & setup guide
- **[../QUICK_REFERENCE.md](../QUICK_REFERENCE.md)** - Quick commands & troubleshooting
- **[../IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md)** - Complete implementation report
- **[../upstash-migration-prd.md](../upstash-migration-prd.md)** - Phase 1 design document
- **[../cloud-hosted-groq-migration-prd.md](../cloud-hosted-groq-migration-prd.md)** - Phase 2 design document

### External Links
- [Upstash Vector Documentation](https://upstash.com/docs/vector)
- [Groq API Documentation](https://console.groq.com/docs)
- [Ollama Documentation](https://ollama.com/docs)
- [mixedbread-ai Embedding Model](https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1)

---

## 🎓 Learning Path

### Beginner (15 minutes)
1. Read [Cloud Migration Overview](#-cloud-migration-overview) (5 min)
2. Follow [Setup Instructions](#-setup-instructions) for Full Cloud (5 min)
3. Run `python test_groq.py` (5 min)

### Intermediate (1 hour)
1. Complete Beginner path (15 min)
2. Read [Comparison Table](#-comparison-table-local-vs-cloud) (10 min)
3. Review [Advanced Query Examples](#-advanced-query-examples-and-expected-responses) (15 min)
4. Experiment with different queries (20 min)

### Advanced (2-3 hours)
1. Complete Intermediate path (1 hour)
2. Read design documents (30 min)
3. Review source code (30 min)
4. Implement custom modifications (30-60 min)

---

## 🚦 Getting Started Checklist

### Full Cloud Setup
- [ ] Python 3.8+ installed
- [ ] Created Upstash account
- [ ] Created Groq account
- [ ] Obtained API keys
- [ ] Created `.env` file with credentials
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Ran test: `python test_groq.py`
- [ ] All 3 tests passed ✅
- [ ] Tried interactive mode: `python rag_run_groq.py`

### Hybrid Cloud Setup
- [ ] Python 3.8+ installed
- [ ] Ollama installed
- [ ] Downloaded llama3.2 model
- [ ] Created Upstash account
- [ ] Obtained Upstash credentials
- [ ] Created `.env` file (Upstash only)
- [ ] Installed dependencies
- [ ] Started Ollama: `ollama serve`
- [ ] Ran hybrid version: `python rag_run_upstash.py`

---

## 🎯 Quick Start Summary

**Want to try it RIGHT NOW?** (2 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Get free API keys
# - Upstash: https://console.upstash.com (30 seconds)
# - Groq: https://console.groq.com (30 seconds)

# 3. Create .env file
echo "UPSTASH_VECTOR_REST_URL=your_url" > .env
echo "UPSTASH_VECTOR_REST_TOKEN=your_token" >> .env
echo "GROQ_API_KEY=your_key" >> .env

# 4. Run automated test
python test_groq.py

# 5. See results in ~3 seconds! ⚡
```

**Expected Output**:
```
✅ Test 1: 1.25s, $0.000091
✅ Test 2: 0.71s, $0.000060
✅ Test 3: 0.76s, $0.000054
📊 SUMMARY: $0.000205 total
```

---

## 💡 Pro Tips

### Performance Optimization
1. **Use streaming mode** for long responses (better UX)
2. **Cache common queries** to reduce API costs
3. **Reduce top_k** to 2 if responses are too long
4. **Lower max_tokens** for concise answers (saves money)

### Cost Optimization
1. **Start with free tiers** (sufficient for most users)
2. **Monitor usage** with `stats` command
3. **Implement caching** for repeated questions
4. **Set temperature lower** (0.5) for more focused answers
5. **Use context truncation** for very long documents

### Development Best Practices
1. **Test locally first** (use hybrid version for development)
2. **Use environment-specific keys** (dev vs prod)
3. **Implement error handling** for production
4. **Add logging** for debugging
5. **Version control .env.example** (not actual .env)

### Production Deployment
1. **Use secrets manager** (AWS Secrets Manager, Azure Key Vault)
2. **Set up monitoring** (track usage, errors, latency)
3. **Implement rate limiting** (prevent abuse)
4. **Add request queuing** (handle spikes)
5. **Set up alerts** (cost limits, error rates)

---

## 🤝 Support & Community

### Getting Help

**For setup issues**:
1. Check [Troubleshooting Guide](#-troubleshooting-guide-for-common-cloud-setup-issues)
2. Run diagnostic script (see Issue 8 above)
3. Verify all environment variables are set correctly

**For general questions**:
1. Review documentation in this README
2. Check [MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md)
3. Read [QUICK_REFERENCE.md](../QUICK_REFERENCE.md)

**For bugs or feature requests**:
1. Check if issue is already documented
2. Create detailed issue report with:
   - System info (OS, Python version)
   - Error messages (full stack trace)
   - Steps to reproduce
   - Expected vs actual behavior

---

## 📊 Project Statistics

- **Total Code**: 2,400+ lines
- **Documentation**: 26,000+ words
- **Food Items**: 100 (across 6 categories)
- **Supported Queries**: Unlimited variations
- **Response Time**: 0.5-1.5s (Full Cloud)
- **Cost per Query**: ~$0.000068 (Full Cloud)
- **Free Tier**: Sufficient for 6,000 queries/day
- **Setup Time**: 2 minutes (Full Cloud)
- **Performance Gain**: 10x faster than local

---

## 🏆 Success Metrics

After setup, you should see:

### Full Cloud
- ✅ Test completion: ~3 seconds for 3 queries
- ✅ Average query time: 0.5-1.5 seconds
- ✅ Generation speed: 500-800 tokens/sec
- ✅ Cost per query: ~$0.000068
- ✅ Health checks: All systems passing

### Hybrid Cloud
- ✅ Vector search: 0.2-0.3 seconds
- ✅ LLM generation: 5-15 seconds
- ✅ Total query time: 5-15 seconds
- ✅ Monthly cost: $0
- ✅ Upstash + Ollama connected

### Local
- ✅ Fully offline capable
- ✅ 100% private processing
- ✅ No API dependencies
- ✅ Zero monthly costs

---

## 🔄 Version History

### v3.0 - Full Cloud 
- ✅ Added Groq API integration
- ✅ Achieved 10x performance improvement
- ✅ Implemented streaming support
- ✅ Added usage tracking and cost estimation
- ✅ Production-ready error handling

### v2.0 - Hybrid Cloud
- ✅ Migrated to Upstash Vector
- ✅ Automatic cloud-based embeddings
- ✅ Removed local embedding dependencies
- ✅ Added migration tools

### v1.0 - Original Local
- ✅ Initial RAG implementation
- ✅ ChromaDB local storage
- ✅ Ollama local embeddings + LLM
- ✅ 100 food items database

---

## 👨‍🍳 Credits

**Original Project**: [RAG-Food](https://github.com/gocallum/ragfood) by Callum Bir

**Enhanced by Dennis Bonnici** with:
- 100 carefully curated food items
- Cloud migration (Upstash Vector + Groq API)
- Comprehensive documentation (26,000+ words)
- Production-ready features
- Automated testing suite

**Technologies Used**:
- [Python](https://python.org) - Programming language
- [Upstash Vector](https://upstash.com/docs/vector) - Cloud vector database
- [Groq API](https://groq.com) - Ultra-fast LLM inference
- [Ollama](https://ollama.com) - Local LLM deployment
- [mixedbread-ai/mxbai-embed-large-v1](https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1) - Embedding model
- [llama-3.1-8b-instant](https://groq.com/models) - Language model

---

## 📝 License

This project is for educational purposes. Please refer to individual technology licenses:
- Upstash: [Terms of Service](https://upstash.com/terms)
- Groq: [Terms of Service](https://groq.com/terms)
- Ollama: [MIT License](https://github.com/ollama/ollama/blob/main/LICENSE)

---

## 🎉 Conclusion

You now have access to three RAG architectures:

1. **Local**: Perfect for privacy and offline use
2. **Hybrid**: Best balance of cost and features
3. **Full Cloud**: Production-ready with best performance

Choose the version that fits your needs and start querying the food database!

**Ready to start?**
```bash
python test_groq.py  # See it in action!
```

---

**Last Updated**: December 9, 2025  
**Status**: ✅ Production Ready  
**Recommendation**: Use Full Cloud (`rag_run_groq.py`) for best experience

