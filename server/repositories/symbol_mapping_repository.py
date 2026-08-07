from sqlalchemy.orm import Session

from server.database.models.symbol_mapping import SymbolMapping


class SymbolMappingRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        mapping: SymbolMapping,
    ) -> SymbolMapping:
        self.db.add(mapping)
        self.db.commit()
        self.db.refresh(mapping)
        return mapping

    def get_by_connection(
        self,
        connection_id: int,
    ) -> list[SymbolMapping]:
        return (
            self.db.query(SymbolMapping)
            .filter(
                SymbolMapping.connection_id == connection_id,
            )
            .all()
        )

    def get_by_master_symbol(
        self,
        connection_id: int,
        master_symbol: str,
    ) -> SymbolMapping | None:
        return (
            self.db.query(SymbolMapping)
            .filter(
                SymbolMapping.connection_id == connection_id,
                SymbolMapping.master_symbol == master_symbol,
            )
            .first()
        )

    def update(
        self,
        mapping: SymbolMapping,
    ) -> SymbolMapping:
        self.db.commit()
        self.db.refresh(mapping)
        return mapping

    def delete(
        self,
        mapping: SymbolMapping,
    ) -> None:
        self.db.delete(mapping)
        self.db.commit()