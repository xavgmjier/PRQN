from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status
from typing import List
from models import Investor, Commitment
from schema import InvestorResponse, CommitmentResponse, GenericPageResponse
from database import get_db
import math

router = APIRouter(prefix="/api/v1/investors", tags=["Investors"])

@router.get("/", response_model=GenericPageResponse[InvestorResponse])
async def get_all_investors(page: int = 0, size: int = 10, db: Session = Depends(get_db)):
    investors = db.query(Investor).offset(page*size).limit(size)
    investor_record_count = db.query(Investor).count()
    available_pages = math.ceil(investor_record_count/size)

    commitment_sum_total_by_investor = db.query(Commitment.investor_id, func.sum(Commitment.commitment_amount))\
        .group_by(Commitment.investor_id).all()
    
    if investors.first() == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"could not return investors")

    meta_dict = {
        "total_commitments": dict(commitment_sum_total_by_investor)
    }

    return GenericPageResponse(
        page_number=page,
        page_size=size,
        total_pages=available_pages,
        total_records=investor_record_count,
        content=investors,
        content_meta=meta_dict
    )

@router.get("/{id}", response_model=List[InvestorResponse])
async def get_investor_by_id(id: int, db: Session = Depends(get_db)):
    investor = db.query(Investor).where(Investor.investor_id == id).first()

    if investor == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"could not return investor by ID: {id}")
    return investor

@router.get("/{id}/commitments", response_model=GenericPageResponse[CommitmentResponse])
async def get_commitments_by_investor_id(id: int, page: int = 0, size: int = 10, asset_class: str = 'all', db: Session = Depends(get_db)):

    commitment_query_all = db.query(Commitment).where(Commitment.investor_id == id)
    commitment_query_by_filter = db.query(Commitment).where(Commitment.investor_id == id, Commitment.commitment_asset_class == asset_class)

    record_count_query_for_all = db.query(Commitment.commitment_id).where(Commitment.investor_id == id)
    record_count_query_for_filter = db.query(Commitment.commitment_id).where(Commitment.investor_id == id, Commitment.commitment_asset_class == asset_class)

    investor_name = db.query(Investor.investor_name).where(Investor.investor_id == id).first()

    commitments = commitment_query_all.offset(page*size).limit(size) if asset_class == 'all' \
        else commitment_query_by_filter.offset(page*size).limit(size)
        
        
    commitment_record_count_total = record_count_query_for_all.count() if asset_class == 'all' \
        else record_count_query_for_filter.count()

    commitment_sum_total = db.query(Commitment.investor_id, func.sum(Commitment.commitment_amount))\
        .where(Commitment.investor_id == id)\
        .all()

    commitment_sum_by_asset_class = db.query(Commitment.commitment_asset_class, func.sum(Commitment.commitment_amount))\
        .where(Commitment.investor_id == id)\
        .group_by(Commitment.commitment_asset_class).all()

    commitments_tuple = [(tuple(r)) for r in commitment_sum_by_asset_class]

    if commitments.first() == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"could not return commitments for investor: {id}")

    meta_content = {
        "investor_name": investor_name[0],
        "total_commitment": commitment_sum_total[0][1],
        "total_commitments_per_asset_class" : dict(commitments_tuple)
    }

    available_pages = math.ceil(commitment_record_count_total/size)
    
    return GenericPageResponse(
        page_number=page,
        page_size=size,
        total_pages=available_pages,
        total_records=commitment_record_count_total,
        content=commitments,
        content_meta=meta_content
    )
