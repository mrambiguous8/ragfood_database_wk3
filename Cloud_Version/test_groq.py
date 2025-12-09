"""
Quick test script for Groq RAG system
"""

import os
import json
import time
from dotenv import load_dotenv
from upstash_vector import Index
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize clients
index = Index(
    url=os.getenv("UPSTASH_VECTOR_REST_URL"),
    token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Test questions
test_questions = [
    "Tell me about Filipino food",
    "What are healthy breakfast options?",
    "Suggest vegetarian dishes from India"
]

print("=" * 70)
print("🧪 TESTING FULL CLOUD RAG SYSTEM")
print("=" * 70)
print("☁️  Vector DB: Upstash Vector")
print("🚀 LLM: Groq API (llama-3.1-8b-instant)")
print("=" * 70)

# Health check
print("\n🏥 Health Check...")
try:
    info = index.info()
    print(f"✅ Upstash: {info.vector_count} vectors, {info.dimension}D")
    
    test = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=10
    )
    print(f"✅ Groq: Connected and operational\n")
except Exception as e:
    print(f"❌ Health check failed: {e}\n")
    exit(1)

# Run tests
total_tokens = 0

for i, question in enumerate(test_questions, 1):
    print(f"\n{'=' * 70}")
    print(f"Test {i}/3: {question}")
    print('=' * 70)
    
    start_time = time.time()
    
    # Step 1: Retrieve from Upstash
    print("🔍 Searching Upstash Vector...")
    results = index.query(data=question, top_k=3, include_metadata=True)
    
    top_docs = []
    for result in results:
        text = result.metadata.get("text", "")
        top_docs.append(text)
        name = text.split('\n')[0] if text else f"ID: {result.id}"
        print(f"   📄 {name} (score: {result.score:.4f})")
    
    search_time = time.time() - start_time
    
    # Step 2: Generate with Groq
    context = "\n\n---\n\n".join(top_docs)
    prompt = f"""Use the following context to answer the question. Be informative and specific.

Context:
{context}

Question: {question}

Please provide a clear, accurate answer based on the context above."""
    
    print("\n🤖 Generating answer with Groq...")
    gen_start = time.time()
    
    completion = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
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
        top_p=1
    )
    
    answer = completion.choices[0].message.content.strip()
    gen_time = time.time() - gen_start
    total_time = time.time() - start_time
    
    # Display results
    print(f"\n📝 Answer:\n{answer}\n")
    
    # Metrics
    tokens = completion.usage.total_tokens
    total_tokens += tokens
    cost = tokens * 0.000065 / 1000
    
    print(f"⚡ Performance:")
    print(f"   - Search time: {search_time:.2f}s")
    print(f"   - Generation time: {gen_time:.2f}s")
    print(f"   - Total time: {total_time:.2f}s")
    print(f"   - Tokens: {tokens} (prompt: {completion.usage.prompt_tokens}, completion: {completion.usage.completion_tokens})")
    print(f"   - Cost: ${cost:.6f}")

# Summary
print(f"\n{'=' * 70}")
print("📊 TEST SUMMARY")
print('=' * 70)
print(f"Total queries: {len(test_questions)}")
print(f"Total tokens: {total_tokens}")
print(f"Avg tokens/query: {total_tokens / len(test_questions):.0f}")
print(f"Total cost: ${total_tokens * 0.000065 / 1000:.6f}")
print(f"\n✅ All tests completed successfully!")
print("=" * 70)
