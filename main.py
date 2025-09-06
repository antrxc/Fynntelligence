import os
import requests
import tempfile
import mimetypes
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI
from AgentContracts.PrimaryGen import PRIMARY_GEN_PROMPT

# -------------------------------
# Environment Setup
# -------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# -------------------------------
# Pydantic Models
# -------------------------------
class ChartsOutput(BaseModel):
    chart_type: str
    data: dict
    title: str
    x_axis: str
    y_axis: str
    description: str

class RecommendedPrompts(BaseModel):
    prompts: list[str]
    rationale: str
    categories: list[str]
    priority: str

class SummaryOutput(BaseModel):
    summary: str
    keydata: dict
    insights: list[str]
    action_items: list[str]

class OutputObject(BaseModel):
    summary: SummaryOutput
    recommendations: RecommendedPrompts
    charts: ChartsOutput
    filename: str
    filetype: str
    metadata: dict

# -------------------------------
# File Handling Utilities
# -------------------------------
def download_file(url: str) -> bytes:
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def get_file_extension(url: str, content: bytes) -> str:
    ext = Path(url).suffix
    if not ext:
        content_type = mimetypes.guess_type(url)[0]
        if content_type:
            ext = mimetypes.guess_extension(content_type)
    return ext.lower() if ext else ""

def process_file(content: bytes, extension: str) -> str:
    # Downloaded file is saved first, then parsed by tools.parse_file_by_type
    with tempfile.NamedTemporaryFile(suffix=extension, delete=False, mode='wb') as tmp_file:
        tmp_file.write(content)
        tmp_file.flush()
        from tools import parse_file_by_type
        if extension in {".jpg", ".jpeg", ".png", ".gif"}:
            return "Image file detected - content analysis not implemented"
        return parse_file_by_type(tmp_file.name, extension)

# -------------------------------
# Main Execution
# -------------------------------
def main(URL)
    url = URL
    file_content = download_file(url)
    extension = get_file_extension(url, file_content)
    processed_content = process_file(file_content, extension)

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": PRIMARY_GEN_PROMPT},
            {"role": "user", "content": f"Analyze this content:\n\n{processed_content}"}
        ],
        
    )

    outputJSON = response.choices[0].message.content
    return outputJSON

inputURL = input("Enter URL: ")
main(inputURL)
