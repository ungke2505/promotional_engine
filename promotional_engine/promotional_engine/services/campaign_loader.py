from __future__ import annotations

from datetime import datetime

from .frappe_repository import load_campaigns_from_db


def load_active_campaigns(context: dict) -> list[dict]:
    campaigns = context.get("campaigns") or load_campaigns_from_db()
    if campaigns:
        return [campaign for campaign in campaigns if _is_campaign_active(campaign)]

    return []


def _is_campaign_active(campaign: dict) -> bool:
    status = (campaign.get("status") or "Active").lower()
    if status not in {"active", "draft"}:
        return False

    now = datetime.utcnow()
    start_date = _parse_datetime(campaign.get("start_date"))
    end_date = _parse_datetime(campaign.get("end_date"))

    if start_date and now < start_date:
        return False
    if end_date and now > end_date:
        return False
    return True


def _parse_datetime(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return None
