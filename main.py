from flask import Flask, render_template, request, jsonify
from openai import AzureOpenAI, OpenAI
import httpx
from config import USE_AZURE
import webbrowser
import threading

app = Flask(__name__)

# Initialize the appropriate client based on configuration
if USE_AZURE:
    from config import (
        AZURE_OPENAI_ENDPOINT,
        AZURE_OPENAI_KEY,
        AZURE_OPENAI_DEPLOYMENT,
        AZURE_OPENAI_API_VERSION
    )
    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        timeout=httpx.Timeout(60.0, connect=10.0)
    )
    MODEL = AZURE_OPENAI_DEPLOYMENT
    print("✓ Using Azure OpenAI")
else:
    from config import OPENAI_API_KEY, OPENAI_MODEL
    client = OpenAI(
        api_key=OPENAI_API_KEY,
        timeout=httpx.Timeout(60.0, connect=10.0)
    )
    MODEL = OPENAI_MODEL
    print(f"✓ Using OpenAI (ChatGPT) with model: {MODEL}")

conversation_history = [
    {"role": "system", "content": "You are a helpful AI assistant. Be concise and clear in your responses."}
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    history = data.get('history', [])
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Build conversation from client history
    conversation_history = [
        {"role": "system", "content": "You are a helpful AI assistant. Be concise and clear in your responses."}
    ]
    conversation_history.extend(history)
    conversation_history.append({"role": "user", "content": user_message})
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=conversation_history,
            max_tokens=1000,
            temperature=0.7
        )
        
        assistant_message = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": assistant_message})
        
        return jsonify({'response': assistant_message})
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error: {error_msg}")
        
        if "DeploymentNotFound" in error_msg or "404" in error_msg:
            error_msg = f"Model/Deployment '{MODEL}' not found. Check your config.py"
        elif "401" in error_msg or "Unauthorized" in error_msg:
            error_msg = "Invalid API key. Check your API key in config.py"
        elif "insufficient_quota" in error_msg:
            error_msg = "API quota exceeded. Check your OpenAI billing at platform.openai.com"
        elif "timeout" in error_msg.lower():
            error_msg = "Request timed out. Check your network connection."
            
        return jsonify({'error': error_msg}), 500


@app.route('/clear', methods=['POST'])
def clear():
    global conversation_history
    conversation_history = [
        {"role": "system", "content": "You are a helpful AI assistant. Be concise and clear in your responses."}
    ]
    return jsonify({'status': 'cleared'})


def open_browser():
    webbrowser.open('http://127.0.0.1:8080')


if __name__ == '__main__':
    threading.Timer(1.5, open_browser).start()
    app.run(debug=False, host='0.0.0.0', port=8080)
