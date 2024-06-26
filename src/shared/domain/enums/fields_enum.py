from enum import Enum


class FIELD_TYPE(Enum):
    TEXT_FIELD = 'TEXT_FIELD'
    NUMBER_FIELD = 'NUMBER_FIELD'
    DROPDOWN_FIELD = 'DROPDOWN_FIELD'
    TYPEAHEAD_FIELD = 'TYPEAHEAD_FIELD'
    RADIO_GROUP_FIELD = 'RADIO_GROUP_FIELD'
    DATE_FIELD = 'DATE_FIELD'
    CHECKBOX_FIELD = 'CHECKBOX_FIELD'
    CHECKBOX_GROUP_FIELD = 'CHECKBOX_GROUP_FIELD'
    SWITCH_BUTTON_FIELD = 'SWITCH_BUTTON_FIELD'
    FILE_FIELD = 'FILE_FIELD'