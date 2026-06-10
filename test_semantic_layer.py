import json
import requests

# -------------------------------------------------------------
# CONFIGURATION: Replace these with your dbt Cloud details
# -------------------------------------------------------------
# Paste the exact GraphQL URL from your Project Settings -> Semantic Layer page
GRAPHQL_URL = "https://or660.semantic-layer.us1.dbt.com/api/graphql"  

# Paste your generated dbt Cloud Service Token
SERVICE_TOKEN = "dbtc_1N_ds_82x0dn6SFNKCm-6wn4GegB-v0vTSUyMdtqwOLRQmd25M"
# -------------------------------------------------------------

# Paste your exact Environment ID (Must be an integer, no quotes)
ENVIRONMENT_ID = 70506183137342
# -------------------------------------------------------------

def test_dbt_semantic_layer():
    print(f"Connecting to dbt Cloud Semantic Layer for Environment {ENVIRONMENT_ID}...")

    # 1. Set up the authorization headers
    headers = {
        "Authorization": f"Bearer {SERVICE_TOKEN}",
        "Content-Type": "application/json"
    }

    # 2. Updated GraphQL query expecting the environmentId argument
    query = """
    query GetMetrics($environmentId: BigInt!) {
      metrics(environmentId: $environmentId) {
        name
        label
        type
        description
      }
    }
    """

    # 3. Pass the environment ID as a GraphQL variable
    variables = {
        "environmentId": ENVIRONMENT_ID
    }

    # 4. Package the query and variables into the payload
    payload = {
        "query": query,
        "variables": variables
    }

    try:
        # 5. Fire the POST request
        response = requests.post(GRAPHQL_URL, json=payload, headers=headers)
        
        # 6. Handle the response codes
        if response.status_code == 200:
            response_data = response.json()
            
            # Check for GraphQL validation/execution errors
            if "errors" in response_data:
                print("\n❌ GraphQL Error returned from dbt Cloud:")
                print(json.dumps(response_data["errors"], indent=2))
                return

            metrics_list = response_data.get("data", {}).get("metrics", [])
            
            if not metrics_list:
                print("\n⚠️ Connection successful, but NO metrics were found.")
                print("Verify that your deployment job ran successfully and generated a semantic manifest.")
                return

            # 7. Success! Print the metrics found in your deployment manifest
            print(f"\n✅ Success! Connected smoothly. Discovered {len(metrics_list)} metric(s):\n")
            print(f"{'METRIC NAME':<25} | {'LABEL':<20} | {'TYPE':<10}")
            print("-" * 65)
            for metric in metrics_list:
                print(f"{metric['name']:<25} | {metric['label']:<20} | {metric['type']:<10}")
                
        elif response.status_code == 401:
            print("\n❌ Authentication Failed (401): Your Service Token is invalid or expired.")
        elif response.status_code == 404:
            print("\n❌ Endpoint Not Found (404): Please check your GRAPHQL_URL path configuration.")
        else:
            print(f"\n❌ Failed to connect. HTTP Status Code: {response.status_code}")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Network Error: Could not connect to the server.\nDetails: {e}")

if __name__ == "__main__":
    test_dbt_semantic_layer()