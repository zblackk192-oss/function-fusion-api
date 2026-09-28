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
        "request_id": "REQ-DEMO-001",
        "status": "success",
        "result": {
            "function_point_set": {
                "raw_text": "\n".join(raw_text_list),
                "function_points": merged_function_points,
                "summary": "\n".join(summary_list)
            },
            "relations": [
                relation.model_dump()
                for relation in request.relations
            ]
        },
        "error": None
    }

    return result