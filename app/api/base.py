import httpx


class BaseVscaleClient:
    def __init__(self, token: str, base_url: str = "https://api.vscale.io/v1", timeout: float = 15.0):
        self._client = httpx.Client(base_url=base_url, headers={"X-Token": token}, timeout=timeout)

    def _get(self, path: str, **kwargs):
        r = self._client.get(path, **kwargs)
        r.raise_for_status()
        return r.json()

    def close(self):
        self._client.close()