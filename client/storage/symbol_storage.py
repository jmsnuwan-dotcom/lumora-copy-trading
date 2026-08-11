import json
from pathlib import Path


class SymbolStorage:

    FILE_PATH = (
        Path(__file__).resolve().parent
        / "symbol_config.json"
    )

    @classmethod
    def save_gold_symbol(
        cls,
        symbol: str,
    ) -> None:

        data = {
            "gold_symbol": symbol,
        }

        cls.FILE_PATH.write_text(
            json.dumps(data, indent=4),
            encoding="utf-8",
        )

    @classmethod
    def get_gold_symbol(
        cls,
    ) -> str | None:

        if not cls.FILE_PATH.exists():
            return None

        try:
            data = json.loads(
                cls.FILE_PATH.read_text(
                    encoding="utf-8",
                )
            )

            return data.get(
                "gold_symbol"
            )

        except (
            OSError,
            json.JSONDecodeError,
        ):
            return None
        