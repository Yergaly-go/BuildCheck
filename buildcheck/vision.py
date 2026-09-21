from enum import StrEnum


class VisionCapability(StrEnum):
    UNAVAILABLE = "UNAVAILABLE"


class VisionAdapter:
    """Provider-neutral boundary; F001 intentionally has no provider or image inference."""

    capability = VisionCapability.UNAVAILABLE

    def describe_availability(self) -> VisionCapability:
        return self.capability
