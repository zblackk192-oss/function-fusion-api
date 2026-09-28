from typing import Any, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(
    title="Function Fusion API",
    description="功能逻辑架构多源融合接口",
    version="1.0.0"
)


# =========================
# 请求模型
# =========================

class FunctionPointSet(BaseModel):
    raw_text: str = ""
    function_points: List[Any] = Field(default_factory=list)
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
    function_point_sets: List[FunctionPointSet] = Field(default_factory=list)
    relations: List[Relation] = Field(default_factory=list)


# =========================
# 基础测试接口
# =========================

@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "function-fusion-api"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================
# 功能融合接口
# =========================

@app.post("/api/v1/function-fusion/fuse")
def fuse_function_logic(request: FusionRequest):

    # 暂时先做最简单的融合：
    # 把所有 function_points 合并到一起
    merged_function_points = []

    raw_text_list = []
    summary_list = []

    for item in request.function_point_sets:

        if item.raw_text:
            raw_text_list.append(item.raw_text)

        if item.summary:
            summary_list.append(item.summary)

        merged_function_points.extend(item.function_points)

    result = {
        "caseId": "CURRENT001",
        "projectName": "新能源汽车动力电池系统",

        "functions": [
            {
                "functionId": "F001",
                "name": "检测动力电池剩余电量",
                "action": "检测",
                "object": "动力电池剩余电量",
                "effect": "获取动力电池当前剩余电量状态",
                "trigger": "车辆启动",
                "condition": "电池管理系统已上电且通信正常",
                "inputs": [
                    "车辆启动信号",
                    "电池状态数据"
                ],
                "outputs": [
                    "动力电池剩余电量"
                ],
                "preconditions": [
                    "车辆已启动"
                ],
                "postconditions": [
                    "已获得动力电池剩余电量"
                ],
                "scenario": "车辆运行",
                "constraint": "满足实时电量检测需求"
            },
            {
                "functionId": "F002",
                "name": "限制驱动功率",
                "action": "限制",
                "object": "驱动功率",
                "effect": "降低车辆最大可用驱动功率，减少电量消耗",
                "trigger": "动力电池剩余电量低于20%",
                "condition": "动力电池剩余电量低于20%",
                "inputs": [
                    "动力电池剩余电量"
                ],
                "outputs": [
                    "驱动功率限制指令"
                ],
                "preconditions": [
                    "动力电池剩余电量低于20%"
                ],
                "postconditions": [
                    "驱动功率已受限"
                ],
                "scenario": "低电量运行",
                "constraint": "保证低电量状态下车辆安全运行"
            },
            {
                "functionId": "F003",
                "name": "提示驾驶员充电",
                "action": "提示",
                "object": "驾驶员",
                "effect": "通知驾驶员当前电量过低，需要及时充电",
                "trigger": "动力电池剩余电量低于20%",
                "condition": "动力电池剩余电量低于20%",
                "inputs": [
                    "动力电池剩余电量"
                ],
                "outputs": [
                    "充电提示信号"
                ],
                "preconditions": [
                    "动力电池剩余电量低于20%"
                ],
                "postconditions": [
                    "已向驾驶员发出充电提示"
                ],
                "scenario": "低电量运行",
                "constraint": "提示信息需要及时反馈"
            }
        ],

        "relations": [
            {
                "source": "F001",
                "target": "F002",
                "type": "data_flow",
                "flowObject": "动力电池剩余电量"
            },
            {
                "source": "F001",
                "target": "F003",
                "type": "data_flow",
                "flowObject": "动力电池剩余电量"
            }
        ]
    }

    return result