# OpenAI Configuration
# Set USE_AZURE = True for Azure OpenAI, False for regular OpenAI (ChatGPT)

USE_AZURE = True  # Toggle between Azure OpenAI and regular OpenAI

# ============ Azure OpenAI Settings ============
# Used when USE_AZURE = True
AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com/"
AZURE_OPENAI_KEY = "your-azure-openai-key-here"
AZURE_OPENAI_DEPLOYMENT = "your-deployment-name"  # Your deployment name (NOT the model name)
AZURE_OPENAI_API_VERSION = "2024-02-15-preview"

# ============ Regular OpenAI (ChatGPT) Settings ============
# Used when USE_AZURE = False
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY = "sk-your-openai-api-key-here"
OPENAI_MODEL = "gpt-4o"  # Options: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo
