from pydantic import BaseModel
from typing import Optional

class IdentifyRequest(BaseModel):
    email: Optional[str] = None
    phoneNumber: Optional[int] = None
