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
                    "新能源汽车动力电池管理系统需要实时检测"
                    "动力电池剩余电量。当系统检测到剩余电量"
                    "低于20%时，应判断车辆进入低电量状态，"
                    "限制车辆最大驱动功率，并通过人机交互"
                    "系统提示驾驶员及时充电。"
                ),
                "function_points": [
                    {
                        "id": "detect-battery-soc",
                        "name": "检测动力电池剩余电量",
                        "event": {
                            "actor": "电池管理系统",
                            "action": "检测",
                            "object": "动力电池剩余电量",
                            "effect": (
                                "获得动力电池当前剩余电量"
                            ),
                            "trigger": "车辆启动或周期检测触发",
                            "condition": (
                                "电池管理系统已上电且"
                                "电池采样通信正常"
                            ),
                            "inputs": [
                                "车辆启动信号",
                                "动力电池电压数据",
                                "动力电池电流数据",
                                "电池状态采样数据"
                            ],
                            "outputs": [
                                "动力电池剩余电量"
                            ],
                            "preconditions": [
                                "车辆已启动",
                                "电池管理系统正常运行",
                                "电池采样数据有效"
                            ],
                            "postconditions": [
                                "已获得最新的动力电池剩余电量"
                            ]
                        }
                    },
                    {
                        "id": "evaluate-low-battery-state",
                        "name": "判断低电量状态",
                        "event": {
                            "actor": "电池管理系统",
                            "action": "判断",
                            "object": "动力电池低电量状态",
                            "effect": (
                                "确定动力电池是否进入"
                                "低电量运行状态"
                            ),
                            "trigger": (
                                "获得最新的动力电池剩余电量"
                            ),
                            "condition": (
                                "动力电池剩余电量检测结果有效"
                            ),
                            "inputs": [
                                "动力电池剩余电量",
                                "低电量阈值20%"
                            ],
                            "outputs": [
                                "低电量状态判定结果"
                            ],
                            "preconditions": [
                                "已完成动力电池剩余电量检测",
                                "低电量阈值已配置"
                            ],
                            "postconditions": [
                                "已确定车辆是否处于低电量状态"
                            ]
                        }
                    },
                    {
                        "id": "limit-drive-power",
                        "name": "限制车辆驱动功率",
                        "event": {
                            "actor": "车辆能量管理控制器",
                            "action": "限制",
                            "object": "车辆最大驱动功率",
                            "effect": (
                                "降低车辆最大可用驱动功率，"
                                "减少动力电池能量消耗"
                            ),
                            "trigger": (
                                "低电量状态判定结果为低电量"
                            ),
                            "condition": (
                                "动力电池剩余电量低于20%，"
                                "且车辆处于可执行功率限制的"
                                "运行状态"
                            ),
                            "inputs": [
                                "低电量状态判定结果",
                                "当前车辆运行状态",
                                "当前驱动功率需求"
                            ],
                            "outputs": [
                                "驱动功率限制指令"
                            ],
                            "preconditions": [
                                "车辆已进入低电量状态",
                                "车辆能量管理控制器正常运行"
                            ],
                            "postconditions": [
                                "车辆最大驱动功率已受限"
                            ]
                        }
                    },
                    {
                        "id": "notify-driver-to-charge",
                        "name": "提示驾驶员及时充电",
                        "event": {
                            "actor": "车辆人机交互系统",
                            "action": "提示",
                            "object": "驾驶员",
                            "effect": (
                                "向驾驶员展示低电量信息和"
                                "充电提醒"
                            ),
                            "trigger": (
                                "低电量状态判定结果为低电量"
                            ),
                            "condition": (
                                "车辆人机交互系统正常运行"
                            ),
                            "inputs": [
                                "低电量状态判定结果",
                                "动力电池剩余电量"
                            ],
                            "outputs": [
                                "低电量告警信息",
                                "充电提示信息"
                            ],
                            "preconditions": [
                                "车辆已进入低电量状态",
                                "仪表或中控显示功能可用"
                            ],
                            "postconditions": [
                                "驾驶员已收到低电量充电提示"
                            ]
                        }
                    }
                ],
                "summary": (
                    "该功能点集合描述新能源汽车在动力电池"
                    "低电量场景下，从剩余电量检测、低电量"
                    "状态判断，到驱动功率限制和驾驶员充电"
                    "提醒的完整功能链路。"
                )
            },
            "relations": [
                {
                    "source": "detect-battery-soc",
                    "target": "evaluate-low-battery-state",
                    "source_name": "检测动力电池剩余电量",
                    "target_name": "判断低电量状态",
                    "relation_type": "data_flow",
                    "direction": "source_to_target",
                    "confidence": 0.99,
                    "evidence": (
                        "动力电池剩余电量检测结果作为"
                        "低电量状态判断的输入。"
                    )
                },
                {
                    "source": "evaluate-low-battery-state",
                    "target": "limit-drive-power",
                    "source_name": "判断低电量状态",
                    "target_name": "限制车辆驱动功率",
                    "relation_type": "control_flow",
                    "direction": "source_to_target",
                    "confidence": 0.97,
                    "evidence": (
                        "低电量状态判定结果为低电量时，"
                        "触发车辆驱动功率限制。"
                    )
                },
                {
                    "source": "evaluate-low-battery-state",
                    "target": "notify-driver-to-charge",
                    "source_name": "判断低电量状态",
                    "target_name": "提示驾驶员及时充电",
                    "relation_type": "control_flow",
                    "direction": "source_to_target",
                    "confidence": 0.98,
                    "evidence": (
                        "低电量状态判定结果为低电量时，"
                        "触发驾驶员充电提醒。"
                    )
                },
                {
                    "source": "detect-battery-soc",
                    "target": "notify-driver-to-charge",
                    "source_name": "检测动力电池剩余电量",
                    "target_name": "提示驾驶员及时充电",
                    "relation_type": "data_flow",
                    "direction": "source_to_target",
                    "confidence": 0.95,
                    "evidence": (
                        "充电提示需要使用动力电池剩余电量，"
                        "向驾驶员展示当前电量信息。"
                    )
                }
            ]
        },
        "error": None
    }

    return result