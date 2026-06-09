import re

STATUS_COLORS = {
    "Pass": "🟢",
    "Partial": "🟡",
    "Fail": "🔴"
}

def parse_report(raw: dict) -> dict:
    pillars = []

    for pillar in raw.get("pillars", []):
        status = pillar.get("status", "Fail").strip().title()
        pillars.append({
            "name": pillar.get("pillar_name", "Unknown"),
            "status": status,
            "badge": STATUS_COLORS.get(status, "⚪"),
            "reasoning": pillar.get("reasoning", ""),
            "evidence": pillar.get("evidence", "Not found"),
            "section": pillar.get("relevant_sections_act", "")
        })

    return {
        "overall_score": raw.get("overall_score", "0 out of 7"),
        "overall_summary": raw.get("overall_summary", ""),
        "pillars": pillars
    }

def get_score_color(score_str: str) -> str:
    try:
        match = re.search(r'\d+', score_str)
        if match:
            score = int(match.group())
            if score >= 5:
                return "green"
            elif score >= 3:
                return "orange"
            else:
                return "red"
        return "gray"
    except Exception:
        return "gray"