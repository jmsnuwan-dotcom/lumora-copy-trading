from server.services.symbol_detector import SymbolDetector
from server.services.symbol_mapper import SymbolMapper
from server.services.symbol_mapping_service import SymbolMappingService


class AutoSymbolMappingService:

    def __init__(
        self,
        mapping_service: SymbolMappingService,
    ):
        self.mapping_service = mapping_service

    def auto_map(
        self,
        connection_id: int,
        master_symbols: list[str],
    ):

        broker_symbols = SymbolDetector.get_symbols()

        for master in master_symbols:

            broker = SymbolMapper.find_best_match(
                master,
                broker_symbols,
            )

            if broker:

                self.mapping_service.create_mapping(
                    connection_id=connection_id,
                    master_symbol=master,
                    broker_symbol=broker,
                )