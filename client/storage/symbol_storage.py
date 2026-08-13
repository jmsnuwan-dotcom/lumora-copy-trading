import json
from pathlib import Path


class SymbolStorage:

    @classmethod
    def _file_path(cls) -> Path:
        """
        Return a writable location for the user's symbol configuration.

        This works both when running from source and when running
        as a PyInstaller EXE.
        """

        app_data = (
            Path.home()
            / "AppData"
            / "Local"
            / "Lumora"
        )

        app_data.mkdir(
            parents=True,
            exist_ok=True,
        )

        return app_data / "symbol_config.json"

    @classmethod
    def save_gold_symbol(
        cls,
        symbol: str,
    ) -> None:

        data = {
            "gold_symbol": symbol,
        }

        cls._file_path().write_text(
            json.dumps(
                data,
                indent=4,
            ),
            encoding="utf-8",
        )

    @classmethod
    def get_gold_symbol(
        cls,
    ) -> str | None:

        file_path = cls._file_path()

        if not file_path.exists():
            return None

        try:

            data = json.loads(
                file_path.read_text(
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