from src.shared.domain.entities.information_field import ImageInformationField, InformationField, MapInformationField, TextInformationField
from src.shared.domain.enums.information_field_type_enum import INFORMATION_FIELD_TYPE
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError


class InformationFieldDTO():
    information_field: InformationField

    def __init__(self, information_field: InformationField):
        self.information_field = information_field

    def from_request(information_field_dict: dict) -> "InformationFieldDTO":
        if information_field_dict.get('information_field_type') is None:
            raise MissingParameters('information_field_type')
        information_field_type = INFORMATION_FIELD_TYPE[information_field_dict.get('information_field_type')]

        information_field_dict.pop('information_field_type')

        if information_field_type == INFORMATION_FIELD_TYPE.TEXT_INFORMATION_FIELD:
            if information_field_dict.get('value') is None:
                raise MissingParameters('value')
            return InformationFieldDTO(TextInformationField(**information_field_dict))
        
        elif information_field_type == INFORMATION_FIELD_TYPE.MAP_INFORMATION_FIELD:
             if information_field_dict.get('latitude') is None:
                raise MissingParameters('latitude')
             if information_field_dict.get('longitude') is None:
                raise MissingParameters('longitude')
             return InformationFieldDTO(MapInformationField(**information_field_dict))
        
        elif information_field_type == INFORMATION_FIELD_TYPE.IMAGE_INFORMATION_FIELD:
            if information_field_dict.get('file_path') is None:
                raise MissingParameters('file_path')
            return InformationFieldDTO(ImageInformationField(**information_field_dict))
        
        else:
            raise EntityError('information_field_type')
    
    def to_entity(self) -> InformationField:
        return self.information_field
    