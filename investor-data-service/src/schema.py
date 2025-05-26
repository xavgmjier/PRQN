from pydantic import BaseModel
from typing import Any, List, Optional, Generic, TypeVar

class InvestorResponse(BaseModel):
    investor_id: str
    investor_name: str
    investory_type: str
    investor_country: str
    investor_date_added: str
    investor_last_updated: str

class CommitmentResponse(BaseModel):
    commitment_id: str
    commitment_asset_class: str
    commitment_currency: str
    commitment_amount: int

T = TypeVar("T")

class GenericPageResponse(BaseModel, Generic[T]):
    # The response for a paginated query
    page_number: int
    page_size: int
    total_pages: int
    total_records: int
    content: List[T]
    content_meta: Optional[Any] = None