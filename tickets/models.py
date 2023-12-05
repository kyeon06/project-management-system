from django.db import models

from common.models import BaseModel
from kanbans.models import Column
from teams.models import Team
from users.models import User


class Ticket(BaseModel):
    TAG_CHOICES = (
        ("Backend", "BE"),
        ("Frontend", "FE"),
        ("Design", "Design"),
        ("QA", "QA"),
        ("PM", "PM"),
        ("Document", "Document"),
    )

    title = models.CharField("작업제목", max_length=200)
    order = models.IntegerField("작업순서")
    tag = models.CharField("태그", choices=TAG_CHOICES, max_length=100)
    deadline = models.DateField("작업기한")
    workload = models.FloatField("작업시간(H)")

    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        db_table = "tickets"
    
    def __str__(self):
        return self.title
