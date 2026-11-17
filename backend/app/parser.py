import re
from pathlib import Path
from typing import Dict, Union
from fastapi import HTTPException, status
from app.schemas import ScenarioDetail

# Points to the repository root (mailphish/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates" / "emails"


class TemplateParser:

    @staticmethod
    def safe_resolve_path(file_path_input: Union[str, Path]) -> Path:
        """Resolves template path safely within the project root."""
        target_path = Path(file_path_input)

        if not target_path.is_absolute():
            target_path = (PROJECT_ROOT / target_path).resolve()
        else:
            target_path = target_path.resolve()

        if not target_path.exists() or not target_path.is_file():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template file not found at path: '{file_path_input}'"
            )

        if target_path.suffix.lower() != ".html":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Selected template must be an .html file."
            )

        # Security boundary check
        if not target_path.is_relative_to(PROJECT_ROOT):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Path is outside permitted project directories."
            )

        return target_path

    @staticmethod
    def parse_header_comment(html_content: str) -> Dict[str, any]:
        """Extracts metadata from HTML comment block matching template format."""
        meta = {
            "subject": "",
            "sender": "",
            "brand": "",
            "category": "",
            "triggers": [],
            "visual_details": [],
            "red_flags": []
        }

        comment_match = re.search(r"<!--(.*?)-->", html_content, re.DOTALL)
        if not comment_match:
            return meta

        comment_body = comment_match.group(1)

        current_key = None
        buffer = []

        def flush_field(key: str, val: str):
            val = val.strip()
            if not val:
                return
            if key == "Subject:":
                meta["subject"] = val
            elif key in ("From:", "Sender:"):
                meta["sender"] = val
            elif key in ("Brand:", "Brand impersonated:"):
                meta["brand"] = val
            elif key in ("Type:", "Category:"):
                meta["category"] = val
            elif key in ("Trigger:", "Triggers:"):
                # Split triggers separated by '+' or ','
                raw_triggers = [t.strip() for t in re.split(r"[+,]", val) if t.strip()]
                meta["triggers"] = raw_triggers
            elif key in ("Red flags pro debrief:", "Red Flags:"):
                meta["red_flags"] = [f.strip() for f in re.split(r"[;,]", val) if f.strip()]
            elif key in ("Vizuální reference:", "Visual Details:"):
                meta["visual_details"] = [d.strip() for d in re.split(r"[;,]", val) if d.strip()]

        for line in comment_body.splitlines():
            line_str = line.strip()
            if not line_str:
                continue

            # Detect key header fields
            matched_key = None
            for key in ["Scenario:", "Type:", "Brand:", "Subject:", "From:", "Trigger:", "Red flags pro debrief:", "Vizuální reference:"]:
                if line_str.startswith(key):
                    matched_key = key
                    break

            if matched_key:
                if current_key and buffer:
                    flush_field(current_key, " ".join(buffer))
                current_key = matched_key
                buffer = [line_str[len(matched_key):].strip()]
            elif current_key:
                buffer.append(line_str)

        if current_key and buffer:
            flush_field(current_key, " ".join(buffer))

        return meta

    @classmethod
    def load_scenario(cls, file_path_input: Union[str, Path]) -> ScenarioDetail:
        """Loads HTML/TXT files and builds metadata."""
        file_path = cls.safe_resolve_path(file_path_input)
        html_content = file_path.read_text(encoding="utf-8")
        meta = cls.parse_header_comment(html_content)

        txt_path = file_path.with_suffix(".txt")
        txt_content = txt_path.read_text(encoding="utf-8") if txt_path.exists() else None

        scenario_id = file_path.stem
        rel_path = str(file_path.relative_to(PROJECT_ROOT)).replace("\\", "/")
        is_ref = "07-figma" in scenario_id or "reference" in scenario_id.lower()

        return ScenarioDetail(
            id=scenario_id,
            file_path=rel_path,
            file_name=file_path.name,
            is_reference=is_ref,
            subject=meta["subject"] or "Cvičné bezpečnostní oznámení",
            sender=meta["sender"] or "no-reply@lookalike.example",
            brand_impersonated=meta["brand"] or "Unknown Brand",
            category=meta["category"] or ("Reference email" if is_ref else "Account / security alert"),
            triggers=meta["triggers"],
            visual_details=meta["visual_details"],
            red_flags=meta["red_flags"],
            has_text_version=txt_content is not None,
            html_content=html_content,
            txt_content=txt_content
        )

    @staticmethod
    def render(content: str, replacements: Dict[str, str]) -> str:
        """Substitutes placeholders formatted as {{placeholder_name}}."""
        rendered = content
        for key, val in replacements.items():
            pattern = re.compile(f"\\{{\\{{\\s*{key}\\s*\\}}\\}}")
            rendered = pattern.sub(val, rendered)
        return rendered