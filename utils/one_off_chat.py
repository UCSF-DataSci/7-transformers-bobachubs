import requests
import argparse
import os

def get_response(prompt, model_name, API_KEY):
    """
    Get a response from the model
    
    Args:
        prompt: The prompt to send to the model
        model_name: Name of the model to use
        api_key: API key for authentication (optional for some models)
        
    Returns:
        The model's response
    """
    # TODO: Implement the get_response function
    # Set up the API URL and headers
    if not API_KEY:
        return "No API key provided"
    
    API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 50,
            "return_full_text": False
        }
    }   
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and "generated_text" in result[0]:
                return result[0]["generated_text"]
            if isinstance(result, dict) and "generated_text" in result:
                return result["generated_text"]
        else:
            return f"API Error ({response.status_code}): {response.text[:100]}"
    except Exception as e:
        return f"Request failed: {str(e)}"
        

    # Send the payload to the API
    # Extract and return the generated text from the response
    # Handle any errors that might occur

def run_chat(model_name, API_KEY):
    """Run an interactive chat session"""
    print("Welcome to the Simple LLM Chat! Type 'q' to quit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'q':
            print("Goodbye!")
            break
            
        # TODO: Get response from the model
        response = get_response(user_input, model_name, API_KEY)
        print(f"\nAssistant: {response}")       

def main():
    parser = argparse.ArgumentParser(description="Chat with an LLM")
    # TODO: Add arguments to the parser
        
    parser = argparse.ArgumentParser(description="Chat with an LLM")
    parser.add_argument("--model", default="HuggingFaceH4/zephyr-7b-beta", help="Model to use")
    parser.add_argument("--api-key", default=os.getenv("HUGGINGFACE_API_KEY"), help="API key (or set HUGGINGFACE_API_KEY env var)")
    args = parser.parse_args()

    # TODO: Run the chat function with parsed arguments
    run_chat(args.model, args.api_key)

if __name__ == "__main__":
    main()