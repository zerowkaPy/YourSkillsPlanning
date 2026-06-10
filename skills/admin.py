from sqladmin import ModelView
from db.tables import Skill


class SkillsAdmin(ModelView, model=Skill):
    name = "Skill"
    name_plural = "Skills"
    icon = "fa-solid fa-chart-bar"
    column_list = [Skill.name, Skill.desc, Skill.weight]


