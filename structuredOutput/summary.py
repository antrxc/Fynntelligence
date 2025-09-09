from pydantic import BaseModel
from OAIconfig.google_client import client
import requests
import time
from AgentContracts.Summary import SUMMARY_PROMPT
from tools.doclingConv import DocConvert
from google import genai


class SummaryOutput(BaseModel):
    summary: str
    insights: list[str]
    action_items: list[str]

def summaryJSON(processed_content):
    # Google GenAI expects a list of strings, not dicts with roles
    content = [
        SUMMARY_PROMPT,
        "".join(processed_content)
    ]
    start_time = time.time()
    response = client.models.generate_content(
        model="gemini-2.5-pro",  # Use a valid Google model name
        contents=content,
        config={
            "response_mime_type": "application/json",
            "response_schema": SummaryOutput,
        }
    )
    end_time = time.time()
    print(f"Generation time: {end_time - start_time:.2f} seconds")
    outputJSON = response.text
    return outputJSON

url=input("Enter URL:")
print(summaryJSON(DocConvert(url)))
