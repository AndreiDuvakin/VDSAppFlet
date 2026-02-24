from app.api.base import BaseVscaleClient


class ServersClient(BaseVscaleClient):
    def list(self) -> list[dict]:
        return self._get("/scalets")

    def get(self, ctid: int) -> dict:
        return self._get(f"/scalets/{ctid}")