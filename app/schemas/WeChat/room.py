from pydantic import (
    BaseModel,
    Field
)
from datetime import datetime
from typing import (
    Dict,
    Any
)


class RoomUsageRecord(BaseModel):
    room_id: int = Field(..., description="实验室房间的编号")
    operator_name: str = Field(..., description="实验人员的真实姓名")
    room_status: str = Field(..., description="进入房间/离开房间")
    operation_type: str = Field(..., description="进入房间所进行的操作，可以分为日常操作/流程操作/CNAS")
    details: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional details of the instrument operation record",
        examples=[{
            "instrument_number": ["SN001", "SN002"],
            "slot_type": "A",
            "chip_sequence": "ATCG...",
            "is_sequencing": True,
            "operation_type": "Standard Sequencing",
            "operation_reason": "Routine analysis",
            "operation_date": "2024-09-11 14:30",
            "remarks": "Proceeded without issues"
        }]
    )
