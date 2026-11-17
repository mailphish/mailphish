from typing import Dict, List, Optional
from pydantic import BaseModel, EmailStr, Field


class ScenarioMetadata(BaseModel):
    id: str
    file_path: str
    file_name: str
    is_reference: bool
    subject: str
    sender: str
    brand_impersonated: str
    category: str
    triggers: List[str] = []
    visual_details: List[str] = []
    red_flags: List[str] = []
    has_text_version: bool = False


class ScenarioDetail(ScenarioMetadata):
    html_content: str
    txt_content: Optional[str] = None


class RenderRequest(BaseModel):
    file_path: str = Field(..., example="templates/emails/05-google-drive-shared-file.html")
    recipient_name: str = "Jan Novák"
    recipient_email: EmailStr = "jan.novak@firma.example"
    sender_display_name: str = "Pavel Dvořák"
    tracking_url: str = "https://example.com/t/sample-token"
    custom_vars: Dict[str, str] = Field(default_factory=dict)


class RenderResponse(BaseModel):
    subject: str
    sender: str
    html_rendered: str
    txt_rendered: Optional[str] = None


class TrackClickRequest(BaseModel):
    tracking_token: str
    file_path: str


class DebriefResponse(BaseModel):
    scenario_id: str
    brand_impersonated: str
    subject: str
    sender: str
    is_reference: bool
    triggers: List[str]
    red_flags: List[str]
    visual_details: List[str]


class AggregateMetrics(BaseModel):
    total_clicks: int
    click_through_rate: float
    clicks_by_brand: Dict[str, int]
    clicks_by_trigger: Dict[str, int]