import requests
import json


# Replace these with your Notion API token and database ID
NOTION_API_TOKEN = '<Enter your Notion API token>'
DATABASE_ID = '<Enter your Database ID>'


# Function to retrieve database schema from Notion
def get_notion_database_schema():
    url = f'https://api.notion.com/v1/databases/{DATABASE_ID}'
    headers = {
        "Authorization": f"Bearer {NOTION_API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching database schema: {response.status_code}, {response.text}")
    return response.json()

# Function to parse the schema data
def parse_database_schema(database_schema):
    properties = database_schema.get('properties', {})
    schema_data = {}

    for key, value in properties.items():
        value_type = value['type']
        schema_data[key] = {"type": value_type}
        
        if value_type == 'multi_select':
            schema_data[key]['options'] = [option['name'] for option in value['multi_select']['options']]
        
    return schema_data

# Function to generate extraction prompts
def generate_extraction_prompts(schema):
    prompts = []
    for field, details in schema.items():
        prompt = f"{field}: "
        if details["type"] == "checkbox":
            prompt += "[TRUE|FALSE]"
        elif details["type"] == "multi_select":
            options = ", ".join(details.get("options", []))
            prompt += f"[{options}]"
        else:
            prompt += "[Provide appropriate summary]"
        prompts.append(prompt)
    return prompts

# Main function
def main():
    database_schema = get_notion_database_schema()
    parsed_schema = parse_database_schema(database_schema)
    #print(json.dumps(parsed_schema, indent=4))
    #schema = json.dumps(parsed_schema)
    extraction_prompts = generate_extraction_prompts(parsed_schema)
    
    for prompt in extraction_prompts:
        print(prompt)

    

if __name__ == "__main__":
    main()
