# planner/ai_helper.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from datetime import date, timedelta
import re

load_dotenv()
api_key = os.getenv("LLM_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

def _try_parse_json(text):
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    fence_match = re.search(r"```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```", text, re.S | re.I)
    if fence_match:
        try:
            return json.loads(fence_match.group(1))
        except Exception:
            pass
    first_brace = re.search(r"(\{.*\}|\[.*\])", text, re.S)
    if first_brace:
        try:
            return json.loads(first_brace.group(1))
        except Exception:
            pass
    return None

def normalize_deadline(deadline_text, user_specified_days):
    """Convert relative deadlines to YYYY-MM-DD or use today if not specified."""
    if not deadline_text or deadline_text.strip() == "":
        return date.today().strftime("%Y-%m-%d")
    if user_specified_days:
        # Convert "in X day(s)" to absolute date
        match = re.search(r"in\s+(\d+)\s+day", deadline_text, re.I)
        if match:
            return (date.today() + timedelta(days=int(match.group(1)))).strftime("%Y-%m-%d")
        # Keep absolute date if LLM gives YYYY-MM-DD
        try:
            return date.fromisoformat(deadline_text).strftime("%Y-%m-%d")
        except Exception:
            return date.today().strftime("%Y-%m-%d")
    # If user didn't specify days/weeks/months, ignore LLM's relative deadline
    return date.today().strftime("%Y-%m-%d")

def _fallback_parse(text, max_tasks=None, user_specified_days=False):
    tasks = []
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    cur = {}
    for ln in lines:
        if re.match(r'^\d+\.', ln) or re.match(r'^- ', ln) or ln.lower().startswith("task:"):
            if cur:
                tasks.append(cur)
                cur = {}
            name = re.sub(r'^\d+\.\s*', '', ln)
            name = re.sub(r'^(task:)\s*', '', name, flags=re.I)
            cur['task_name'] = name.strip()
            cur.setdefault('deadline', '')
            cur.setdefault('dependencies', '')
        elif ln.lower().startswith("deadline:"):
            cur['deadline'] = ln.split(":",1)[1].strip()
        elif ln.lower().startswith("dependencies:") or ln.lower().startswith("depends on:"):
            cur['dependencies'] = ln.split(":",1)[1].strip()
        else:
            if 'task_name' not in cur:
                cur['task_name'] = ln
                cur.setdefault('deadline', '')
                cur.setdefault('dependencies', '')
            else:
                cur['task_name'] += " " + ln
    if cur:
        tasks.append(cur)
    if max_tasks and isinstance(max_tasks, int):
        tasks = tasks[:max_tasks]

    normalized = []
    for t in tasks:
        normalized.append({
            "task_name": t.get("task_name","Untitled Task").strip(),
            "deadline": normalize_deadline(t.get("deadline","").strip(), user_specified_days),
            "dependencies": t.get("dependencies","").strip()
        })
    return normalized

def generate_plan(goal_text, max_tasks=None):
    # Check if goal_text mentions any period
    user_specified_days = bool(re.search(r"\b(days?|weeks?|months?)\b", goal_text, re.I))

    max_tasks_sentence = f"Return up to {max_tasks} tasks." if max_tasks else "Return an appropriate number of tasks based on the complexity of the goal."
    prompt = f"""
You are a helpful task planner. Break down the following goal into actionable tasks.
For each task, provide:
- "task_name" (short string)
- "deadline" (suggested approximate date in YYYY-MM-DD format if possible, otherwise relative like "in 3 days")
- "dependencies" (comma-separated names of tasks this depends on, or empty string)

Goal: "{goal_text}"

{max_tasks_sentence}

Return the output as a JSON array ONLY.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a precise JSON generator. Return only JSON when asked."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=600
        )

        text = response.choices[0].message.content.strip()
        parsed = _try_parse_json(text)
        if parsed and isinstance(parsed, list):
            normalized = []
            for item in parsed:
                if not isinstance(item, dict):
                    continue
                normalized.append({
                    "task_name": str(item.get("task_name","")).strip() or "Untitled Task",
                    "deadline": normalize_deadline(str(item.get("deadline","")).strip(), user_specified_days),
                    "dependencies": str(item.get("dependencies","")).strip()
                })
            if max_tasks and isinstance(max_tasks, int):
                normalized = normalized[:max_tasks]
            if normalized:
                return normalized

        # fallback
        return _fallback_parse(text, max_tasks=max_tasks, user_specified_days=user_specified_days)

    except Exception as e:
        print("AI generation error:", e)
        return [{"task_name":"Error generating tasks","deadline":date.today().strftime("%Y-%m-%d"),"dependencies":""}]
