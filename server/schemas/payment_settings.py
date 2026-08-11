from pydantic import BaseModel


class PaymentSettingsResponse(BaseModel):
    id: int

    bank_name: str
    account_name: str
    account_number: str
    branch: str
    bank_instructions: str

    crypto_currency: str
    crypto_network: str
    crypto_address: str
    crypto_instructions: str


class PaymentSettingsUpdate(BaseModel):
    bank_name: str
    account_name: str
    account_number: str
    branch: str
    bank_instructions: str

    crypto_currency: str
    crypto_network: str
    crypto_address: str
    crypto_instructions: str