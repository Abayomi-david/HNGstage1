from pydantic import BaseModel
from typing import Dict, Optional, Any, List
from datetime import datetime


class StringRequest(BaseModel):
    value: str


class StringProperties(BaseModel):
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str
    character_frequency_map: Dict[str, int]


class StringResponse(BaseModel):
    id: str
    value: str
    properties: StringProperties
    created_at: datetime


class FilterResponse(BaseModel):
    data: List[StringResponse]
    count: int
    filters_applied: Optional[Dict[str, Any]] = None


class NaturalLangResponse(BaseModel):
    data: List[StringResponse]
    count: int
    interpreted_query: Dict[str, Any]
