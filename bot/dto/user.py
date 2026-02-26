from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    telegram_id: int
    daily_count: int
    timestamp_first_count: datetime
