from gpt_context.services import ContextService
from lib.health import (
    HealthBase,
    HealthCheckRequest,
    GoogleDriveHealthCheckRequest,
    HealthCheckResponse,
    HealthCheckResponseServingStatus
)

service_name = "gpt_context"


class HealthCheckGrpcService(HealthBase):
    def __init__(self, context_service: ContextService):
        self.context_service = context_service

    async def check(self, request: HealthCheckRequest) -> HealthCheckResponse:
        if not request.service == service_name:
            return HealthCheckResponse(status=HealthCheckResponseServingStatus.SERVICE_UNKNOWN)

        return HealthCheckResponse(status=HealthCheckResponseServingStatus.SERVING)

    async def check_google_drive(self, health_check_request: GoogleDriveHealthCheckRequest) -> HealthCheckResponse:
        try:
            healthy = self.context_service.check_google_docs_connectivity(health_check_request.folder_id)
            if not healthy:
                return HealthCheckResponse(status=HealthCheckResponseServingStatus.NOT_SERVING)

            return HealthCheckResponse(status=HealthCheckResponseServingStatus.SERVING)
        except Exception as e:
            print(f"Error checking google drive connectivity: {e}")
            return HealthCheckResponse(status=HealthCheckResponseServingStatus.NOT_SERVING)
