from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    USER = "user"


class UserStatus(StrEnum):
    ACTIVE = "active"
    DISABLED = "disabled"


class PackageName(StrEnum):
    GOLD = "Gold"
    PLATINUM = "Platinum"


class PlanType(StrEnum):
    TRIAL = "Trial"
    MONTHLY = "Monthly"
    LIFETIME = "Lifetime"


class SubscriptionStatus(StrEnum):
    ACTIVE = "active"
    EXPIRED = "expired"


class PaymentStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class SignalAction(StrEnum):
    BUY = "BUY"
    SELL = "SELL"
    CLOSE_BUY = "CLOSE_BUY"
    CLOSE_SELL = "CLOSE_SELL"


class ConnectionStatus(StrEnum):
    ONLINE = "online"
    OFFLINE = "offline"