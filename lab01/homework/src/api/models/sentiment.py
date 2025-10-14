from pydantic import BaseModel
from pydantic import StringConstraints
from typing import Annotated


class PredictRequest(BaseModel):
    text: Annotated[str, StringConstraints(min_length=1)]


class PredictResponse(BaseModel):
    prediction: str
