# RAG Food System – Customised by Dennis Bonnici

This is my enhanced version of the RAG-Food project. I added 100 food items focused on:
- Cultural cuisines from countries including Philippines, Thailand, Vietname, India, China 
- Healthy foods with detailed nutrition benefits
- Popular international dishes with cooking methods

---

## 📄 `README.md`

````markdown
# 🧠 RAG-Food: Simple Retrieval-Augmented Generation with ChromaDB + Ollama

This is a **minimal working RAG (Retrieval-Augmented Generation)** demo using:

- ✅ Local LLM via [Ollama](https://ollama.com/)
- ✅ Local embeddings via `mxbai-embed-large`
- ✅ [ChromaDB](https://www.trychroma.com/) as the vector database
- ✅ A simple food dataset in JSON (Filipino foods, fruits, etc.)

---

## 🎯 What This Does

This app allows you to ask questions like:

- “Which foods include chickpeas?”
- “What dessert is made from milk and cream?”
- “What is Halo-Halo made of and what are its main ingredients?”

It **does not rely on the LLM’s built-in memory**. Instead, it:

1. **Embeds your custom text data** (about food) using `mxbai-embed-large`
2. Stores those embeddings in **ChromaDB**
3. For any question, it:
   - Embeds your question
   - Finds relevant context via similarity search
   - Passes that context + question to a local LLM (`llama3.2`)
4. Returns a natural-language answer grounded in your data.

---

## 📦 Requirements

### ✅ Software

- Python 3.8+
- Ollama installed and running locally
- ChromaDB installed

### ✅ Ollama Models Needed

Run these in your terminal to install them:

```bash
ollama pull llama3.2
ollama pull mxbai-embed-large
````

> Make sure `ollama` is running in the background. You can test it with:
>
> ```bash
> ollama run llama3.2
> ```

---

## 🛠️ Installation & Setup

### 1. Clone or download this repo

```bash
git clone https://github.com/mrambiguous8/my_ragfood_database_wk3
cd ragfood_database_wk3/Cloud_Version
```

### 2. Create `.env` file with your Upstash credentials

```bash
UPSTASH_VECTOR_REST_URL=https://your-index.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your_token_here
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Upstash RAG app

```bash
python rag_run_upstash.py
```

On first run, it will:

* Upload all 100 food items to Upstash Vector
* Create embeddings automatically in the cloud
* Start interactive query mode

### 5. (Optional) Migrate from old ChromaDB version

If you have existing ChromaDB data:

```bash
python migrate_chroma_to_upstash.py
```

---

## 📁 File Structure

```
Cloud_Version/
├── .env                          # Upstash credentials (create this)
├── rag_run_upstash.py           # Main app (Upstash version) ⭐
├── rag_run.py                   # Legacy app (ChromaDB version)
├── migrate_chroma_to_upstash.py # Migration script
├── fooddatabase.json            # Food knowledge base (100 items)
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

### Upstash Version (rag_run_upstash.py)

1. **Data** is loaded from `fooddatabase.json`
2. Text is sent to **Upstash Vector** (automatic embedding in cloud)
3. Embeddings are stored in Upstash's serverless vector database
4. When you ask a question:
   * Question is sent to Upstash (automatic embedding)
   * Top 3 most relevant documents are retrieved
   * Context + question is passed to local `llama3.2` LLM
   * Model generates answer using retrieved context

### Key Differences from ChromaDB Version
Example Queries

Try these questions in the interactive mode:

```
You: Tell me about Filipino food
You: What are healthy breakfast options?
You: Suggest vegetarian dishes from India
You: What desserts use coconut?
You: Compare Thai and Vietnamese cuisine
```

You can also run health checks:

```
You: health
```

---
� Troubleshooting

**"Error connecting to Ollama"**
- Make sure Ollama is running: `ollama serve`
- Verify model is installed: `ollama pull llama3.2`

**"Error during upsert/query"**
- Check `.env` file has correct Upstash credentials
- Verify credentials at [Upstash Console](https://console.upstash.com/)

**"Health check failed"**
- Run the `health` command in the app for diagnostics
- Check internet connection for Upstash API

---

## 👨‍🍳 Credits

This project is based upon RAG-Food repository https://github.com/gocallum/ragfood by Callum Bir.

**Technologies used:**

* [Ollama](https://ollama.com) - Local LLM for answer generation
* [Upstash Vector](https://upstash.com/docs/vector) - Cloud vector database
* [mixedbread-ai/mxbai-embed-large-v1](https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1) - Embedding model (via Upstash)

**Enhanced by Dennis Bonnici** with 100 food items and cloud migration.

### Health Checks
Run `health` command to verify connections to Upstash and Ollama.

### Migration Support
Migrate existing ChromaDB data using the migration script:

```bash
# Dry run (preview only)
python migrate_chroma_to_upstash.py --dry-run

# Actual migration
python migrate_chroma_to_upstash.py

# Custom batch size
python migrate_chroma_to_upstash.py --batch-size 50
```

---

## 💰 Cost Considerations

**Upstash Free Tier:**
- 10,000 queries/month
- 10,000 vectors storage
- More than enough for this 100-item dataset

**This project:** $0/month (free tier sufficient)
You can update `rag_run.py` to include your own questions like:

```python
print(rag_query("What is Adobo?"))
print(rag_query("Which foods are vegetarian?"))
```

---

## 🚀 Next Ideas

* Swap in larger datasets (Wikipedia articles, recipes, PDFs)
* Add a web UI with Gradio or Flask
* Cache embeddings to avoid reprocessing on every run

---

## 👨‍🍳 Credits


This project is based upon RAG-Food repository https://github.com/gocallum/ragfood by Callum Bir using the following: 

* [Ollama](https://ollama.com)
* [ChromaDB](https://www.trychroma.com)
* [mxbai-embed-large](https://ollama.com/library/mxbai-embed-large)

