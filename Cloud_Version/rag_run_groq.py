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
