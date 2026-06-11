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

def get_dbt_metadata():
    """Fetches metrics and dimensions from the dbt Semantic Layer."""
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
    """Maps user prompt to semantic layer targets, or flags conversational requests."""
    system_instruction = f"""
    You are a data assistant routing queries for a dbt Semantic Layer.
    
    Available Schema Metadata:
    {json.dumps(metadata, indent=2)}
    
    CRITICAL INSTRUCTIONS:
    1. If the user is asking a conversational question, asking how you can help, or asking what metrics are available, set the "is_conversational" key to true and write a helpful response in the "chat_response" key.
    2. If the user is asking to query data, set "is_conversational" to false, and populate "metrics" and "group_by".
    
    Respond ONLY with raw JSON matching this template. No markdown code blocks.
    {{
        "is_conversational": false,
        "chat_response": "",
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
            
    parsed = json.loads(raw_content)
    
    # Defensive fix: Make sure keys always exist even if the LLM forgets them
    if "metrics" not in parsed: parsed["metrics"] = []
    if "group_by" not in parsed: parsed["group_by"] = []
    if "is_conversational" not in parsed: parsed["is_conversational"] = False
    
    return parsed

def query_semantic_layer(api_params):
    """Executes query mapping against Snowflake via dbt."""
    print(f"\n🤖 Mapped -> Metrics: {api_params['metrics']} | Group By: {api_params['group_by']}")
    
    arrow_table = dbt_client.query(
        metrics=api_params["metrics"],
        group_by=api_params["group_by"]
    )
    return arrow_table.to_pandas()

if __name__ == "__main__":
    print("🔍 RUNNING DBT SEMANTIC LAYER DIAGNOSTICS...")
    print(f"Connecting to Host: {DBT_HOST}")
    print(f"Environment ID: {DBT_ENV_ID}")
    print(f"Token Mask: {DBT_AUTH_TOKEN[:6]}...{DBT_AUTH_TOKEN[-4:] if len(DBT_AUTH_TOKEN) > 4 else ''}")

    with dbt_client.session():
        try:
            # Test 1: Check Metadata Sync
            print("\n⏳ Testing Leg 1: Script -> dbt Cloud...")
            metrics = dbt_client.metrics()
            print(f"✅ Successful! Found {len(metrics)} metrics.")
            
            if len(metrics) > 0:
                test_metric = metrics[0].name
                print(f"📋 Selected '{test_metric}' for Snowflake compilation test.")
                
                # Test 2: Force dbt Cloud to compile the SQL without running it
                print("\n⏳ Testing Leg 2: Compilation & Snowflake Handshake...")
                
                # We use compile() instead of query() to isolate authentication from execution
                compiled_meta = dbt_client.compile(metrics=[test_metric])
                print(f"compiled:{compiled_meta}")
                print("✅ Snowflake Connection Validated successfully!")
                print("\n📊 Generated Snowflake SQL Preview:")
                print("--------------------------------------------------")
                print(compiled_meta.sql)
                print("--------------------------------------------------")

        except Exception as e:
            print("\n❌ DIAGNOSTICS FAILED!")
            print(f"Error Type: {type(e).__name__}")
            print(f"Error Message: {e}")