from dataclasses import dataclass, asdict
from typing import Dict, Optional
from datetime import datetime
import uuid


@dataclass
class LogDTO:
    level: str
    service: str
    message: str
    data: Optional[Dict[str, str]] = None
    id: Optional[str] = None
    date: Optional[str] = None

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.date is None:
            self.date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        if self.data is None:
            self.data = {}

    def to_dict(self) -> dict:
        return asdict(self)

