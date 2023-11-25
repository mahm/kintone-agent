from pydantic import BaseModel, Field, create_model
from typing import List, Dict, Any, Optional, Type


# Basic Field Types
class RecordNumberField(BaseModel):
    value: str


class IDField(BaseModel):
    value: str


class RevisionField(BaseModel):
    value: str


class CreatorField(BaseModel):
    value: Dict[str, str]


class CreatedTimeField(BaseModel):
    value: str


class ModifierField(BaseModel):
    value: Dict[str, str]


class UpdatedTimeField(BaseModel):
    value: str


# Custom Field Types
class SingleLineTextField(BaseModel):
    value: str


class MultiLineTextField(BaseModel):
    value: str


class RichTextField(BaseModel):
    value: str


class NumberField(BaseModel):
    value: int


class CalcField(BaseModel):
    value: str


class CheckBoxField(BaseModel):
    value: List[str]


class RadioButtonField(BaseModel):
    value: str


class MultiSelectField(BaseModel):
    value: List[str]


class DropDownField(BaseModel):
    value: str


class UserSelectField(BaseModel):
    value: List[Dict[str, str]]


class OrganizationSelectField(BaseModel):
    value: List[Dict[str, str]]


class GroupSelectField(BaseModel):
    value: List[Dict[str, str]]


class DateField(BaseModel):
    value: str


class TimeField(BaseModel):
    value: str


class DateTimeField(BaseModel):
    value: str


class LinkField(BaseModel):
    value: str


class FileField(BaseModel):
    value: List[Dict[str, Any]]


class LookupField(BaseModel):
    value: Any  # Depends on the key field type


class SubTableField(BaseModel):
    value: List[Dict[str, Any]]


class ReferenceTableField(BaseModel):
    pass  # No value field


class CategoryField(BaseModel):
    value: List[str]


class StatusField(BaseModel):
    value: str


class StatusAssigneeField(BaseModel):
    value: List[Dict[str, str]]


class LabelField(BaseModel):
    pass  # No value field


class SpacerField(BaseModel):
    pass  # No value field


class HRField(BaseModel):
    pass  # No value field


class GroupField(BaseModel):
    pass  # No value field


def kintone_field_to_model(properties: list):
    # NOTE: 編集可能なもののみ適用するようにする
    field_classes = {
        # "RECORD_NUMBER": RecordNumberField,
        # "ID": IDField,
        # "REVISION": RevisionField,
        # "CREATOR": CreatorField,
        # "CREATED_TIME": CreatedTimeField,
        # "MODIFIER": ModifierField,
        # "UPDATED_TIME": UpdatedTimeField,
        # "LABEL": LabelField,
        # "SPACER": SpacerField,
        # "HR": HRField,
        # "GROUP": GroupField,
        # "CALC": CalcField,
        "SINGLE_LINE_TEXT": SingleLineTextField,
        "MULTI_LINE_TEXT": MultiLineTextField,
        "RICH_TEXT": RichTextField,
        "NUMBER": NumberField,
        "CHECK_BOX": CheckBoxField,
        "RADIO_BUTTON": RadioButtonField,
        "MULTI_SELECT": MultiSelectField,
        "DROP_DOWN": DropDownField,
        "USER_SELECT": UserSelectField,
        "ORGANIZATION_SELECT": OrganizationSelectField,
        "GROUP_SELECT": GroupSelectField,
        "DATE": DateField,
        "TIME": TimeField,
        "DATETIME": DateTimeField,
        "LINK": LinkField,
        "FILE": FileField,
        "LOOKUP": LookupField,
        "SUBTABLE": SubTableField,
        "REFERENCE_TABLE": ReferenceTableField,
        "CATEGORY": CategoryField,
        "STATUS": StatusField,
        "STATUS_ASSIGNEE": StatusAssigneeField,
    }

    fields = {}

    for prop_info in properties:
        prop_name = prop_info["code"]
        prop_label = prop_info["label"]
        field_type = prop_info["type"]
        required = prop_info.get("required", "false") == "true"
        default_value = prop_info.get("defaultValue")
        field_class: Type[BaseModel] = field_classes.get(field_type)

        if field_class:
            if required or default_value is not None:
                fields[prop_name] = (
                    field_class,
                    Field(description=prop_label, default=default_value),
                )
            else:
                fields[prop_name] = (
                    Optional[field_class],
                    Field(description=prop_label, default=None),
                )

    return create_model("KintoneModel", **fields)
