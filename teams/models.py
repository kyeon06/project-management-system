from django.db import models
from common.models import BaseModel
from users.models import User


class Team(BaseModel):
    name = models.CharField("팀명", max_length=100, unique=True)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "teams"

    def __str__(self):
        return self.name