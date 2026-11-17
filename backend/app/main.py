from typing import Dict, List
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from app.parser import PROJECT_ROOT, TEMPLATES_DIR, TemplateParser
from app.schemas import (
    AggregateMetrics,
    DebriefResponse,
    RenderRequest,
    RenderResponse,
    ScenarioDetail,
    ScenarioMetadata,
    TrackClickRequest,
)

app = FastAPI(
    title="Phishing Awareness Training Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for click events
db_click_events: List[Dict[str, str]] = []


@app.get("/api/v1/scenarios", response_model=List[ScenarioMetadata])
def list_scenarios():
    """Scans templates/emails/ and returns metadata for all .html scenarios."""
    if not TEMPLATES_DIR.exists():
        return []

    scenarios = []
    for file_path in sorted(TEMPLATES_DIR.glob("*.html")):
        try:
            detail = TemplateParser.load_scenario(file_path)
            meta = ScenarioMetadata(**detail.model_dump())
            scenarios.append(meta)
        except Exception:
            continue
    return scenarios


@app.get("/api/v1/scenarios/inspect", response_model=ScenarioDetail)
def inspect_scenario(file_path: str = Query(..., example="templates/emails/05-google-drive-shared-file.html")):
    """Parses and returns full scenario details by template path."""
    return TemplateParser.load_scenario(file_path)


@app.post("/api/v1/scenarios/render", response_model=RenderResponse)
def render_template(payload: RenderRequest):
    """Substitutes merge fields ({{recipient_name}}, {{tracking_url}}, etc.) into template."""
    scenario = TemplateParser.load_scenario(payload.file_path)

    replacements = {
        "recipient_name": payload.recipient_name,
        "recipient_email": payload.recipient_email,
        "sender_display_name": payload.sender_display_name,
        "tracking_url": payload.tracking_url,
        "login_time": "Dnes, 14:32",
        "login_location": "Praha, Česká republika",
        "tracking_number": "Z78945612",
        "pickup_point": "Z-BOX Hlavní 12, Praha",
        "file_name": "Mzdy_Q4_navrh.xlsx",
        **payload.custom_vars
    }

    html_rendered = TemplateParser.render(scenario.html_content, replacements)
    txt_rendered = (
        TemplateParser.render(scenario.txt_content, replacements)
        if scenario.txt_content else None
    )

    return RenderResponse(
        subject=TemplateParser.render(scenario.subject, replacements),
        sender=TemplateParser.render(scenario.sender, replacements),
        html_rendered=html_rendered,
        txt_rendered=txt_rendered
    )


@app.post("/api/v1/track-click")
def track_click(payload: TrackClickRequest):
    """Registers recipient link click event."""
    db_click_events.append({
        "token": payload.tracking_token,
        "file_path": payload.file_path
    })
    return {"status": "success", "token": payload.tracking_token}


@app.get("/api/v1/debrief", response_model=DebriefResponse)
def get_debrief(file_path: str = Query(..., example="templates/emails/05-google-drive-shared-file.html")):
    """Fetches psychological triggers, red flags, and brand checks for post-click debrief view."""
    scenario = TemplateParser.load_scenario(file_path)
    return DebriefResponse(
        scenario_id=scenario.id,
        brand_impersonated=scenario.brand_impersonated,
        subject=scenario.subject,
        sender=scenario.sender,
        is_reference=scenario.is_reference,
        triggers=scenario.triggers,
        red_flags=scenario.red_flags,
        visual_details=scenario.visual_details
    )


@app.get("/api/v1/analytics", response_model=AggregateMetrics)
def get_analytics():
    """Calculates click metrics broken down by brand and psychological trigger."""
    clicks_by_brand: Dict[str, int] = {}
    clicks_by_trigger: Dict[str, int] = {}

    for event in db_click_events:
        try:
            scenario = TemplateParser.load_scenario(event["file_path"])
            brand = scenario.brand_impersonated
            clicks_by_brand[brand] = clicks_by_brand.get(brand, 0) + 1

            for trigger in scenario.triggers:
                clicks_by_trigger[trigger] = clicks_by_trigger.get(trigger, 0) + 1
        except Exception:
            continue

    total_clicks = len(db_click_events)
    # The Click-Through Rate formula:
    # CTR = (Total Clicks / Total Delivered) * 100
    ctr = float(total_clicks)  # Base indicator

    return AggregateMetrics(
        total_clicks=total_clicks,
        click_through_rate=ctr,
        clicks_by_brand=clicks_by_brand,
        clicks_by_trigger=clicks_by_trigger
    )