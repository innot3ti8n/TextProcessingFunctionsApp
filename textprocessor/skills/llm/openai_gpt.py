import os, logging, time, pprint
from openai import AzureOpenAI

# Set up the OpenAI client
openai_client = AzureOpenAI(
    azure_endpoint=os.environ.get("AZURE_API_ENDPOINT"),
    api_key=os.environ.get("AZURE_API_KEY"),
    api_version="2024-02-15-preview"
)

# Function to generate a response using the prompt configuration
import json
import logging

def process_text(text, prompt_config, retries=3, delay=2):
    print(f"Sending prompts... Max tokens allowed: {prompt_config['chatParameters']['maxResponseLength']}")

    # Clear messages to avoid residuals from previous calls
    messages = []
    
    # Add the system prompt and text
    messages.append({"role": "system", "content": prompt_config["systemPrompt"]})
    
    # Check if few-shot examples are relevant for this prompt
    if "fewShotExamples" in prompt_config and prompt_config["fewShotExamples"]:
        for example in prompt_config["fewShotExamples"]:
            messages.append({"role": "user", "content": example["userInput"]})
            messages.append({"role": "assistant", "content": example["chatbotResponse"]})
    
    messages.append({"role": "user", "content": text})

    for attempt in range(retries):
        try:
            response = openai_client.chat.completions.create(
                model=prompt_config["chatParameters"]["deploymentName"],
                messages=messages,
                max_tokens=3500,
                temperature=prompt_config["chatParameters"]["temperature"],
                top_p=prompt_config["chatParameters"]["topProbablities"],
                stop=prompt_config["chatParameters"]["stopSequences"],
                frequency_penalty=prompt_config["chatParameters"]["frequencyPenalty"],
                presence_penalty=prompt_config["chatParameters"]["presencePenalty"],
            )

            content = response.choices[0].message.content

            return content

        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            return "Error: Invalid JSON in prompt configuration."

        except KeyError as e:
            logging.error(f"Missing key in prompt configuration: {e}")
            return f"Error: Missing key in prompt configuration: {e}"

        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return "Error: An unexpected error occurred after multiple attempts."
