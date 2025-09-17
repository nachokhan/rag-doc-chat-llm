import os
import json
import logging
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_facts_from_text(text: str) -> list[dict]:
    """Extracts facts from a text using an LLM."""
    prompt = f"""
        Extract key facts from the following text.

        Return the facts as a JSON list of objects. 
        Each object must have exactly these two fields:
        - "label": the name of the fact
        - "value_text": the value of the fact

        Rules:
        - Output must be ONLY the JSON string.
        - Do NOT include explanations, comments, or code fences.
        - Do NOT use ``` or any snippet markers.
        - Do NOT prepend or append text.

        Text:
        {text}

        Response:
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts key facts from documents."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    try:
        facts = json.loads(response.choices[0].message.content)
        logging.info("Parsed successfully")
        return facts
    except (json.JSONDecodeError, IndexError):
        logging.error("Error parsing JSON response: %s", response.choices[0].message.content)
        return []
