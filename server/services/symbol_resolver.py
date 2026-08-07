from server.services.symbol_mapping_service import SymbolMappingService


class SymbolResolver:

    def __init__(
        self,
        mapping_service: SymbolMappingService,
    ):
        self.mapping_service = mapping_service

    def resolve(
        self,
        connection_id: int,
        master_symbol: str,
    ) -> str:
        """
        Resolve canonical symbol to broker symbol.
        Falls back to the master symbol if no mapping exists.
        """

        broker_symbol = self.mapping_service.resolve_symbol(
            connection_id=connection_id,
            master_symbol=master_symbol,
        )

        if broker_symbol:
            return broker_symbol

        return master_symbol