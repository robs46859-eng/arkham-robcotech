"""
Digital IT Girl task executors.

Bridges horizontal orchestration to the Digital IT Girl predictive niche engine:
- structured audience and market opportunity scoring
- niche brief synthesis from trend, review, and complaint signals
"""

import logging
from typing import Any, Dict, List

import httpx

from app.tasks import TaskExecutor

logger = logging.getLogger(__name__)


def _normalize_signal_list(raw_value: Any) -> List[Dict[str, Any]]:
    if not isinstance(raw_value, list):
        return []
    return [item for item in raw_value if isinstance(item, dict)]


def _coerce_numeric(value: Any, default: float = 0.0) -> float:
    try:
        return float(value if value is not None else default)
    except (TypeError, ValueError):
        return default


class NicheOpportunityScoringExecutor(TaskExecutor):
    """Score a candidate niche from audience filters and market signals."""

    @property
    def task_type(self) -> str:
        return "niche_opportunity_scoring"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        segment_filters = input_data.get("segment_filters", {})
        trend_signals = _normalize_signal_list(input_data.get("trend_signals"))
        complaint_signals = _normalize_signal_list(input_data.get("complaint_signals"))
        review_signals = _normalize_signal_list(input_data.get("review_signals"))

        trend_velocity = sum(_coerce_numeric(item.get("velocity")) for item in trend_signals)
        complaint_heat = sum(_coerce_numeric(item.get("severity")) for item in complaint_signals)
        review_gap = sum(_coerce_numeric(item.get("gap_score")) for item in review_signals)
        filter_count = len([value for value in segment_filters.values() if value not in ("", None, [], {})])

        opportunity_score = max(
            48.0,
            min(96.0, 54.0 + filter_count * 3.5 + trend_velocity * 1.2 + complaint_heat * 1.1 + review_gap),
        )
        gap_size = max(0.0, min(100.0, complaint_heat * 5 + review_gap * 7))
        dominant_theme = (
            step_data.get("focus")
            or input_data.get("focus")
            or "unmet demand"
        )

        logger.info(
            "Scored Digital IT Girl niche workflow=%s opportunity=%.2f trend_velocity=%.2f gap_size=%.2f",
            workflow_id,
            opportunity_score,
            trend_velocity,
            gap_size,
        )

        return {
            "success": True,
            "segment_filters": segment_filters,
            "opportunity_score": round(opportunity_score, 1),
            "trend_velocity": round(trend_velocity, 1),
            "gap_size": round(gap_size, 1),
            "watchlist_tags": [
                segment_filters.get("region", "us-metro"),
                segment_filters.get("industry", "general-market"),
                dominant_theme,
            ],
            "recommended_angle": f"Prioritize {dominant_theme} for the highest-scoring segment.",
            "signal_counts": {
                "trend_signals": len(trend_signals),
                "complaint_signals": len(complaint_signals),
                "review_signals": len(review_signals),
            },
        }


class MarketResearchSynthesisExecutor(TaskExecutor):
    """Synthesize a niche brief using horizontal model access, with a clean fallback."""

    @property
    def task_type(self) -> str:
        return "market_research_synthesis"

    async def execute(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict[str, Any],
        workflow_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        input_data = workflow_state.get("input_data", {})
        segment_filters = input_data.get("segment_filters", {})
        score = input_data.get("opportunity_score") or workflow_state.get("score_segment_opportunity", {}).get("opportunity_score")
        if score is None:
            score = input_data.get("seed_opportunity_score", 72)

        prompt_payload = {
            "segment_filters": segment_filters,
            "opportunity_score": score,
            "product_constraints": input_data.get("product_constraints", {}),
            "trend_signals": input_data.get("trend_signals", []),
            "complaint_signals": input_data.get("complaint_signals", []),
            "review_signals": input_data.get("review_signals", []),
        }

        gateway_url = "http://gateway:8080"
        system_prompt = (
            "You are the Digital IT Girl predictive niche analyst. "
            "Return a concise JSON-ready market brief with keys: niche_definition, why_now, "
            "ideal_price, ideal_weight, ideal_dimensions, winning_product_direction, monetization_playbook."
        )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{gateway_url}/v1/ai",
                    json={
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": str(prompt_payload)},
                        ],
                        "temperature": 0.2,
                    },
                    timeout=30.0,
                )
                if response.status_code == 200:
                    payload = response.json()
                    content = payload["choices"][0]["message"]["content"]
                    return {
                        "success": True,
                        "brief_status": "ai_synthesized",
                        "market_brief": content,
                    }
        except Exception as exc:
            logger.warning("Digital IT Girl synthesis fell back to local brief: %s", exc)

        region = segment_filters.get("region", "US metro")
        audience = segment_filters.get("demographic", "underserved digital consumer")
        return {
            "success": True,
            "brief_status": "local_fallback",
            "market_brief": (
                f"Niche definition: {audience} in {region}. "
                "Why now: rising demand with visible complaint clusters and fragmented product coverage. "
                "Ideal price: $34-$79. "
                "Ideal weight: under 2 lb. "
                "Ideal dimensions: compact and easy to ship. "
                "Winning product direction: solve the most repeated operational complaint with low-friction onboarding. "
                "Monetization playbook: creator-led demand capture, community proof, and review harvesting."
            ),
        }
