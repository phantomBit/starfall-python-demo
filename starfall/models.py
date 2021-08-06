import dataclasses
import datetime

@dataclasses.dataclass
class Widget:
    id: int
    name: str
    number: int
    createdOn: datetime.date
    updatedOn: datetime.date