# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

import google.auth
from fastapi import FastAPI, Response
from google.adk.cli.fast_api import get_fast_api_app
from google.cloud import logging as google_cloud_logging

from app.app_utils.telemetry import setup_telemetry
from app.app_utils.typing import Feedback
from app.server import register_api_endpoints

import datetime
from google.genai.models import Models, AsyncModels

def calculate_model_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    # Google AI Studio / Vertex AI pricing per 1M tokens (context < 128k baseline)
    if "flash-lite" in model.lower():
        input_rate = 0.0375
        output_rate = 0.15
    else:
        # Default to standard gemini-3.1-flash rate
        input_rate = 0.075
        output_rate = 0.30
    return (input_tokens * input_rate + output_tokens * output_rate) / 1_000_000

original_generate_content = Models.generate_content

def patched_generate_content(self, *, model: str, contents, config=None, **kwargs):
    response = original_generate_content(self, model=model, contents=contents, config=config, **kwargs)
    try:
        usage = getattr(response, "usage_metadata", None)
        if usage:
            log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
            os.makedirs(log_dir, exist_ok=True)
            cost = calculate_model_cost(model, usage.prompt_token_count, usage.candidates_token_count)
            log_message = (
                f"[{datetime.datetime.now(datetime.UTC).isoformat()}] "
                f"MODEL USAGE: model={model} "
                f"prompt_tokens={usage.prompt_token_count} "
                f"candidates_tokens={usage.candidates_token_count} "
                f"total_tokens={usage.total_token_count} "
                f"cost_usd={cost:.8f}\n"
            )
            with open(os.path.join(log_dir, "agent.log"), "a") as f:
                f.write(log_message)
    except Exception:
        pass
    return response

Models.generate_content = patched_generate_content

original_async_generate_content = AsyncModels.generate_content

async def patched_async_generate_content(self, *, model: str, contents, config=None, **kwargs):
    response = await original_async_generate_content(self, model=model, contents=contents, config=config, **kwargs)
    try:
        usage = getattr(response, "usage_metadata", None)
        if usage:
            log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
            os.makedirs(log_dir, exist_ok=True)
            cost = calculate_model_cost(model, usage.prompt_token_count, usage.candidates_token_count)
            log_message = (
                f"[{datetime.datetime.now(datetime.UTC).isoformat()}] "
                f"MODEL USAGE: model={model} "
                f"prompt_tokens={usage.prompt_token_count} "
                f"candidates_tokens={usage.candidates_token_count} "
                f"total_tokens={usage.total_token_count} "
                f"cost_usd={cost:.8f}\n"
            )
            with open(os.path.join(log_dir, "agent.log"), "a") as f:
                f.write(log_message)
    except Exception:
        pass
    return response

AsyncModels.generate_content = patched_async_generate_content

original_async_generate_content_stream = AsyncModels.generate_content_stream

async def patched_async_generate_content_stream(self, *, model: str, contents, config=None, **kwargs):
    generator = original_async_generate_content_stream(self, model=model, contents=contents, config=config, **kwargs)
    last_response = None
    async for response in generator:
        last_response = response
        yield response
    try:
        usage = getattr(last_response, "usage_metadata", None)
        if usage:
            log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
            os.makedirs(log_dir, exist_ok=True)
            cost = calculate_model_cost(model, usage.prompt_token_count, usage.candidates_token_count)
            log_message = (
                f"[{datetime.datetime.now(datetime.UTC).isoformat()}] "
                f"MODEL USAGE: model={model} "
                f"prompt_tokens={usage.prompt_token_count} "
                f"candidates_tokens={usage.candidates_token_count} "
                f"total_tokens={usage.total_token_count} "
                f"cost_usd={cost:.8f}\n"
            )
            with open(os.path.join(log_dir, "agent.log"), "a") as f:
                f.write(log_message)
    except Exception:
        pass

AsyncModels.generate_content_stream = patched_async_generate_content_stream

# Apply global Gemini and ADK mocks during integration testing to conserve API quota
if os.getenv("INTEGRATION_TEST") == "TRUE" and os.getenv("GEMINI_LIVE_TESTING") != "true":
    from unittest.mock import patch

    # 1. Mock run_agent_sync to trigger static local fallbacks
    sync_patcher = patch(
        "app.agent.run_agent_sync",
        side_effect=Exception("Mock LLM error to trigger static fallback")
    )
    sync_patcher.start()

    # 2. Mock ADK Gemini.generate_content_async to yield mock LLM responses
    async def mock_generate_content_async(self, llm_request, stream=False):
        from google.genai import types
        import google.adk.models.google_llm as m
        content = types.Content(
            role="model",
            parts=[types.Part.from_text(text="Mocked Gemini response")]
        )
        yield m.LlmResponse(content=content)

    adk_patcher = patch(
        "google.adk.models.google_llm.Gemini.generate_content_async",
        new=mock_generate_content_async
    )
    adk_patcher.start()

    # 3. Mock google-genai generate_content for copilot chat
    class MockGenAIResponse:
        def __init__(self, text="Mocked Gemini response"):
            self.text = text

    genai_patcher = patch(
        "google.genai.models.Models.generate_content",
        return_value=MockGenAIResponse()
    )
    genai_patcher.start()

setup_telemetry()
try:
    _, project_id = google.auth.default()
    logging_client = google_cloud_logging.Client()
    logger = logging_client.logger(__name__)
    otel_to_cloud = True
except Exception as e:
    print(f"Warning: Could not initialize Google Cloud Logging client ({e}). Falling back to stdout logging.")
    class SimpleLogger:
        def log_struct(self, data, severity="INFO"):
            print(f"[{severity}] {data}")
    logger = SimpleLogger()
    otel_to_cloud = False

allow_origins = (
    os.getenv("ALLOW_ORIGINS", "").split(",") if os.getenv("ALLOW_ORIGINS") else None
)

# Artifact bucket for ADK (created by Terraform, passed via env var)
logs_bucket_name = os.environ.get("LOGS_BUCKET_NAME")

AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# In-memory session configuration - no persistent storage
session_service_uri = None

artifact_service_uri = f"gs://{logs_bucket_name}" if logs_bucket_name else None

app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=False,
    artifact_service_uri=artifact_service_uri,
    allow_origins=allow_origins,
    session_service_uri=session_service_uri,
    otel_to_cloud=otel_to_cloud,
)
app.title = "my-agent"
app.description = "API for interacting with the Agent my-agent"

register_api_endpoints(app)

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#3C3F3E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10" stroke="#3C3F3E"/>
  <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 8.88 9.88 16.24 7.76" fill="#FAF8F5" stroke="#3C3F3E"/>
  <circle cx="12" cy="12" r="1" fill="#3C3F3E"/>
</svg>"""
    return Response(content=svg_content, media_type="image/svg+xml")

@app.post("/feedback")
def collect_feedback(feedback: Feedback) -> dict[str, str]:
    """Collect and log feedback.

    Args:
        feedback: The feedback data to log

    Returns:
        Success message
    """
    try:
        logger.log_struct(feedback.model_dump(), severity="INFO")
    except Exception as e:
        print(f"Warning: Failed to log feedback to Cloud Logging: {e}")
    return {"status": "success"}


# Main execution
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
