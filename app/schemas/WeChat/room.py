from pydantic import (
    BaseModel,
    Field
)
from typing import (
    Dict,
    Any
)


class RoomUsageRecord(BaseModel):
    room_id: int = Field(..., description="实验室房间的编号")
    operator_name: str = Field(..., description="实验人员的真实姓名")
    room_status: str = Field(..., description="进入房间/离开房间")
    operation_type: str = Field(..., description="进入房间所进行的操作，可以分为日常/提取/培养/CNAS")
    details: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional details of the instrument operation record",
        examples=[{
            "instruments_used": {
                "96道手动手动移液工作站" : "GHJC-EQ0033",
                "东森超声波清洗机" : "GHJC-EQ0021",
                "台式离心机（右）" : "GHJC-EQ0018",
                "台式离心机（左）" : "GHJC-EQ0032",
                "生物安全柜（加样）" : "GHJC-EQ0019",
                "生物安全柜（提取）" : "GHJC-EQ0020",
                "电热恒温水浴槽" : "GHJC-EQ0024",
                "电脑" : "GHJC-EQ0029",
                "电脑显示器" : "GHJC-EQ0030",
                "移液器" : ["GHJC-YYQ0007", "GHJC-YYQ0008", "GHJC-YYQ0013", "GHJC-YYQ0014", "GHJC-YYQ0016", "GHJC-YYQ0020", "GHJC-YYQ0021","GHJC-YYQ0022", "GHJC-YYQ0023"],
                "迷你微孔板离心机（96孔板）" : "GHJC-EQ0034",
                "迷你离心机（EP管）" : "GHJC-EQ0017"
            },
            "operation_date" : "2024-09-29 17:39"
        }]
    )
