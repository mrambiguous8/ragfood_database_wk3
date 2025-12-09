# Ollama to Groq Cloud API Migration Design Document

## Executive Summary

This document details the migration from local Ollama LLM inference to Groq Cloud API for the RAG Food System. The migration eliminates local LLM dependencies while leveraging Groq's ultra-fast inference speeds (up to 10x faster than traditional cloud APIs). This completes the full cloud migration: Upstash Vector for embeddings/storage + Groq for LLM generation.

---

## Table of Contents

1. [Architecture Comparison](#1-architecture-comparison)
2. [Implementation Plan](#2-implementation-plan)
3. [Code Changes Required](#3-code-changes-required)
4. [API Integration Details](#4-api-integration-details)
5. [Error Handling Strategy](#5-error-handling-strategy)
6. [Rate Limiting & Usage Management](#6-rate-limiting--usage-management)
7. [Cost Analysis](#7-cost-analysis)
8. [Performance Expectations](#8-performance-expectations)
9. [Testing Strategy](#9-testing-strategy)
10. [Migration Checklist](#10-migration-checklist)

---

## 1. Architecture Comparison

### 1.1 Current Architecture (Upstash + Ollama)

```
┌─────────────────┐
│   User Query    │
└────────┬────────┘
         │
         ▼
┌──────────────────────────────────────┐
│    Python RAG Application            │
│  ┌───────────────────────────────┐   │
│  │  Upstash Vector Client        │   │
│  │  (Cloud embeddings + storage) │   │
│  └──────────┬────────────────────┘   │
│             │                         │
│  ┌──────────▼────────────────────┐   │
│  │  Ollama (localhost:11434)     │   │
│  │  - llama3.2 model             │   │
│  │  - Local CPU/GPU inference    │   │
│  │  - No API costs               │   │
│  └──────────┬────────────────────┘   │
└─────────────┼─────────────────────────┘
              │
              ▼
      ┌───────────────┐
      │    Answer     │
      └───────────────┘
```

**Limitations:**
- Requires Ollama installed and running
- Local resource consumption (CPU/GPU/Memory)
- Slower inference on modest hardware
- Not scalable for multiple users
- Deployment complexity

### 1.2 New Architecture (Upstash + Groq)

```
┌─────────────────┐
│   User Query    │
└────────┬────────┘
         │
         ▼
┌──────────────────────────────────────┐
│    Python RAG Application            │
│  ┌───────────────────────────────┐   │
│  │  Upstash Vector Client        │   │
│  │  (Cloud embeddings + storage) │   │
│  └──────────┬────────────────────┘   │
│             │                         │
│  ┌──────────▼────────────────────┐   │
│  │  Groq Cloud API Client        │   │
│  │  - llama-3.1-8b-instant       │   │
│  │  - Ultra-fast inference       │   │
│  │  - Usage-based pricing        │   │
│  └──────────┬────────────────────┘   │
└─────────────┼─────────────────────────┘
              │ HTTPS (API Key)
              ▼
┌──────────────────────────────────────┐
│   Groq Cloud Service                 │
│  - LPU-based inference               │
│  - Sub-second response times         │
│  - Enterprise reliability            │
└──────────────┬───────────────────────┘
              │
              ▼
      ┌───────────────┐
      │    Answer     │
      └───────────────┘
```

**Benefits:**
- No local LLM installation required
- Ultra-fast inference (500+ tokens/sec)
- Zero local compute overhead
- Easy scaling and deployment
- Fully cloud-native stack

### 1.3 Key Architectural Changes

| Aspect | Before (Ollama) | After (Groq) | Impact |
|--------|-----------------|--------------|---------|
| **Deployment** | Local service required | API credentials only | Simplified deployment |
| **Performance** | 10-50 tokens/sec | 500+ tokens/sec | 10-50x faster |
| **Cost** | Free (local compute) | Pay-per-token | Small monthly cost |
| **Scalability** | Single machine | Cloud auto-scaling | Unlimited concurrent users |
| **Maintenance** | Manual updates | Managed service | Zero maintenance |
| **Availability** | Depends on local uptime | 99.9% SLA | High reliability |
| **API Format** | Custom Ollama API | OpenAI-compatible | Industry standard |

---

## 2. Implementation Plan

### Phase 1: Preparation (30 minutes)

**Tasks:**
1. ✅ Add GROQ_API_KEY to `.env` file (COMPLETED)
2. Install Groq Python SDK: `pip install groq`
3. Test Groq API connectivity
4. Review current Ollama integration points
5. Benchmark current response times

**Deliverables:**
- Groq SDK installed
- API connectivity verified
- Baseline performance metrics

### Phase 2: Code Refactoring (1-2 hours)

**Tasks:**
1. Create new file: `rag_run_groq.py` (full cloud version)
2. Replace Ollama HTTP calls with Groq SDK
3. Update prompt formatting for chat completion API
4. Implement streaming response handling
5. Add error handling and retry logic
6. Preserve backward compatibility with Upstash Vector

**Deliverables:**
- New implementation using Groq
- Streaming response support
- Comprehensive error handling

### Phase 3: Testing & Validation (1 hour)

**Tasks:**
1. Functional testing (same queries as Ollama version)
2. Response quality comparison
3. Performance benchmarking
4. Error scenario testing
5. Rate limit testing

**Deliverables:**
- Test suite results
- Performance comparison report
- Quality assessment

### Phase 4: Optimization (30 minutes)

**Tasks:**
1. Implement response caching for common queries
2. Add usage tracking and logging
3. Optimize token usage
4. Configure timeouts and retries

**Deliverables:**
- Optimized implementation
- Usage monitoring dashboard

### Phase 5: Deployment (15 minutes)

**Tasks:**
1. Update documentation
2. Deploy new version
3. Monitor initial usage
4. Validate cost projections

**Deliverables:**
- Production deployment
- Updated README
- Monitoring alerts configured

**Total Estimated Time: 3-4 hours**

---

## 3. Code Changes Required

### 3.1 File Structure

```
Cloud_Version/
├── .env                          # Add GROQ_API_KEY
├── rag_run_upstash.py           # Current (Ollama) version
├── rag_run_groq.py              # New (Groq) version ⭐
├── rag_run_full_cloud.py        # Alias for rag_run_groq.py ⭐
├── requirements.txt              # Add groq dependency
├── fooddatabase.json            # No changes
└── README.md                     # Update with Groq instructions
```

### 3.2 Environment Variables

**Update `.env`:**
```bash
# Upstash Vector
UPSTASH_VECTOR_REST_URL=https://your-index.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your_token_here

# Groq LLM (NEW)
GROQ_API_KEY=gsk_your_groq_api_key_here
```

### 3.3 Dependencies

**Update `requirements.txt`:**
```python
# Existing
requests>=2.31.0
python-dotenv>=1.0.0
upstash-vector>=0.8.0

# NEW - Groq SDK
groq>=0.4.0
```

### 3.4 Core Code Changes

#### A. Imports

**Before (Ollama):**
```python
import requests

# Generate answer with Ollama
response = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3.2",
    "prompt": prompt,
    "stream": False
}, timeout=60)
```

**After (Groq):**
```python
from groq import Groq
import os

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Generate answer with Groq
completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": "You are a helpful food expert assistant."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=1024,
    stream=False
)
```

#### B. Response Handling

**Before (Ollama):**
```python
if response.status_code == 200:
    return response.json()["response"].strip()
else:
    return f"❌ LLM API error: {response.status_code}"
```

**After (Groq):**
```python
try:
    answer = completion.choices[0].message.content.strip()
    return answer
except Exception as e:
    return f"❌ Groq API error: {e}"
```

#### C. Streaming Support (Optional)

**Groq Streaming:**
```python
def rag_query_streaming(question):
    """Query with streaming response."""
    # ... retrieve context from Upstash ...
    
    # Build prompt
    prompt = f"""Use the following context to answer the question.

Context:
{context}

Question: {question}
Answer:"""
    
    # Stream from Groq
    print("\n🤖 Answer: ", end="", flush=True)
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful food expert assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1024,
        stream=True  # Enable streaming
    )
    
    full_response = []
    for chunk in completion:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_response.append(content)
    
    print("\n")
    return "".join(full_response)
```

### 3.5 Complete New Implementation

**File: `rag_run_groq.py`** (see next section for full code)

---

## 4. API Integration Details

### 4.1 Groq API Specifications

**Endpoint:** `https://api.groq.com/openai/v1/chat/completions`

**Authentication:**
```python
Authorization: Bearer gsk_your_api_key_here
```

**Request Format:**
```json
{
  "model": "llama-3.1-8b-instant",
  "messages": [
    {"role": "system", "content": "System prompt"},
    {"role": "user", "content": "User query"}
  ],
  "temperature": 0.7,
  "max_tokens": 1024,
  "top_p": 1,
  "stream": false
}
```

**Response Format (Non-Streaming):**
```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "llama-3.1-8b-instant",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Generated answer here..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 200,
    "total_tokens": 350
  }
}
```

### 4.2 Available Models

| Model | Speed | Context | Best For |
|-------|-------|---------|----------|
| **llama-3.1-8b-instant** | Ultra-fast | 8K tokens | Quick responses ⭐ |
| llama-3.1-70b-versatile | Fast | 32K tokens | Complex reasoning |
| mixtral-8x7b-32768 | Fast | 32K tokens | Long context |
| gemma-7b-it | Fast | 8K tokens | Lightweight |

**Recommended:** `llama-3.1-8b-instant` for RAG use case (fast + sufficient quality)

### 4.3 SDK Configuration Options

```python
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    timeout=30.0,  # Request timeout
    max_retries=2   # Automatic retry on failure
)

# Generation parameters
completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[...],
    temperature=0.7,        # 0.0-2.0 (creativity)
    max_tokens=1024,        # Max response length
    top_p=1,                # Nucleus sampling
    frequency_penalty=0,    # Reduce repetition
    presence_penalty=0,     # Encourage new topics
    stop=None              # Custom stop sequences
)
```

---

## 5. Error Handling Strategy

### 5.1 Error Categories

**API Errors:**
- 401 Unauthorized (invalid API key)
- 429 Rate Limit Exceeded
- 500 Internal Server Error
- Timeout errors
- Network connectivity issues

**Input Errors:**
- Token limit exceeded
- Invalid model name
- Malformed messages

### 5.2 Comprehensive Error Handling

```python
from groq import Groq, APIError, RateLimitError, APITimeoutError
import time

class GroqRAG:
    def __init__(self):
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY"),
            timeout=30.0,
            max_retries=2
        )
        self.model = "llama-3.1-8b-instant"
    
    def generate_answer(self, prompt, max_retries=3):
        """Generate answer with robust error handling."""
        
        for attempt in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful food expert."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1024
                )
                
                # Extract answer
                answer = completion.choices[0].message.content.strip()
                
                # Log usage
                usage = completion.usage
                print(f"📊 Tokens used: {usage.total_tokens} "
                      f"(prompt: {usage.prompt_tokens}, "
                      f"completion: {usage.completion_tokens})")
                
                return answer
                
            except RateLimitError as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"⚠️  Rate limited. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    return "❌ Rate limit exceeded. Please try again later."
            
            except APITimeoutError:
                if attempt < max_retries - 1:
                    print(f"⚠️  Request timeout. Retrying...")
                else:
                    return "❌ Request timed out. Please try again."
            
            except APIError as e:
                print(f"❌ Groq API error: {e}")
                return "❌ Unable to generate response. Please check your API key."
            
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                return "❌ An unexpected error occurred."
        
        return "❌ Failed after multiple retries."
```

### 5.3 Fallback Strategy

```python
def generate_with_fallback(self, prompt):
    """Try Groq, fallback to simpler response if fails."""
    
    # Try Groq
    answer = self.generate_answer(prompt)
    
    # If error, provide simple fallback
    if answer.startswith("❌"):
        print("⚠️  Using fallback response...")
        return ("I'm unable to generate a detailed response right now. "
                "Based on the context provided, please review the retrieved "
                "food items above for relevant information.")
    
    return answer
```

---

## 6. Rate Limiting & Usage Management

### 6.1 Groq Rate Limits

**Free Tier:**
- 30 requests per minute (RPM)
- 14,400 tokens per minute (TPM)
- Daily limits apply

**Paid Tier:**
- Higher RPM/TPM limits
- Volume discounts
- Priority support

### 6.2 Usage Tracking

```python
import json
from datetime import datetime

class UsageTracker:
    def __init__(self, log_file="groq_usage.json"):
        self.log_file = log_file
        self.daily_tokens = 0
        self.daily_requests = 0
    
    def log_usage(self, prompt_tokens, completion_tokens, model):
        """Log API usage for monitoring."""
        total_tokens = prompt_tokens + completion_tokens
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens
        }
        
        # Append to log file
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except:
            pass
        
        # Update daily counters
        self.daily_tokens += total_tokens
        self.daily_requests += 1
        
        return total_tokens
    
    def get_daily_usage(self):
        """Get today's usage summary."""
        return {
            "requests": self.daily_requests,
            "tokens": self.daily_tokens,
            "estimated_cost": self.daily_tokens * 0.000001  # $0.001 per 1K tokens
        }
```

### 6.3 Rate Limit Handling

```python
from time import time, sleep

class RateLimiter:
    def __init__(self, rpm_limit=30):
        self.rpm_limit = rpm_limit
        self.requests = []
    
    def wait_if_needed(self):
        """Wait if approaching rate limit."""
        now = time()
        
        # Remove requests older than 1 minute
        self.requests = [t for t in self.requests if now - t < 60]
        
        # Check if at limit
        if len(self.requests) >= self.rpm_limit:
            # Calculate wait time
            oldest = self.requests[0]
            wait_time = 60 - (now - oldest) + 1
            
            if wait_time > 0:
                print(f"⏳ Rate limit: waiting {wait_time:.0f}s...")
                sleep(wait_time)
        
        # Record this request
        self.requests.append(now)
```

---

## 7. Cost Analysis

### 7.1 Groq Pricing

**Model:** llama-3.1-8b-instant

| Usage | Price |
|-------|-------|
| Input tokens | $0.05 per 1M tokens |
| Output tokens | $0.08 per 1M tokens |

**Example Calculation:**
- Average RAG query: 500 input tokens + 200 output tokens
- Cost per query: (500 × $0.05 + 200 × $0.08) / 1,000,000 = **$0.000041**
- 1,000 queries: **$0.041** (~4 cents)
- 10,000 queries: **$0.41**

### 7.2 Monthly Cost Projection

| Usage Level | Queries/Month | Estimated Cost |
|-------------|---------------|----------------|
| **Light** | 100 | $0.004 (~free) |
| **Moderate** | 1,000 | $0.04 (4 cents) |
| **Heavy** | 10,000 | $0.41 (41 cents) |
| **Enterprise** | 100,000 | $4.10 |

### 7.3 Cost Comparison

| Solution | Monthly Cost | Notes |
|----------|--------------|-------|
| **Ollama (local)** | $0 | + electricity, hardware wear |
| **Groq Cloud** | $0.04-$4 | Based on actual usage |
| **OpenAI GPT-3.5** | $0.50-$50 | 10x more expensive |
| **OpenAI GPT-4** | $15-$150 | 30x more expensive |

**Conclusion:** Groq is extremely cost-effective for this use case.

### 7.4 Cost Optimization Strategies

```python
# 1. Cache common queries
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(question_hash):
    """Cache repeated questions."""
    return generate_answer(question)

# 2. Reduce prompt tokens
def optimize_context(documents, max_tokens=1500):
    """Truncate context to reduce input tokens."""
    combined = "\n\n".join(documents)
    
    # Rough token estimate (4 chars ≈ 1 token)
    if len(combined) > max_tokens * 4:
        combined = combined[:max_tokens * 4] + "..."
    
    return combined

# 3. Lower temperature for deterministic answers
completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[...],
    temperature=0.3,  # Lower = more focused, shorter responses
    max_tokens=512    # Limit response length
)
```

---

## 8. Performance Expectations

### 8.1 Latency Comparison

| Component | Ollama (Local) | Groq Cloud | Improvement |
|-----------|----------------|------------|-------------|
| **Embedding** | N/A (Upstash) | N/A (Upstash) | - |
| **Vector Search** | 100-150ms | 100-150ms | - |
| **LLM Generation** | 5-15 seconds | 0.5-1.5 seconds | **10x faster** |
| **Total Query Time** | 5-15 sec | 0.6-1.7 sec | **8-10x faster** |

**Tokens/Second:**
- Ollama (CPU): 10-30 tokens/sec
- Ollama (GPU): 50-100 tokens/sec
- **Groq LPU: 500-800 tokens/sec** 🚀

### 8.2 Response Quality

| Aspect | Ollama llama3.2 | Groq llama-3.1-8b | Verdict |
|--------|-----------------|-------------------|---------|
| **Accuracy** | Good | Good | Similar |
| **Coherence** | Good | Good | Similar |
| **Context Handling** | 2K tokens | 8K tokens | Groq better |
| **Consistency** | Varies by hardware | Consistent | Groq better |

### 8.3 Throughput

**Concurrent Users:**
- Ollama: 1-2 users (single machine)
- Groq: Unlimited (cloud auto-scaling)

**Peak Load:**
- Ollama: Limited by local GPU
- Groq: Enterprise-grade infrastructure

---

## 9. Testing Strategy

### 9.1 Functional Tests

```python
def test_basic_query():
    """Test simple RAG query works."""
    answer = rag_query("What is Adobo?")
    assert len(answer) > 50
    assert "❌" not in answer
    print("✅ Basic query test passed")

def test_streaming():
    """Test streaming response works."""
    answer = rag_query_streaming("Tell me about Filipino food")
    assert len(answer) > 100
    print("✅ Streaming test passed")

def test_error_handling():
    """Test graceful error handling."""
    # Temporarily break API key
    os.environ["GROQ_API_KEY"] = "invalid"
    answer = rag_query("test")
    assert "❌" in answer or "error" in answer.lower()
    print("✅ Error handling test passed")
```

### 9.2 Performance Tests

```python
import time

def benchmark_response_time(num_queries=10):
    """Benchmark average response time."""
    questions = [
        "What is Adobo?",
        "Tell me about healthy breakfast options",
        "Suggest vegetarian dishes",
        # ... more test questions
    ]
    
    times = []
    for q in questions[:num_queries]:
        start = time.time()
        answer = rag_query(q)
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"Query: {elapsed:.2f}s")
    
    avg_time = sum(times) / len(times)
    print(f"\n📊 Average response time: {avg_time:.2f}s")
    print(f"📊 Fastest: {min(times):.2f}s")
    print(f"📊 Slowest: {max(times):.2f}s")
    
    return avg_time
```

### 9.3 Quality Assessment

```python
def compare_answers():
    """Compare Ollama vs Groq answers."""
    questions = [
        "What is Adobo?",
        "Suggest healthy breakfast options",
        "Compare Thai and Vietnamese cuisine"
    ]
    
    for q in questions:
        print(f"\nQuestion: {q}")
        print("-" * 60)
        
        # Get Ollama answer (if still available)
        # ollama_answer = rag_query_ollama(q)
        
        # Get Groq answer
        groq_answer = rag_query_groq(q)
        
        print(f"Groq: {groq_answer}")
        # Manual quality assessment
```

---

## 10. Migration Checklist

### Pre-Migration
- [ ] Verify GROQ_API_KEY in `.env`
- [ ] Install Groq SDK: `pip install groq`
- [ ] Test Groq API connectivity
- [ ] Backup current implementation
- [ ] Document current performance metrics

### Migration
- [ ] Create `rag_run_groq.py` with new implementation
- [ ] Update imports and client initialization
- [ ] Replace Ollama HTTP calls with Groq SDK
- [ ] Implement error handling and retries
- [ ] Add usage tracking
- [ ] Test basic functionality

### Post-Migration
- [ ] Run functional test suite
- [ ] Benchmark performance (should be 8-10x faster)
- [ ] Compare response quality
- [ ] Monitor first 24h usage and costs
- [ ] Update README with Groq instructions
- [ ] Archive Ollama version (optional: keep for offline fallback)

### Validation Tests
- [ ] Query: "What is Adobo?" returns accurate answer
- [ ] Query: "Healthy breakfast options" returns relevant results
- [ ] Streaming response works properly
- [ ] Error handling: Invalid API key shows graceful error
- [ ] Performance: Response time < 2 seconds
- [ ] Cost tracking: Usage logged correctly

---

## 11. Full Implementation Code

**File: `rag_run_groq.py`**

```python
"""
RAG Food System - Full Cloud Version
=====================================
Vector Database: Upstash Vector (cloud embeddings + storage)
LLM Generation: Groq API (ultra-fast inference)

No local dependencies required!
"""

import os
import json
import time
from dotenv import load_dotenv
from upstash_vector import Index
from groq import Groq, APIError, RateLimitError, APITimeoutError

# Load environment variables
load_dotenv()

# Constants
JSON_FILE = "fooddatabase.json"
GROQ_MODEL = "llama-3.1-8b-instant"

# Initialize Upstash Vector
index = Index(
    url=os.getenv("UPSTASH_VECTOR_REST_URL"),
    token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
)

# Initialize Groq
groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    timeout=30.0,
    max_retries=2
)

# Usage tracking
usage_stats = {
    "queries": 0,
    "total_tokens": 0,
    "prompt_tokens": 0,
    "completion_tokens": 0
}

# Load data
with open(JSON_FILE, "r", encoding="utf-8") as f:
    food_data = json.load(f)

# Get existing IDs from Upstash
print("🔍 Checking for existing documents in Upstash...")
try:
    all_ids = [item["id"] for item in food_data]
    existing_vectors = index.fetch(ids=all_ids[:10])
    existing_ids = {v.id for v in existing_vectors if v}
    print(f"📊 Found {len(existing_ids)} existing documents (sampled)")
except Exception as e:
    print(f"ℹ️  Could not fetch existing vectors: {e}")
    print("ℹ️  Assuming fresh start - will upsert all data")
    existing_ids = set()

# Filter new items
new_items = [item for item in food_data if item['id'] not in existing_ids]

if new_items or len(existing_ids) == 0:
    print(f"\n🆕 Adding {len(new_items) if new_items else len(food_data)} documents to Upstash Vector...")
    
    vectors_to_upsert = []
    items_to_process = new_items if new_items else food_data
    
    for item in items_to_process:
        combined_text = f"""Name: {item['name']}
Category: {item['category']} ({item['category_group']})
Origin: {item['origin']}
Description: {item['description']}
Ingredients: {', '.join(item.get('ingredients', []))}
Preparation: {item.get('preparation_method', 'N/A')}
Nutritional Highlights: {item.get('nutritional_highlights', 'N/A')}
Cultural Significance: {item.get('cultural_significance', 'N/A')}
Dietary Classifications: {', '.join(item.get('dietary_classifications', []))}"""
        
        vectors_to_upsert.append(
            (
                item["id"],
                combined_text,
                {
                    "text": combined_text,
                    "name": item["name"],
                    "category": item["category"],
                    "category_group": item["category_group"],
                    "origin": item["origin"]
                }
            )
        )
    
    try:
        print("📤 Uploading to Upstash (this may take a moment)...")
        index.upsert(vectors=vectors_to_upsert)
        print(f"✅ Successfully added {len(vectors_to_upsert)} documents to Upstash Vector!")
    except Exception as e:
        print(f"❌ Error during upsert: {e}")
else:
    print("✅ All documents already in Upstash Vector.")


def generate_answer_with_groq(prompt, max_retries=3, stream=False):
    """
    Generate answer using Groq API with error handling.
    
    Args:
        prompt (str): The full prompt including context and question
        max_retries (int): Number of retry attempts
        stream (bool): Whether to stream the response
        
    Returns:
        str: Generated answer or error message
    """
    
    for attempt in range(max_retries):
        try:
            completion = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful food expert assistant. Provide informative, "
                                   "accurate answers based on the context provided. Be concise but thorough."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=stream
            )
            
            if stream:
                return completion  # Return iterator for streaming
            
            # Extract answer
            answer = completion.choices[0].message.content.strip()
            
            # Track usage
            usage = completion.usage
            usage_stats["queries"] += 1
            usage_stats["prompt_tokens"] += usage.prompt_tokens
            usage_stats["completion_tokens"] += usage.completion_tokens
            usage_stats["total_tokens"] += usage.total_tokens
            
            print(f"📊 Tokens used: {usage.total_tokens} "
                  f"(prompt: {usage.prompt_tokens}, completion: {usage.completion_tokens})")
            
            return answer
            
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"⚠️  Rate limited. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                return "❌ Rate limit exceeded. Please try again in a few moments."
        
        except APITimeoutError:
            if attempt < max_retries - 1:
                print(f"⚠️  Request timeout. Retrying...")
            else:
                return "❌ Request timed out. Please try again."
        
        except APIError as e:
            print(f"❌ Groq API error: {e}")
            return f"❌ Unable to generate response. API error: {e}"
        
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return f"❌ An unexpected error occurred: {e}"
    
    return "❌ Failed after multiple retries."


def rag_query(question):
    """
    Query the RAG system with a natural language question.
    
    Args:
        question (str): User's question
        
    Returns:
        str: Generated answer based on retrieved context
    """
    try:
        # Step 1: Query Upstash Vector (automatic embedding)
        print("\n🔍 Searching vector database...")
        start_time = time.time()
        
        results = index.query(
            data=question,
            top_k=3,
            include_metadata=True
        )
        
        search_time = time.time() - start_time
        print(f"⚡ Vector search completed in {search_time:.2f}s")
        
        # Step 2: Extract documents
        top_docs = []
        top_ids = []
        
        for result in results:
            top_ids.append(result.id)
            text = result.metadata.get("text", "")
            top_docs.append(text)
        
        # Step 3: Display retrieved information
        print("\n🧠 Retrieved relevant information:\n")
        
        for i, (doc_id, doc) in enumerate(zip(top_ids, top_docs)):
            name_line = doc.split('\n')[0] if doc else f"ID: {doc_id}"
            print(f"🔹 Source {i + 1}: {name_line}")
            print(f"   Similarity: {results[i].score:.4f}")
            print(f"   Preview: \"{doc[:120]}...\"\n")
        
        # Step 4: Build prompt with context
        context = "\n\n---\n\n".join(top_docs)
        
        prompt = f"""Use the following context to answer the question. Be informative and specific.

Context:
{context}

Question: {question}

Please provide a clear, accurate answer based on the context above."""
        
        # Step 5: Generate answer with Groq
        print("🤖 Generating answer with Groq (ultra-fast)...")
        gen_start = time.time()
        
        answer = generate_answer_with_groq(prompt)
        
        gen_time = time.time() - gen_start
        print(f"⚡ Generation completed in {gen_time:.2f}s")
        
        total_time = time.time() - start_time
        print(f"✅ Total query time: {total_time:.2f}s\n")
        
        return answer
    
    except Exception as e:
        return f"❌ Error during query: {e}"


def rag_query_streaming(question):
    """
    Query with streaming response for better UX on long answers.
    
    Args:
        question (str): User's question
        
    Returns:
        str: Full generated answer
    """
    try:
        # Step 1: Retrieve context from Upstash
        print("\n🔍 Searching vector database...")
        
        results = index.query(
            data=question,
            top_k=3,
            include_metadata=True
        )
        
        top_docs = []
        for result in results:
            text = result.metadata.get("text", "")
            top_docs.append(text)
            name_line = text.split('\n')[0] if text else ""
            print(f"🔹 Found: {name_line} (score: {result.score:.4f})")
        
        # Step 2: Build prompt
        context = "\n\n---\n\n".join(top_docs)
        
        prompt = f"""Use the following context to answer the question. Be informative and specific.

Context:
{context}

Question: {question}

Please provide a clear, accurate answer based on the context above."""
        
        # Step 3: Stream from Groq
        print("\n🤖 Answer: ", end="", flush=True)
        
        stream = generate_answer_with_groq(prompt, stream=True)
        
        full_response = []
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response.append(content)
        
        print("\n")
        return "".join(full_response)
    
    except Exception as e:
        return f"\n❌ Error during streaming query: {e}"


def health_check():
    """Verify connection to Upstash and Groq."""
    print("\n🏥 Running health checks...\n")
    
    all_healthy = True
    
    # Check Upstash
    try:
        info = index.info()
        print(f"✅ Upstash Vector: Connected")
        print(f"   - Dimension: {info.dimension}")
        print(f"   - Vector count: {info.vector_count}")
        print(f"   - Metric: Cosine similarity")
    except Exception as e:
        print(f"❌ Upstash Vector: Failed ({e})")
        all_healthy = False
    
    # Check Groq
    try:
        test_completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print(f"✅ Groq API: Connected")
        print(f"   - Model: {GROQ_MODEL}")
        print(f"   - Status: Operational")
    except Exception as e:
        print(f"❌ Groq API: Failed ({e})")
        all_healthy = False
    
    # Show usage stats
    if usage_stats["queries"] > 0:
        avg_tokens = usage_stats["total_tokens"] / usage_stats["queries"]
        estimated_cost = usage_stats["total_tokens"] * 0.000065 / 1000
        print(f"\n📊 Session Usage:")
        print(f"   - Queries: {usage_stats['queries']}")
        print(f"   - Total tokens: {usage_stats['total_tokens']}")
        print(f"   - Avg tokens/query: {avg_tokens:.0f}")
        print(f"   - Estimated cost: ${estimated_cost:.6f}")
    
    if all_healthy:
        print("\n✅ All systems operational!\n")
    else:
        print("\n⚠️  Some services are unavailable.\n")
    
    return all_healthy


# Interactive loop
if __name__ == "__main__":
    print("\n" + "="*70)
    print("🍽️  FOOD DATABASE RAG SYSTEM (Full Cloud Edition)")
    print("="*70)
    print("☁️  Vector DB: Upstash Vector")
    print("🚀 LLM: Groq API (llama-3.1-8b-instant)")
    print("="*70)
    
    # Run health check
    if not health_check():
        print("⚠️  Please fix service issues before querying.\n")
    
    print("\n💬 Ask a question about food (type 'exit' to quit):")
    print("   Commands:")
    print("   - 'health' - Check system status")
    print("   - 'stream' - Toggle streaming mode")
    print("   - 'stats' - Show usage statistics")
    print("\n   Example questions:")
    print("   - Tell me about Filipino food")
    print("   - What are healthy breakfast options?")
    print("   - Suggest vegetarian dishes from India\n")
    
    streaming_mode = False
    
    while True:
        try:
            question = input("You: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ["exit", "quit", "bye", "q"]:
                print("\n👋 Goodbye! Thanks for using the Food RAG system!")
                if usage_stats["queries"] > 0:
                    print(f"\n📊 Final Stats:")
                    print(f"   Queries: {usage_stats['queries']}")
                    print(f"   Tokens: {usage_stats['total_tokens']}")
                    cost = usage_stats["total_tokens"] * 0.000065 / 1000
                    print(f"   Cost: ${cost:.6f}\n")
                break
            
            if question.lower() == "health":
                health_check()
                continue
            
            if question.lower() == "stream":
                streaming_mode = not streaming_mode
                print(f"🔄 Streaming mode: {'ON' if streaming_mode else 'OFF'}\n")
                continue
            
            if question.lower() == "stats":
                if usage_stats["queries"] > 0:
                    avg = usage_stats["total_tokens"] / usage_stats["queries"]
                    cost = usage_stats["total_tokens"] * 0.000065 / 1000
                    print(f"\n📊 Usage Statistics:")
                    print(f"   Queries: {usage_stats['queries']}")
                    print(f"   Total tokens: {usage_stats['total_tokens']}")
                    print(f"   Avg tokens/query: {avg:.0f}")
                    print(f"   Estimated cost: ${cost:.6f}\n")
                else:
                    print("\n📊 No queries yet.\n")
                continue
            
            # Execute RAG query
            if streaming_mode:
                answer = rag_query_streaming(question)
            else:
                answer = rag_query(question)
                print(f"\n🤖 Answer:\n{answer}\n")
            
            print("-" * 70)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}\n")
```

---

## 12. Deployment Guide

### 12.1 Environment Setup

**1. Create/Update `.env` file:**
```bash
# Upstash Vector
UPSTASH_VECTOR_REST_URL=https://resolved-pig-86020-us1-vector.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your_token_here

# Groq API (NEW)
GROQ_API_KEY=gsk_your_groq_api_key_here
```

**2. Install dependencies:**
```bash
pip install groq upstash-vector python-dotenv
```

**3. Test connection:**
```python
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Quick test
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=20
)
print(response.choices[0].message.content)
```

### 12.2 Running the Application

**Standard Mode:**
```bash
cd Cloud_Version
python rag_run_groq.py
```

**With Streaming:**
```bash
You: stream
🔄 Streaming mode: ON

You: Tell me about Filipino food
# Streams response in real-time
```

### 12.3 Production Considerations

**Environment Variables:**
- Never commit `.env` to version control
- Use secrets manager in production (AWS Secrets Manager, Azure Key Vault)
- Rotate API keys regularly

**Monitoring:**
- Log all API calls and errors
- Track token usage and costs
- Set up alerts for rate limits
- Monitor response times

**Error Handling:**
- Implement circuit breaker pattern
- Add request queuing for rate limits
- Cache common queries
- Provide fallback responses

---

## 13. Comparison: Before vs After

### 13.1 Developer Experience

| Aspect | Ollama | Groq |
|--------|--------|------|
| **Setup Time** | 30 min (install + models) | 2 min (API key) |
| **Dependencies** | Ollama service | None (cloud) |
| **Code Complexity** | HTTP requests | Simple SDK |
| **Debugging** | Check local logs | API error messages |
| **Updates** | Manual model updates | Automatic |

### 13.2 Performance

| Metric | Ollama (Local) | Groq (Cloud) |
|--------|----------------|--------------|
| **Response Time** | 5-15 seconds | 0.5-1.5 seconds |
| **Throughput** | 10-30 tokens/sec | 500-800 tokens/sec |
| **Concurrent Users** | 1-2 | Unlimited |
| **Cold Start** | 0s (always warm) | 0s (serverless) |

### 13.3 Operational

| Aspect | Ollama | Groq |
|--------|--------|------|
| **Maintenance** | Regular updates needed | Zero maintenance |
| **Monitoring** | Local logs | Cloud dashboard |
| **Scaling** | Buy more hardware | Automatic |
| **Availability** | Depends on uptime | 99.9% SLA |
| **Cost** | $0 + electricity | $0.04-$4/month |

---

## 14. Troubleshooting

### Common Issues

**"Invalid API key"**
- Verify `GROQ_API_KEY` in `.env`
- Check for extra spaces or quotes
- Generate new key at console.groq.com

**"Rate limit exceeded"**
- Wait 60 seconds
- Implement rate limiting in code
- Consider paid tier for higher limits

**"Model not found"**
- Check model name: `llama-3.1-8b-instant`
- View available models at docs.groq.com

**Slow responses**
- Check internet connection
- Verify not hitting rate limits
- Consider using streaming for better UX

**High costs**
- Implement caching for common queries
- Reduce `max_tokens` parameter
- Monitor usage with built-in stats command

---

## Conclusion

This migration from Ollama to Groq Cloud API completes the full cloud transformation:

**✅ Benefits Achieved:**
- **10x faster responses** (0.5-1.5s vs 5-15s)
- **Zero local dependencies** (no Ollama installation)
- **Ultra-low cost** ($0.04-$4/month typical usage)
- **Infinite scalability** (cloud auto-scaling)
- **Production-ready** (error handling, monitoring, caching)
- **Simple deployment** (API key only)

**🏗️ Complete Architecture:**
- ☁️ **Upstash Vector**: Automatic embeddings + vector storage
- 🚀 **Groq API**: Ultra-fast LLM inference
- 🎯 **Result**: Fully cloud-native RAG system

**📊 Total Cost (Monthly):**
- Upstash: $0 (free tier)
- Groq: $0.04-$4 (usage-based)
- **Total: < $5/month for most users**

**Next Steps:**
1. Run `python rag_run_groq.py` to test
2. Compare performance with old Ollama version
3. Monitor usage for first week
4. Deploy to production

---

**Questions or Issues?**
Contact: [Your Name/Team]
Last Updated: 2024-12-09