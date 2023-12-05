from django.db import models

from common.models import BaseModel
from teams.models import Team

class Column(BaseModel):
    name = models.CharField("컬럼명", max_length=100)
    order = models.IntegerField("컬럼순서")

    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'columns'

    
    def __str__(self):
        return self.name