from pydantic import BaseModel, ConfigDict


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True, validate_default=True, validate_assignment=True,
                              frozen=False, use_enum_values=True)
