import os
import json
from openai import OpenAI
from dbtsl import SemanticLayerClient
import pandas as pd

# 1. Initialize Clients
DBT_ENV_ID = int(os.getenv("DBT_ENVIRONMENT_ID", "12345"))
DBT_AUTH_TOKEN = os.getenv("DBT_AUTH_TOKEN", "your_dbt_service_token")
DBT_HOST = os.getenv("DBT_HOST", "semantic-layer.cloud.getdbt.com")

ai_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
LOCAL_MODEL = "llama3" 

dbt_client = SemanticLayerClient(
    environment_id=DBT_ENV_ID,
    auth_token=DBT_AUTH_TOKEN,
    host=DBT_HOST
)

# --- REMOVED 'with dbt_client.session()' FROM INDIVIDUAL FUNCTIONS ---

def get_dbt_metadata():
    """Fetches metrics and dimensions assuming a session is already active."""
    metrics = dbt_client.metrics()
    metadata_summary = []
    for m in metrics:
        m.load_dimensions()
        dims = [d.name for d in m.dimensions]
        metadata_summary.append({
            "metric_name": m.name,
            "description": m.description,
            "available_dimensions": dims
        })
    return metadata_summary

def parse_user_prompt_local(user_prompt, metadata):
    """Maps natural language requests to semantic layer targets."""
    system_instruction = f"""
    You are a data assistant. Map the user request to these dbt structures:
    {json.dumps(metadata, indent=2)}
    
    Respond ONLY with raw JSON matching this template. No markdown code blocks.
    {{
        "metrics": ["metric_name"],
        "group_by": ["dimension_name"]
    }}
    """
    response = ai_client.chat.completions.create(
        model=LOCAL_MODEL,
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,
    )
    raw_content = response.choices[0].message.content.strip()
    if raw_content.startswith("```"):
        raw_content = raw_content.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
        if raw_content.startswith("json"):
            raw_content = raw_content[4:].strip()
    return json.loads(raw_content)

def query_semantic_layer(api_params):
    """Executes query mapping assuming a session is already active."""
    print(f"\n🤖 Local Agent Mapped -> Metrics: {api_params['metrics']} | Group By: {api_params['group_by']}")
    
    arrow_table = dbt_client.query(
        metrics=api_params["metrics"],
        group_by=api_params["group_by"]
    )
    return arrow_table.to_pandas()


# --- ONE SESSION TO RULE THEM ALL ---
if __name__ == "__main__":
    print("🔄 Opening Global dbt Semantic Layer Session...")
    
    # Keeping one persistent connection open for the entire lifecycle of the agent
    with dbt_client.session():
        try:
            semantic_metadata = get_dbt_metadata()
            print("✅ Python 3.11 Local Agent initialized successfully!")
        except Exception as e:
            print(f"❌ Failed to sync metadata from dbt Cloud: {e}")
            exit(1)
        
        while True:
            user_input = input("\n💬 Ask your data question (or type 'exit'): ")
            if user_input.lower() == 'exit':
                break
                
            if not user_input.strip():
                continue

            try:
                # 1. Parse prompt with Ollama
                parsed_query = parse_user_prompt_local(user_input, semantic_metadata)
                
                # 2. Query Snowflake through the active session
                df = query_semantic_layer(parsed_query)
                
                # 3. Print tabular results
                print("\n📊 Response Dataset:")
                if df.empty:
                    print("(No rows returned from query)")
                else:
                    print(df.to_string(index=False))
                    
            except json.JSONDecodeError:
                print("❌ Error: The local model struggled to format a clean JSON payload. Try rephrasing.")
            except Exception as e:
                print(f"❌ Execution Error: {e}")