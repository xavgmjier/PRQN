from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status
from typing import List
from models import Commitment
from schema import CommitmentResponse, GenericPageResponse
from database import get_db
import math

router = APIRouter(prefix="/api/v1/commitments", tags=["Commitments"])

@router.get("/", response_model=GenericPageResponse[CommitmentResponse])
async def get_all_commitments(page: int = 0, size: int = 10, db: Session = Depends(get_db)):
    all_commitments = db.query(Commitment).offset(page*size).limit(size)
    commitment_record_count = db.query(Commitment.commitment_id).count()

    available_pages = math.ceil(commitment_record_count/size)

    if all_commitments.first() == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"could not return commitments")

    return GenericPageResponse(
        page_number=page,
        page_size=size,
        total_pages=available_pages,
        total_records=commitment_record_count,
        content=all_commitments
    )

@router.get("/{id}", response_model=List[CommitmentResponse])
async def get_commitment_by_id(id: str, db: Session = Depends(get_db)):
    commitment = db.query(Commitment).where(Commitment.commitment_id == id)

    if commitment.first() == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"could not return commitment by ID: {id}")
    
    return commitment
