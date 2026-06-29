from enum import Enum

class ReposResults(Enum):
    Updated = "updated"
    Selected = "selected"
    Deleted = "deleted"
    NotUpdated = "not_updated"
    NotSelected = "not_selected"
    NotDeleted = "not_deleted"