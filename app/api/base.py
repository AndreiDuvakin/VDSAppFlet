import httpx


class BaseVscaleClient:
    def __init__(self, token: str, base_url: str = "https://api.vscale.io/v1", timeout: float = 15.0):
        self._client = httpx.AsyncClient(base_url=base_url, headers={"X-Token": token}, timeout=timeout)

    async def _get(self, path: str, **kwargs):
        r = await self._client.get(path)
        r.raise_for_status()
        data = r.json()

        return data