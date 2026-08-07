from server.database.models.symbol_mapping import SymbolMapping
from server.repositories.symbol_mapping_repository import SymbolMappingRepository


class SymbolMappingService:

    def __init__(self, repository: SymbolMappingRepository):
        self.repository = repository

    def create_mapping(
        self,
        connection_id: int,
        master_symbol: str,
        broker_symbol: str,
    ) -> SymbolMapping:

        existing = self.repository.get_by_master_symbol(
            connection_id=connection_id,
            master_symbol=master_symbol,
        )

        if existing:
            existing.broker_symbol = broker_symbol
            return self.repository.update(existing)

        mapping = SymbolMapping(
            connection_id=connection_id,
            master_symbol=master_symbol,
            broker_symbol=broker_symbol,
        )

        return self.repository.create(mapping)

    def resolve_symbol(
        self,
        connection_id: int,
        master_symbol: str,
    ) -> str | None:

        mapping = self.repository.get_by_master_symbol(
            connection_id=connection_id,
            master_symbol=master_symbol,
        )

        if mapping is None:
            return None

        return mapping.broker_symbol

    def get_mappings(
        self,
        connection_id: int,
    ):
        return self.repository.get_by_connection(connection_id)

    def delete_mapping(
        self,
        mapping: SymbolMapping,
    ):
        self.repository.delete(mapping)