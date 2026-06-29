from google import genai
import json

from src.constants import API_KEY

client = genai.Client(api_key=API_KEY)

instruction = """You are a skill dependency graph analyzer.

You receive a list of skills.

Your task is to identify logical dependency and prerequisite relationships ONLY between the skills provided in the input.

IMPORTANT RULES:

1. Use ONLY skills that exist in the input list.
2. NEVER invent new skills, categories, domains, labels, or group names.
3. Every "parent" value must be a skill from the input list.
4. Every "child" value must be a skill from the input list.
5. A relationship should be created only when there is a meaningful dependency, prerequisite, specialization, or strong learning relationship between two skills.
6. Do NOT create relationships based only on loose similarity.
7. Do NOT create duplicate edges.
8. Do NOT create self-references (parent and child cannot be the same skill).
9. If no relationships exist between any skills, return an empty array.
10. Return ONLY valid JSON. No explanations, no markdown, no comments, no extra text.

Relationship direction:

* parent → child means that learning the parent skill helps, supports, or is typically required before learning the child skill.
* The graph is directed.
* A skill may have multiple children.
* A skill may have multiple parents.

Input:
{INPUT_SKILLS}

Output schema:

{
"edges": [
{
"parent": "skill_name",
"child": "skill_name"
}
]
}

Example:

Input:

Python, FastAPI, SQLAlchemy, SQL, HTTP, English

Output:

{
"edges": [
{
"parent": "Python",
"child": "FastAPI"
},
{
"parent": "Python",
"child": "SQLAlchemy"
},
{
"parent": "SQL",
"child": "SQLAlchemy"
},
{
"parent": "HTTP",
"child": "FastAPI"
}
]
}
"""


async def build_relations(skills:list[str]) -> dict[str,list[dict[str, str]]]:
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=skills,
        config={
            "system_instruction":instruction
        }
    )
    relations = response.text
    if not relations:
        return {}
    parsed = _relation_to_dict(relations)
    return parsed


def _relation_to_dict(text:str) -> dict[str,list[dict[str, str]]]:
    if text.startswith("```json"):
        text = text.removeprefix("```json").strip()

    if text.endswith("```"):
        text = text.removesuffix("```").strip()

    relations = json.loads(text)
    return relations
