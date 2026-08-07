from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.database.db import get_db
from server.database.models.connection import Connection
from server.repositories.symbol_mapping_repository import SymbolMappingRepository
from server.services.symbol_mapping_service import SymbolMappingService
from server.services.auto_symbol_mapping_service import AutoSymbolMappingService

router = APIRouter()


@router.post("/{connection_id}/auto-map")
def auto_map_symbols(
    connection_id: int,
    db: Session = Depends(get_db),
):
    repository = SymbolMappingRepository(db)
    mapping_service = SymbolMappingService(repository)
    auto_service = AutoSymbolMappingService(mapping_service)

    connection = (
        db.query(Connection)
        .filter(Connection.id == connection_id)
        .first()
    )

    if connection is None:
        return {
            "success": False,
            "message": "Connection not found",
        }

    master_symbols = [
        "XAUUSD",
        "EURUSD",
        "GBPUSD",
        "USDJPY",
        "BTCUSD",
        "ETHUSD",
    ]

    auto_service.auto_map(
        connection_id=connection_id,
        master_symbols=master_symbols,
    )

    return {
        "success": True,
        "message": "Symbol mapping completed",
    }