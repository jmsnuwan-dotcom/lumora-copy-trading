from client.mt5.mt5_client import MT5Client
from client.mt5.symbol_loader import SymbolLoader
from client.mt5.symbol_resolver import SymbolResolver

if not MT5Client.connect():
    print("MT5 Connection Failed")
    exit()

symbols = SymbolLoader.get_symbols()

print(f"Total Symbols : {len(symbols)}")

result = SymbolResolver.resolve(
    "XAUUSD",
    symbols,
)

print("Detected :", result)

MT5Client.shutdown()