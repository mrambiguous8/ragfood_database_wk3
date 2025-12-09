import os
import json
import requests
from dotenv import load_dotenv
from upstash_vector import Index

# Load environment variables
load_dotenv()

# Constants
JSON_FILE = "fooddatabase.json"
LLM_MODEL = "llama3.2"

# Initialize Upstash Vector
index = Index(
    url=os.getenv("UPSTASH_VECTOR_REST_URL"),
    token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
)

# Load data
with open(JSON_FILE, "r", encoding="utf-8") as f:
    food_data = json.load(f)

# Get existing IDs from Upstash
print("🔍 Checking for existing documents in Upstash...")
try:
    # Try to fetch all IDs to check what exists
    all_ids = [item["id"] for item in food_data]
    existing_vectors = index.fetch(ids=all_ids[:10])  # Sample first 10 to check
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
    
    # Prepare batch upsert
    vectors_to_upsert = []
    
    items_to_process = new_items if new_items else food_data
    
    for item in items_to_process:
        # Combine fields for rich context
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
                combined_text,  # Upstash will embed this automatically
                {
                    "text": combined_text,
                    "name": item["name"],
                    "category": item["category"],
                    "category_group": item["category_group"],
                    "origin": item["origin"]
                }
            )
        )
    
    # Batch upsert (more efficient)
    try:
        print("📤 Uploading to Upstash (this may take a moment)...")
        index.upsert(vectors=vectors_to_upsert)
        print(f"✅ Successfully added {len(vectors_to_upsert)} documents to Upstash Vector!")
    except Exception as e:
        print(f"❌ Error during upsert: {e}")
        print("💡 Tip: Check your .env file has correct UPSTASH credentials")
else:
    print("✅ All documents already in Upstash Vector.")

# RAG query function
def rag_query(question):
    """
    Query the RAG system with a natural language question.
    
    Args:
        question (str): User's question
        
    Returns:
        str: Generated answer based on retrieved context
    """
    try:
        # Step 1: Query Upstash (automatic embedding)
        print("\n🔍 Searching vector database...")
        results = index.query(
            data=question,
            top_k=3,
            include_metadata=True
        )
        
        # Step 2: Extract documents
        top_docs = []
        top_ids = []
        
        for result in results:
            top_ids.append(result.id)
            # Get text from metadata
            text = result.metadata.get("text", "")
            top_docs.append(text)
        
        # Step 3: Display retrieved information
        print("\n🧠 Retrieving relevant information to reason through your question...\n")
        
        for i, (doc_id, doc) in enumerate(zip(top_ids, top_docs)):
            # Extract just the name for cleaner display
            name_line = doc.split('\n')[0] if doc else f"ID: {doc_id}"
            print(f"🔹 Source {i + 1}: {name_line}")
            print(f"   Score: {results[i].score:.4f}")
            print(f"   Preview: \"{doc[:150]}...\"\n")
        
        print("📚 These are the most relevant pieces of information.\n")
        
        # Step 4: Build prompt
        context = "\n\n---\n\n".join(top_docs)
        
        prompt = f"""Use the following context to answer the question. Be informative and specific.

Context:
{context}

Question: {question}
Answer:"""
        
        # Step 5: Generate answer with Ollama
        print("🤖 Generating answer with LLM...")
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=60)
        
        if response.status_code == 200:
            return response.json()["response"].strip()
        else:
            return f"❌ LLM API error: {response.status_code}"
    
    except requests.exceptions.RequestException as e:
        return f"❌ Error connecting to Ollama: {e}\n💡 Make sure Ollama is running (ollama serve)"
    except Exception as e:
        return f"❌ Error during query: {e}"

# Health check
def health_check():
    """Verify connection to Upstash and Ollama."""
    print("\n🏥 Running health checks...\n")
    
    # Check Upstash
    try:
        info = index.info()
        print(f"✅ Upstash Vector: Connected")
        print(f"   - Dimension: {info.dimension}")
        print(f"   - Vector count: {info.vector_count}")
    except Exception as e:
        print(f"❌ Upstash Vector: Failed ({e})")
        return False
    
    # Check Ollama
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print(f"✅ Ollama LLM: Connected")
            models = [m["name"] for m in response.json().get("models", [])]
            if LLM_MODEL in models:
                print(f"   - Model '{LLM_MODEL}' available")
            else:
                print(f"⚠️  Model '{LLM_MODEL}' not found. Available: {models[:3]}")
        else:
            print(f"❌ Ollama LLM: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama LLM: Failed ({e})")
        return False
    
    print("\n✅ All systems operational!\n")
    return True

# Interactive loop
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🍽️  FOOD DATABASE RAG SYSTEM (Upstash Vector Edition)")
    print("="*60)
    
    # Run health check
    if not health_check():
        print("\n⚠️  Some services are unavailable. Please fix before querying.\n")
    
    print("\n💬 Ask a question about food (type 'exit' to quit):")
    print("   Examples:")
    print("   - Tell me about Filipino food")
    print("   - What are healthy breakfast options?")
    print("   - Suggest vegetarian dishes from India\n")
    
    while True:
        try:
            question = input("You: ").strip()
            
            if not question:
                continue
                
            if question.lower() in ["exit", "quit", "bye", "q"]:
                print("\n👋 Goodbye! Thanks for using the Food RAG system!\n")
                break
            
            if question.lower() == "health":
                health_check()
                continue
            
            # Execute RAG query
            answer = rag_query(question)
            print(f"\n🤖 Answer:\n{answer}\n")
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}\n")
