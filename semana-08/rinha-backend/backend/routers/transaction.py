from fastapi import APIRouter, HTTPException
from typing import List
from models.models import Transaction, User
from schemas.schemas import TransactionSchema, TransactionCreate

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=TransactionSchema, status_code=201)
async def create_transaction(transaction: TransactionCreate):
    # Verifica se o usuário existe
    user = await User.objects.get_or_none(id=transaction.user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Cria a transação com referência ao usuário
    transaction_obj = await Transaction.objects.create(**transaction.dict())
    return transaction_obj


@router.get("/", response_model=List[TransactionSchema])
async def list_transactions():
    return await Transaction.objects.select_related("user").all()


@router.get("/{transaction_id}", response_model=TransactionSchema)
async def get_transaction(transaction_id: int):
    transaction = await Transaction.objects.select_related("user").get_or_none(id=transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.put("/{transaction_id}", response_model=TransactionSchema)
async def update_transaction(transaction_id: int, transaction_data: TransactionCreate):
    transaction = await Transaction.objects.get_or_none(id=transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Verifica se o usuário referenciado ainda existe
    user = await User.objects.get_or_none(id=transaction_data.user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await transaction.update(**transaction_data.dict())
    updated = await Transaction.objects.get(id=transaction_id)
    return updated


@router.delete("/{transaction_id}", status_code=204)
async def delete_transaction(transaction_id: int):
    transaction = await Transaction.objects.get_or_none(id=transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    await transaction.delete()
    return
