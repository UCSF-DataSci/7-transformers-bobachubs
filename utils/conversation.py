# utils/conversation.py

import requests
import argparse
import os

def get_response(prompt, history=None, model_name="", api_key=None, history_length=3):
    """
    Get a response from the model using conversation history
    
    Args:
        prompt: The current user prompt
        history: List of previous (prompt, response) tuples
        model_name: Name of the model to use
        api_key: API key for authentication
        history_length: Number of previous exchanges to include in context
        
    Returns:
        The model's response
    """
    # TODO: Implement the contextual response function
    # Initialize history if None
    if history is None:
        history = []
    context = history[-history_length:] if history_length > 0 else history

    # TODO: Format a prompt that includes previous exchanges
    formatted_prompt = "\n".join(
        [f"User: {user}\nAssistant: {assistant}" 
         for user, assistant in context]
    )
    if formatted_prompt:
        formatted_prompt += "\n"
    formatted_prompt += f"User: {prompt}\nAssistant:"
    
    # for user_text, assistant_text in context:
    #     formatted_prompt += f"User: {user_text}\nAssistant: {assistant_text}\n---\n"
    # formatted_prompt += f"User: {prompt}\nAssistant:"
    
    # Get a response from the API
    API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    payload = {
        "inputs": formatted_prompt,
        "parameters": {
            "max_new_tokens": 128,
            "do_sample": True,
            "return_full_text": False
        }
    }
    # Return the response
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        result = response.json()
        
        if isinstance(result, list) and "generated_text" in result[0]:
            answer = result[0]["generated_text"]
        if isinstance(result, dict) and "generated_text" in result:
            answer = result["generated_text"]


        answer = answer.split("User:")[0].split("Assistant:")[0].strip()
        answer = answer.split("---")[0].strip()
        return answer
    
    except Exception as e:
        return f"Request failed: {str(e)}"

def run_chat(model_name, api_key, history_length=3):
    """Run an interactive chat session with context"""
    print("Welcome to the Contextual LLM Chat! Type 'q' to quit.")
    
    history = []
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'q':
            print("Goodbye!")
            break
            
        # TODO: Get response using conversation history
        response = get_response(
            prompt=user_input,
            history=history,
            model_name=model_name,
            api_key=api_key,
            history_length=history_length
        )

        history.append((user_input, response))

        print(f"Assistant: {response}")

def main():
    parser = argparse.ArgumentParser(description="Chat with an LLM using conversation history")

    # TODO: Add arguments to the parser
    parser.add_argument("--model", default="HuggingFaceH4/zephyr-7b-beta", help="Model to use")
    parser.add_argument("--api-key", default=os.getenv("HUGGINGFACE_API_KEY"), help="Hugging Face API key")
    parser.add_argument("--history-length", type=int, default=3, help="Number of previous exchanges to include in context")
    args = parser.parse_args()
    
    # TODO: Run the chat function with parsed arguments
    run_chat(args.model, args.api_key, args.history_length)

if __name__ == "__main__":
    main()