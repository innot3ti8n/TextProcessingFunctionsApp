import os
from ._llm_handler import _LLMHandler
from openai import AzureOpenAI

# OpenAI client Configs
client_config = {
    "azure_endpoint": os.environ.get("AZURE_OPENAI_API_ENDPOINT"),
    "api_key": os.environ.get("AZURE_OPENAI_API_KEY"),
    "api_version": os.environ.get("AZURE_OPENAI_API_VERSION")
}

class OpenAI_GPT(_LLMHandler):
    def __init__(self):
        super().__init__(AzureOpenAI(**client_config))

    def process_text(self):
        text = self._text
        prompt_config = self._prompt_config
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
        
        # Add the user's current input text
        messages.append({"role": "user", "content": text})

        def send_prompt():
            client: AzureOpenAI = self._client
            
            response = client.chat.completions.create(
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
        
        return self.attempt_request(send_prompt)

        
