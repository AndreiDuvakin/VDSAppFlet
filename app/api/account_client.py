from app.api.base import BaseVscaleClient

class AccountClient(BaseVscaleClient):
    def get(self) -> dict:
        data = self._get("/account")
        return data.get("info", data)