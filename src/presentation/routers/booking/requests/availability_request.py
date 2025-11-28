from pydantic import BaseModel, Field
from datetime import date

class AvailabilityRequest(BaseModel):
    date_av: date = Field(..., description="YYYY-MM-DD")
