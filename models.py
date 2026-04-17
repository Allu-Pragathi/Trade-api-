from pydantic import BaseModel, Field

class AnalysisResponse(BaseModel):
    sector: str
    report: str
    timestamp: str

class ErrorResponse(BaseModel):
    error: str
    detail: str
