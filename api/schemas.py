from pydantic import BaseModel, ConfigDict, Field, field_validator


class ChatRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True
    )

    query: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )

    @field_validator("query")
    @classmethod
    def validate_query(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Query cannot be empty")

        return value