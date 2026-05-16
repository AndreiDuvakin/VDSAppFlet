import httpx


class BaseVscaleClient:
    def __init__(self, token: str, base_url: str = "https://api.vscale.io/v1", timeout: float = 15.0):
        self._client = httpx.AsyncClient(base_url=base_url, headers={"X-Token": token}, timeout=timeout)

    async def _get(self, path: str, **kwargs):
        r = await self._client.get(path, **kwargs)
        r.raise_for_status()
        return r.json()

    async def _post(self, path: str, json=None, data=None, **kwargs):
        r = await self._client.post(path, json=json, data=data, **kwargs)
        r.raise_for_status()
        if r.status_code == 204:
            return {}

        return r.json()

    async def _put(self, path: str, json=None, data=None, **kwargs):
        r = await self._client.put(path, json=json, data=data, **kwargs)
        r.raise_for_status()
        if r.status_code == 204:
            return {}

        return r.json()

    async def _patch(self, path: str, json=None, data=None, **kwargs):
        r = await self._client.patch(path, json=json, data=data, **kwargs)
        r.raise_for_status()
        if r.status_code == 204:
            return {}

        return r.json()

    async def _delete(self, path: str, **kwargs):
        r = await self._client.delete(path, **kwargs)
        r.raise_for_status()
        if r.status_code == 204:
            return {}
        return r.json()
