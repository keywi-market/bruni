from enum import Enum
from typing import Literal

from pydantic import BaseModel


class Location(BaseModel):
    url: str
