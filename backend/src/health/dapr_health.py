import httpx
from typing import Dict, Any, Optional
from src.config import settings
from src.logging_config import get_logger
import asyncio


logger = get_logger(__name__)


class DaprHealthCheck:
    """Health check service for Dapr sidecars"""

    def __init__(self):
        self.dapr_http_endpoint = settings.dapr_http_endpoint
        self.dapr_grpc_endpoint = settings.dapr_grpc_endpoint

    async def check_dapr_health(self) -> Dict[str, Any]:
        """Check the health of the Dapr sidecar."""
        health_status = {
            "dapr_sidecar": {
                "http_endpoint": self.dapr_http_endpoint,
                "grpc_endpoint": self.dapr_grpc_endpoint,
                "http_reachable": False,
                "grpc_reachable": False,
                "components_loaded": [],
                "errors": []
            }
        }

        # Check HTTP endpoint
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.dapr_http_endpoint}/v1.0/healthz")
                health_status["dapr_sidecar"]["http_reachable"] = response.status_code == 204
        except Exception as e:
            health_status["dapr_sidecar"]["errors"].append(f"HTTP endpoint error: {str(e)}")

        # Check components
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.dapr_http_endpoint}/v1.0/components")
                if response.status_code == 200:
                    components = response.json()
                    health_status["dapr_sidecar"]["components_loaded"] = [
                        comp.get("name") for comp in components
                    ] if isinstance(components, list) else []
        except Exception as e:
            health_status["dapr_sidecar"]["errors"].append(f"Components check error: {str(e)}")

        # Overall health status
        health_status["dapr_sidecar"]["overall_healthy"] = (
            health_status["dapr_sidecar"]["http_reachable"] and
            len(health_status["dapr_sidecar"]["errors"]) == 0
        )

        return health_status

    async def check_dapr_service_invocation(self, app_id: str, method: str = "health") -> Dict[str, Any]:
        """Check if Dapr service invocation is working."""
        try:
            invocation_url = f"{self.dapr_http_endpoint}/v1.0/invoke/{app_id}/method/{method}"

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(invocation_url)

            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "message": f"Service invocation to {app_id}/{method} successful" if response.status_code == 200 else f"Service invocation failed with status {response.status_code}",
                "response": response.text[:500] if response.text else None  # Limit response size
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Service invocation to {app_id}/{method} failed"
            }

    async def check_dapr_pubsub(self, pubsub_name: str) -> Dict[str, Any]:
        """Check if Dapr pub/sub is working by attempting to publish a test message."""
        try:
            publish_url = f"{self.dapr_http_endpoint}/v1.0/publish/{pubsub_name}/test-topic"

            test_message = {
                "message": "health_check",
                "timestamp": "test",
                "source": "health_check"
            }

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(publish_url, json=test_message)

            return {
                "success": response.status_code in [200, 204],
                "status_code": response.status_code,
                "message": f"Pub/sub publish to {pubsub_name} successful" if response.status_code in [200, 204] else f"Pub/sub publish failed with status {response.status_code}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Pub/sub publish to {pubsub_name} failed"
            }

    async def comprehensive_health_check(self) -> Dict[str, Any]:
        """Perform a comprehensive health check of all Dapr components."""
        health_results = {
            "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
            "checks": {}
        }

        # Check Dapr sidecar health
        health_results["checks"]["dapr_health"] = await self.check_dapr_health()

        # Check if we can reach our own service through Dapr (self-check)
        try:
            self_check_url = f"{self.dapr_http_endpoint}/v1.0/invoke/todo-backend/method/health"
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(self_check_url)
            health_results["checks"]["self_service_invocation"] = {
                "success": response.status_code == 200,
                "status_code": response.status_code
            }
        except Exception as e:
            health_results["checks"]["self_service_invocation"] = {
                "success": False,
                "error": str(e)
            }

        # Overall health
        all_checks = health_results["checks"]
        health_results["overall_healthy"] = all(
            check.get("overall_healthy", check.get("success", False))
            for check in all_checks.values()
            if isinstance(check, dict) and "overall_healthy" in check or "success" in check
        )

        return health_results


# Global instance
dapr_health_checker = DaprHealthCheck()


async def get_dapr_health_status() -> Dict[str, Any]:
    """Get the current health status of Dapr components."""
    return await dapr_health_checker.comprehensive_health_check()