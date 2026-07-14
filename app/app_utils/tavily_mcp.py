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

import asyncio
import os
import threading
import logging
import time
from mcp import ClientSession
from mcp.client.sse import sse_client
from app.app_utils.rate_limiter import tavily_rate_limiter

logger = logging.getLogger(__name__)

class TavilyMCPManager:
    """Singleton manager for the Tavily remote MCP server connection."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(TavilyMCPManager, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self.thread.start()
        self.session = None
        self.client_ctx = None
        self.connect_lock = threading.Lock()

    def _run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def _async_connect(self):
        tavily_key = os.environ.get("TAVILY_API_KEY", "").strip()
        if tavily_key:
            server_url = f"https://mcp.tavily.com/mcp/?tavilyApiKey={tavily_key}"
            logger.info("Connecting to Tavily remote MCP server in KEYED mode.")
        else:
            server_url = "https://mcp.tavily.com/mcp/"
            logger.info("Connecting to Tavily remote MCP server in KEYLESS mode.")

        # Initialize the SSE client transport context
        self.client_ctx = sse_client(server_url)
        
        # Enter the context to open the connection
        read_write = await self.client_ctx.__aenter__()
        read, write = read_write
        
        # Establish the MCP client session
        self.session = ClientSession(read, write)
        await self.session.__aenter__()
        await self.session.initialize()
        logger.info("Tavily remote MCP server connection initialized successfully.")

    def connect(self):
        """Thread-safe connection logic. Connects to the remote SSE endpoint if not connected."""
        with self.connect_lock:
            if self.session is not None:
                return

            import concurrent.futures
            future = concurrent.futures.Future()

            async def do_init():
                try:
                    await self._async_connect()
                    future.set_result(True)
                except Exception as e:
                    future.set_exception(e)

            asyncio.run_coroutine_threadsafe(do_init(), self.loop)
            try:
                future.result(timeout=30)
            except Exception as e:
                self.session = None
                self.client_ctx = None
                logger.error(f"Failed to connect to Tavily MCP server: {e}")
                raise RuntimeError(f"Failed to connect to Tavily MCP server: {e}") from e

    async def _async_search(self, query: str) -> str:
        if not self.session:
            raise RuntimeError("Tavily MCP session is not connected")
        
        # Invoke the tavily-search tool
        response = await self.session.call_tool("tavily-search", arguments={"query": query})
        
        # Extract text content from the tool response structure
        text_parts = []
        if hasattr(response, "content"):
            for content_block in response.content:
                if hasattr(content_block, "text"):
                    text_parts.append(content_block.text)
                elif isinstance(content_block, dict) and "text" in content_block:
                    text_parts.append(content_block["text"])
        
        return "\n".join(text_parts)

    def search(self, query: str) -> str:
        """Performs a web search using the remote Tavily MCP server.
        
        Includes token-bucket throttling and automatic session cleanup for auto-reconnection on error.
        """
        # Consume 1 request token (block/throttle if rate limit has been hit)
        while True:
            wait_time = tavily_rate_limiter.consume(1.0)
            if wait_time <= 0.0:
                break
            logger.warning(
                f"[Rate Limiter] Tavily keyless search limit reached. "
                f"Throttling search query for {wait_time:.2f}s."
            )
            time.sleep(wait_time)

        try:
            self.connect()
            
            import concurrent.futures
            future = concurrent.futures.Future()

            async def do_search():
                try:
                    res = await self._async_search(query)
                    future.set_result(res)
                except Exception as e:
                    future.set_exception(e)

            asyncio.run_coroutine_threadsafe(do_search(), self.loop)
            return future.result(timeout=30)
        except Exception as e:
            logger.error(f"Error during Tavily search: {e}. Clearing session to force reconnection.")
            with self.connect_lock:
                self.session = None
                self.client_ctx = None
            raise e
