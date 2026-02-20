import json
import httpx
from typing import Dict, Any, Optional
from src.config import settings
from src.logging_config import get_logger
from pydantic import BaseModel


logger = get_logger(__name__)


class DaprService:
    """
    Service for interacting with Dapr sidecar for service invocation,
    state management, and pub/sub functionality.
    """

    def __init__(self):
        self.dapr_http_endpoint = settings.dapr_http_endpoint
        self.dapr_grpc_endpoint = settings.dapr_grpc_endpoint

    async def invoke_service(
        self,
        app_id: str,
        method: str,
        data: Optional[Dict] = None,
        verb: str = "POST"
    ) -> Dict[str, Any]:
        """
        Invoke a method on another service through Dapr sidecar.

        Args:
            app_id: The ID of the target Dapr application
            method: The method to invoke on the target service
            data: Optional data to send with the request
            verb: HTTP method to use (GET, POST, PUT, DELETE, etc.)

        Returns:
            Response data from the target service
        """
        url = f"{self.dapr_http_endpoint}/v1.0/invoke/{app_id}/method/{method}"

        try:
            async with httpx.AsyncClient() as client:
                if verb.upper() == "GET":
                    response = await client.get(url)
                elif verb.upper() == "POST":
                    response = await client.post(url, json=data)
                elif verb.upper() == "PUT":
                    response = await client.put(url, json=data)
                elif verb.upper() == "DELETE":
                    response = await client.delete(url)
                else:
                    raise ValueError(f"Unsupported HTTP verb: {verb}")

            response.raise_for_status()
            return response.json() if response.content else {}

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during service invocation: {e}")
            raise
        except Exception as e:
            logger.error(f"Error invoking service {app_id}/{method}: {e}")
            raise

    async def save_state(
        self,
        store_name: str,
        key: str,
        value: Any,
        etag: Optional[str] = None
    ) -> bool:
        """
        Save state to Dapr state store.

        Args:
            store_name: Name of the state store component
            key: Key for the state value
            value: Value to store
            etag: Optional etag for concurrency control

        Returns:
            True if successful, False otherwise
        """
        url = f"{self.dapr_http_endpoint}/v1.0/state/{store_name}"

        state_item = {
            "key": key,
            "value": value
        }

        if etag:
            state_item["etag"] = etag

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=[state_item])
                response.raise_for_status()
                return True
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during state save: {e}")
            return False
        except Exception as e:
            logger.error(f"Error saving state for key {key}: {e}")
            return False

    async def get_state(
        self,
        store_name: str,
        key: str
    ) -> Any:
        """
        Get state from Dapr state store.

        Args:
            store_name: Name of the state store component
            key: Key for the state value

        Returns:
            The stored value or None if not found
        """
        url = f"{self.dapr_http_endpoint}/v1.0/state/{store_name}/{key}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    return None
                else:
                    response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during state retrieval: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting state for key {key}: {e}")
            return None

    async def publish_event(
        self,
        pubsub_name: str,
        topic_name: str,
        data: Dict[str, Any]
    ) -> bool:
        """
        Publish an event to a Dapr pub/sub topic.

        Args:
            pubsub_name: Name of the pub/sub component
            topic_name: Name of the topic to publish to
            data: Data to publish

        Returns:
            True if successful, False otherwise
        """
        url = f"{self.dapr_http_endpoint}/v1.0/publish/{pubsub_name}/{topic_name}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data)
                response.raise_for_status()
                return True
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during event publishing: {e}")
            return False
        except Exception as e:
            logger.error(f"Error publishing event to {pubsub_name}/{topic_name}: {e}")
            return False

    async def get_secret(
        self,
        store_name: str,
        key: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> Optional[str]:
        """
        Get a secret from Dapr secret store.

        Args:
            store_name: Name of the secret store component
            key: Key for the secret
            metadata: Optional metadata for the request

        Returns:
            The secret value or None if not found
        """
        url = f"{self.dapr_http_endpoint}/v1.0/secrets/{store_name}/{key}"

        if metadata:
            # Convert metadata to query parameters
            import urllib.parse
            params = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in metadata.items()])
            url += f"?{params}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                if response.status_code == 200:
                    result = response.json()
                    # Dapr returns a dictionary with the key as the secret name
                    return result.get(key)
                elif response.status_code == 404:
                    return None
                else:
                    response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during secret retrieval: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting secret {key} from {store_name}: {e}")
            return None


# Global Dapr service instance
_dapr_service: Optional[DaprService] = None


def get_dapr_service() -> DaprService:
    """Get or create a Dapr service instance."""
    global _dapr_service
    if not _dapr_service:
        _dapr_service = DaprService()
    return _dapr_service