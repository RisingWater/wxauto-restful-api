from pydantic import BaseModel
from typing import Union, Optional

class APIResponse(BaseModel):
    success: bool
    message: str = ""
    data: Optional[Union[dict, list]] = None