from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import CurrentUser, SessionDep, get_current_superuser
from app.crud.item import crud_item
from app.schemas.item import ItemCreateRequest, ItemResponse

router = APIRouter()


@router.post("/user", status_code=status.HTTP_201_CREATED)
def create_item_for_user(
    db: SessionDep, item: ItemCreateRequest, current_user: CurrentUser
) -> ItemResponse:
    obj_in = {**item.model_dump(), "owner_id": current_user.id}
    return crud_item.create_with_owner(db, obj_in=obj_in)


@router.get("/user")
def read_items_from_user(
    db: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> list[ItemResponse]:
    return crud_item.list_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)


@router.get("/all", dependencies=[Depends(get_current_superuser)])
def read_items(db: SessionDep, skip: int = 0, limit: int = 100) -> list[ItemResponse]:
    return crud_item.list(db, skip=skip, limit=limit)


@router.get("/{item_id}")
def read_item(db: SessionDep, current_user: CurrentUser, item_id: int) -> ItemResponse:
    db_obj = crud_item.get(db, id=item_id)
    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found."
        )
    if db_obj.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="This is not your item."
        )
    return db_obj
