import dataclasses
import datetime
import typing

WIDGET_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer", "minimum": 0},
        "number": {"type": "integer", "minimum": 0},
        "name": {"type": "string", "minLength": 1, "maxLength": 64},
    },
    "required": ["number", "name"]
}

WIDGET_SCHEMA_POST = {
    "required": ["number", "name", "id"]
}


@dataclasses.dataclass
class Widget:
    name: str
    number: int
    id: typing.Optional[int] = None
    createdOn: typing.Optional[datetime.date] = None
    updatedOn: typing.Optional[datetime.date] = None


def widget_to_json(widget=Widget) -> object:
    return {
        "id": widget.id,
        "name": widget.name,
        "number": widget.number,
        "created_on": widget.createdOn,
        "updated_on": widget.updatedOn,
    }
