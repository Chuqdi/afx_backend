from enum import Enum


class UserRole(Enum):
    REGULAR = "regular"
    ADMIN = "admin"


class UserGender(Enum):
    MALE = "male"
    FEMALE = "female"


class RelationshipStatus(Enum):
    SINGLE = "single"
    MARRIED = "married"
    DEVORCED = "divorced"


class AffirmationExperienceLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERIENCED = "experienced"


class AffirmationType(Enum):
    IAM = "i_am"
    YOUARE = "you_are"


class BillingFrequency(Enum):
    MONTH = "month"
    YEAR = "year"


class ActorAccent(Enum):
    AMERICAN = "american"
    BRITISH = "british"
    IRISH = "irish"
    AUSTRALIAN = "australian"
    AFRICAN = "african"
    OTHER = "other"


class DataType(Enum):
    STRING = "string"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    LIST = "list"
    DICTIONARY = "dictionary"


class SubscriptionPlan(Enum):
    BASIC = "basic"
    PREMIUM = "premium"
    PRO = "pro"


class SubscriptionType(Enum):
    MONTH = "month"
    YEAR = "year"


class TransactionType(Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class TransactionSource(Enum):
    AFFIRMATION = "affirmation"
    SUBSCRIPTION = "subscription"
    TOPUP = "top-up"


class PaymentFrequency(Enum):
    ONETIME = "one-time"
    RECURRING = "recurring"


class PaymentMethodType(Enum):
    CARD = "card"
    CRYPTO = "crypto"
