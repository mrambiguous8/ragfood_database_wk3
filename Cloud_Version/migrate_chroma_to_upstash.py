"""
Migration Script: ChromaDB to Upstash Vector
==============================================
This script migrates data from ChromaDB to Upstash Vector database.

Usage:
    python migrate_chroma_to_upstash.py [--dry-run] [--batch-size N]
    
Options:
    --dry-run       Preview migration without executing
    --batch-size N  Number of vectors to upload per batch (default: 100)
"""

import os
import json
import sys
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def migrate():
    """Main migration function."""
    print("\n" + "="*70)
    print("🔄 MIGRATION: ChromaDB → Upstash Vector")
    print("="*70 + "\n")
    
    # Parse arguments
    dry_run = "--dry-run" in sys.argv
    batch_size = 100
    
    for i, arg in enumerate(sys.argv):
        if arg == "--batch-size" and i + 1 < len(sys.argv):
            try:
                batch_size = int(sys.argv[i + 1])
            except ValueError:
                print("❌ Invalid batch size")
                return
    
    if dry_run:
        print("🔍 DRY RUN MODE - No data will be uploaded\n")
    
    # Step 1: Load ChromaDB data
    print("📂 Step 1: Loading ChromaDB data...")
    try:
        import chromadb
        chroma_client = chromadb.PersistentClient(path="chroma_db")
        collection = chroma_client.get_or_create_collection(name="foods")
        
        # Get all data from ChromaDB
        chroma_data = collection.get(include=["documents", "metadatas"])
        
        print(f"✅ Found {len(chroma_data['ids'])} documents in ChromaDB")
        print(f"   IDs: {chroma_data['ids'][:5]}... (showing first 5)")
        
    except Exception as e:
        print(f"❌ Failed to load ChromaDB: {e}")
        print("💡 Make sure ChromaDB is installed and data exists in chroma_db/")
        return
    
    # Step 2: Load food database for metadata
    print("\n📊 Step 2: Loading food database metadata...")
    try:
        with open("fooddatabase.json", "r", encoding="utf-8") as f:
            food_data = json.load(f)
        
        # Create lookup dictionary
        food_lookup = {item["id"]: item for item in food_data}
        print(f"✅ Loaded {len(food_data)} food items from JSON")
        
    except Exception as e:
        print(f"❌ Failed to load food database: {e}")
        return
    
    # Step 3: Prepare vectors for Upstash
    print("\n🔧 Step 3: Preparing vectors for Upstash...")
    vectors_to_upsert = []
    
    for i, doc_id in enumerate(chroma_data['ids']):
        # Get document text
        doc_text = chroma_data['documents'][i]
        
        # Get metadata from food database
        food_item = food_lookup.get(doc_id)
        
        if food_item:
            metadata = {
                "text": doc_text,
                "name": food_item["name"],
                "category": food_item["category"],
                "category_group": food_item["category_group"],
                "origin": food_item["origin"]
            }
        else:
            metadata = {"text": doc_text}
        
        vectors_to_upsert.append((doc_id, doc_text, metadata))
    
    print(f"✅ Prepared {len(vectors_to_upsert)} vectors")
    
    # Step 4: Connect to Upstash
    print("\n🔌 Step 4: Connecting to Upstash Vector...")
    try:
        from upstash_vector import Index
        
        index = Index(
            url=os.getenv("UPSTASH_VECTOR_REST_URL"),
            token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
        )
        
        # Test connection
        info = index.info()
        print(f"✅ Connected to Upstash Vector")
        print(f"   Dimension: {info.dimension}")
        print(f"   Current vector count: {info.vector_count}")
        
    except Exception as e:
        print(f"❌ Failed to connect to Upstash: {e}")
        print("💡 Check your .env file has correct credentials")
        return
    
    # Step 5: Upload to Upstash
    if dry_run:
        print("\n🔍 DRY RUN: Would upload the following vectors:")
        for vid, _, meta in vectors_to_upsert[:5]:
            print(f"   - ID: {vid}, Name: {meta.get('name', 'N/A')}")
        print(f"   ... and {len(vectors_to_upsert) - 5} more")
        print("\n✅ Dry run complete. Run without --dry-run to execute migration.")
        return
    
    print(f"\n📤 Step 5: Uploading to Upstash (batch size: {batch_size})...")
    
    uploaded = 0
    failed = 0
    
    # Upload in batches
    for i in range(0, len(vectors_to_upsert), batch_size):
        batch = vectors_to_upsert[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(vectors_to_upsert) + batch_size - 1) // batch_size
        
        try:
            print(f"   Batch {batch_num}/{total_batches}: Uploading {len(batch)} vectors...", end=" ")
            index.upsert(vectors=batch)
            uploaded += len(batch)
            print("✅")
            
            # Brief pause to avoid rate limits
            if i + batch_size < len(vectors_to_upsert):
                time.sleep(0.5)
                
        except Exception as e:
            print(f"❌ Failed: {e}")
            failed += len(batch)
    
    # Step 6: Validate migration
    print(f"\n✅ Step 6: Migration complete!")
    print(f"   Uploaded: {uploaded} vectors")
    print(f"   Failed: {failed} vectors")
    
    if failed == 0:
        print("\n🎉 All data migrated successfully!")
        
        # Verify count
        try:
            new_info = index.info()
            print(f"\n📊 Final Upstash vector count: {new_info.vector_count}")
        except:
            pass
    else:
        print(f"\n⚠️  Some vectors failed to migrate. Check errors above.")
    
    print("\n" + "="*70)
    print("Migration process finished")
    print("="*70 + "\n")

def validate_migration():
    """Validate that migration was successful."""
    print("\n🔍 Validating migration...\n")
    
    try:
        from upstash_vector import Index
        
        index = Index(
            url=os.getenv("UPSTASH_VECTOR_REST_URL"),
            token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
        )
        
        # Load expected IDs
        with open("fooddatabase.json", "r", encoding="utf-8") as f:
            food_data = json.load(f)
        
        expected_ids = [item["id"] for item in food_data]
        
        print(f"Expected vectors: {len(expected_ids)}")
        
        # Sample check - fetch first 10 IDs
        sample_ids = expected_ids[:10]
        results = index.fetch(ids=sample_ids)
        found = sum(1 for v in results if v is not None)
        
        print(f"Sample check (first 10): {found}/{len(sample_ids)} found")
        
        if found == len(sample_ids):
            print("\n✅ Validation passed! Data successfully migrated.")
        else:
            print(f"\n⚠️  Only {found}/{len(sample_ids)} vectors found in sample.")
            
    except Exception as e:
        print(f"❌ Validation failed: {e}")

if __name__ == "__main__":
    if "--validate" in sys.argv:
        validate_migration()
    elif "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
    else:
        migrate()
        
        # Offer validation
        if "--dry-run" not in sys.argv:
            response = input("\n🔍 Run validation check? (y/n): ").strip().lower()
            if response == 'y':
                validate_migration()
