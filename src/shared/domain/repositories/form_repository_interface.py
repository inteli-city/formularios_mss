from abc import ABC, abstractmethod
from typing import List, Optional

from src.shared.domain.entities.form import Form
from src.shared.domain.entities.justification import Justification
from src.shared.domain.entities.section import Section
from src.shared.domain.enums.form_status_enum import FORM_STATUS


class IFormRepository(ABC):

    @abstractmethod
    def get_form_by_id(self, user_id:str, form_id: str) -> Form:
        pass
    
    @abstractmethod
    def get_form_by_user_id(self, user_id: str) -> List[Form]:
        pass

    @abstractmethod
    def create_form(self, form: Form) -> Form:
        pass

    @abstractmethod
    def update_form_status(self, user_id: str, form_id: str, status: FORM_STATUS, start_date: Optional[int] = None) -> Form:
        pass

    @abstractmethod
    def cancel_form(self, user_id: str, form_id: str, justification: Justification) -> Form:
        pass

    @abstractmethod
    def complete_form(self, user_id: str, form_id: str, sections: List[Section], vinculation_form_id: Optional[str] = None) -> Form:
        pass