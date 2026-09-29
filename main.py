from typing import Any, List, Optional
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(
    title="Function Fusion API",
    description="功能逻辑架构多源融合接口（下游联调 Mock）",
    version="1.0.0"
)


# =========================
# 请求模型
# =========================

class FunctionPointSet(BaseModel):
    raw_text: str = ""
    function_points: List[Any] = Field(
        default_factory=list
    )
    summary: str = ""


class Relation(BaseModel):
    source: Optional[str] = None
    target: Optional[str] = None
    source_name: Optional[str] = None
    target_name: Optional[str] = None
    relation_type: Optional[str] = None
    direction: Optional[str] = None
    confidence: Optional[float] = None
    evidence: Optional[str] = None


class FusionRequest(BaseModel):
    function_point_sets: List[
        FunctionPointSet
    ] = Field(
        default_factory=list
    )

    relations: List[
        Relation
    ] = Field(
        default_factory=list
    )


# =========================
# 基础测试接口
# =========================

@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "function-fusion-api",
        "mode": "mock"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================
# 功能融合 Mock 接口
# =========================

@app.post(
    "/api/v1/function-fusion/fuse",
    status_code=200
)
def fuse_function_logic(
    request: FusionRequest
):
    """
    下游联调Mock接口。

    当前不会真正执行多源融合算法。

    无论传入什么符合FusionRequest的请求，
    都固定返回新能源汽车动力电池低电量管理场景的
    功能点及关联关系数据。
    """

    result = {
        "request_id": uuid4().hex,
        "status": "success",
        "result": {
            "function_point_set": {
                "raw_text": (
                    "新能源汽车动力电池热管理系统需要实时监测"
                    "电池包温度，并根据温度数据判断电池热状态。"
                    "当电池温度超过冷却阈值时，系统应启动冷却；"
                    "当电池温度低于加热阈值时，系统应启动加热；"
                    "当检测到电池温度异常或存在热失控风险时，"
                    "系统应向整车控制器和驾驶员发送告警信息。"
                ),
                "function_points": [
                    {
                        "id": "monitor-battery-temperature",
                        "name": "监测动力电池温度",
                        "event": {
                            "actor": "电池管理系统",
                            "action": "监测",
                            "object": "动力电池温度",
                            "effect": (
                                "获得动力电池包内部各测温点的"
                                "实时温度数据"
                            ),
                            "trigger": (
                                "车辆启动或电池管理系统"
                                "周期采样触发"
                            ),
                            "condition": (
                                "电池管理系统已上电且"
                                "温度传感器通信正常"
                            ),
                            "inputs": [
                                "车辆启动信号",
                                "电芯温度传感器数据",
                                "电池包环境温度数据"
                            ],
                            "outputs": [
                                "电池最高温度",
                                "电池最低温度",
                                "电池平均温度",
                                "电池温差"
                            ],
                            "preconditions": [
                                "电池管理系统正常运行",
                                "温度传感器已完成初始化",
                                "温度采样数据有效"
                            ],
                            "postconditions": [
                                "已获得最新的动力电池温度信息"
                            ]
                        }
                    },
                    {
                        "id": "evaluate-battery-thermal-state",
                        "name": "判断动力电池热状态",
                        "event": {
                            "actor": "电池管理系统",
                            "action": "判断",
                            "object": "动力电池热状态",
                            "effect": (
                                "确定动力电池处于正常、"
                                "过热、过冷或温度异常状态"
                            ),
                            "trigger": (
                                "获得最新的动力电池温度信息"
                            ),
                            "condition": (
                                "电池温度数据有效且热管理"
                                "阈值已经完成配置"
                            ),
                            "inputs": [
                                "电池最高温度",
                                "电池最低温度",
                                "电池平均温度",
                                "电池温差",
                                "冷却启动阈值",
                                "加热启动阈值",
                                "温度异常阈值"
                            ],
                            "outputs": [
                                "电池热状态判定结果",
                                "冷却需求",
                                "加热需求",
                                "温度异常标志"
                            ],
                            "preconditions": [
                                "已完成动力电池温度监测",
                                "热管理控制阈值有效"
                            ],
                            "postconditions": [
                                "已确定动力电池当前热状态",
                                "已生成功率热管理需求"
                            ]
                        }
                    },
                    {
                        "id": "control-battery-cooling",
                        "name": "执行动力电池冷却",
                        "event": {
                            "actor": "电池热管理控制器",
                            "action": "冷却",
                            "object": "动力电池包",
                            "effect": (
                                "降低动力电池温度并将其维持在"
                                "允许的工作温度范围内"
                            ),
                            "trigger": (
                                "电池热状态判定结果为过热，"
                                "或冷却需求有效"
                            ),
                            "condition": (
                                "电池温度高于冷却启动阈值，"
                                "且冷却系统不存在禁止运行故障"
                            ),
                            "inputs": [
                                "冷却需求",
                                "电池最高温度",
                                "电池平均温度",
                                "车辆运行状态",
                                "冷却系统状态"
                            ],
                            "outputs": [
                                "冷却控制指令",
                                "冷却液泵控制指令",
                                "冷却风扇控制指令"
                            ],
                            "preconditions": [
                                "已确认动力电池存在冷却需求",
                                "冷却液回路可用",
                                "冷却执行机构正常"
                            ],
                            "postconditions": [
                                "动力电池冷却功能已启动",
                                "电池温度开始下降或保持稳定"
                            ]
                        }
                    },
                    {
                        "id": "control-battery-heating",
                        "name": "执行动力电池加热",
                        "event": {
                            "actor": "电池热管理控制器",
                            "action": "加热",
                            "object": "动力电池包",
                            "effect": (
                                "提高动力电池温度并将其恢复到"
                                "适宜的工作温度范围"
                            ),
                            "trigger": (
                                "电池热状态判定结果为过冷，"
                                "或加热需求有效"
                            ),
                            "condition": (
                                "电池温度低于加热启动阈值，"
                                "且加热系统不存在禁止运行故障"
                            ),
                            "inputs": [
                                "加热需求",
                                "电池最低温度",
                                "电池平均温度",
                                "车辆运行状态",
                                "加热系统状态"
                            ],
                            "outputs": [
                                "加热控制指令",
                                "电池加热器控制指令"
                            ],
                            "preconditions": [
                                "已确认动力电池存在加热需求",
                                "加热装置可用",
                                "动力电池允许执行加热"
                            ],
                            "postconditions": [
                                "动力电池加热功能已启动",
                                "电池温度开始上升"
                            ]
                        }
                    },
                    {
                        "id": "report-battery-thermal-alarm",
                        "name": "上报动力电池温度异常",
                        "event": {
                            "actor": "电池管理系统",
                            "action": "上报",
                            "object": "动力电池温度异常信息",
                            "effect": (
                                "向整车控制器和驾驶员发送"
                                "电池温度异常及热风险告警"
                            ),
                            "trigger": (
                                "检测到温度超过安全阈值、"
                                "温差异常或存在热失控风险"
                            ),
                            "condition": (
                                "温度异常标志有效，或电池温度"
                                "持续超过安全阈值"
                            ),
                            "inputs": [
                                "温度异常标志",
                                "电池最高温度",
                                "电池最低温度",
                                "电池温差",
                                "电池热状态判定结果"
                            ],
                            "outputs": [
                                "动力电池温度异常告警",
                                "热失控风险告警",
                                "整车热安全控制请求"
                            ],
                            "preconditions": [
                                "已完成动力电池热状态判断",
                                "告警通信链路正常"
                            ],
                            "postconditions": [
                                "整车控制器已收到热安全告警",
                                "驾驶员已收到温度异常提示"
                            ]
                        }
                    }
                ],
                "summary": (
                    "该功能点集合描述新能源汽车动力电池热管理"
                    "系统从温度监测、热状态判断，到电池冷却、"
                    "电池加热以及温度异常告警的完整功能链路。"
                )
            },
            "relations": [
                {
                    "source": "monitor-battery-temperature",
                    "target": "evaluate-battery-thermal-state",
                    "source_name": "监测动力电池温度",
                    "target_name": "判断动力电池热状态",
                    "relation_type": "data_flow",
                    "direction": "source_to_target",
                    "confidence": 0.99,
                    "evidence": (
                        "动力电池温度监测结果是判断电池"
                        "过热、过冷及温差异常的主要输入。"
                    )
                },
                {
                    "source": "evaluate-battery-thermal-state",
                    "target": "control-battery-cooling",
                    "source_name": "判断动力电池热状态",
                    "target_name": "执行动力电池冷却",
                    "relation_type": "control_flow",
                    "direction": "source_to_target",
                    "confidence": 0.98,
                    "evidence": (
                        "当电池热状态判定为过热并产生"
                        "冷却需求时，触发动力电池冷却控制。"
                    )
                },
                {
                    "source": "evaluate-battery-thermal-state",
                    "target": "control-battery-heating",
                    "source_name": "判断动力电池热状态",
                    "target_name": "执行动力电池加热",
                    "relation_type": "control_flow",
                    "direction": "source_to_target",
                    "confidence": 0.98,
                    "evidence": (
                        "当电池热状态判定为过冷并产生"
                        "加热需求时，触发动力电池加热控制。"
                    )
                },
                {
                    "source": "evaluate-battery-thermal-state",
                    "target": "report-battery-thermal-alarm",
                    "source_name": "判断动力电池热状态",
                    "target_name": "上报动力电池温度异常",
                    "relation_type": "control_flow",
                    "direction": "source_to_target",
                    "confidence": 0.97,
                    "evidence": (
                        "电池热状态判断产生的温度异常标志"
                        "用于触发动力电池热安全告警。"
                    )
                },
                {
                    "source": "monitor-battery-temperature",
                    "target": "report-battery-thermal-alarm",
                    "source_name": "监测动力电池温度",
                    "target_name": "上报动力电池温度异常",
                    "relation_type": "data_flow",
                    "direction": "source_to_target",
                    "confidence": 0.96,
                    "evidence": (
                        "温度异常告警需要携带电池最高温度、"
                        "最低温度及电池温差等实时监测数据。"
                    )
                }
            ]
        },
        "error": None
    }

    return result