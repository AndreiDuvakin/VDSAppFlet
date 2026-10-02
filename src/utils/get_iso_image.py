from functools import cache

from src.core.constants import (
    DEBIAN_ISO_IMAGE,
    DEFAULT_ISO_IMAGE,
    FEDORA_ISO_IMAGE,
    UBUNTU_ISO_IMAGE,
)


@cache
def get_iso_image(
    iso: str,
) -> str:
    made_from = iso.lower()

    if made_from.startswith("ubuntu"):
        return UBUNTU_ISO_IMAGE

    if made_from.startswith("debian"):
        return DEBIAN_ISO_IMAGE

    if made_from.startswith("fedora"):
        return FEDORA_ISO_IMAGE

    return DEFAULT_ISO_IMAGE
