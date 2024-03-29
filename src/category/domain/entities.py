from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, Union
from __seedwork.domain.entities import Entity
from __seedwork.domain.validators import ValidatorRules

# pylint: disable=unnecessary-lambda


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(Entity):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now()
    )

    def __new__(cls, **kwargs): # python`s constructor
        cls.validate(name=kwargs.get("name"),
                     description=kwargs.get("description"),
                     is_active=kwargs.get("is_active"))
        return super(Category, cls).__new__(cls)

    def update(self, name: str, description: Union[None, str]) -> None:
        self.validate(name, description)
        self._set("name", name)
        self._set("description", description)

    def activate(self) -> None:
        self._set("is_active", True)

    def deactivate(self) -> None:
        self._set("is_active", False)

    @classmethod
    def validate(cls, name: str, description: str, is_active: bool = None) -> None:
        ValidatorRules.values(name, "name").required().string().max_length(255)
        ValidatorRules.values(description, "description").string()
        ValidatorRules.values(is_active, "is_active").boolean()
