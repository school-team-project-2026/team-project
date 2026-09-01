from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.interest_item import InterestItem
from app.schemas.interest_item import InterestItemCreate, InterestItemRead

router = APIRouter(
    prefix="/interest-items",
    tags=["interest-items"],
)

DbSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=InterestItemRead,
    status_code=status.HTTP_201_CREATED,
)
def create_interest_item(
    payload: InterestItemCreate,
    session: DbSession,
) -> InterestItem:
    item = InterestItem(
        name=payload.name,
        category=payload.category,
        comment=payload.comment,
    )

    session.add(item)
    session.commit()
    session.refresh(item)

    return item


@router.get(
    "",
    response_model=list[InterestItemRead],
)
def list_interest_items(
    session: DbSession,
) -> list[InterestItem]:
    statement = select(InterestItem).order_by(InterestItem.created_at.desc())

    items = session.scalars(statement).all()

    return list(items)
