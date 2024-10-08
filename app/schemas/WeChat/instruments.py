from pydantic import (
    BaseModel,
    Field
)
from typing import (
    Dict,
    Any,
)


class InstrumentUsageRecord(BaseModel):
    instrument_code: str
    instrument: str = Field(
        ...,
        description="The name or model of the instrument used",
        examples=["sequencing"]
    )
    instrument_status: str = Field(
        ...,
        description="The current status of the instrument (e.g., '正常', '异常')",
        examples=["异常"]
    )
    operator_name: str = Field(
        ...,
        description="The name of the operator conducting the instrument",
        min_length=2,
        max_length=100,
        examples=["牛博"]
    )

    details: Dict[str, Any] = Field(
        ...,
        description="仪器使用表单的详细记录"
    )
