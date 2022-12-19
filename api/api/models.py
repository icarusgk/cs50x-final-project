from django.db import models
from django.conf import settings

# Create your models here.

class WorkSpace(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workspaces')
  name = models.CharField(max_length=100)

  def __str__(self):
    return f'WorkSpace: {self.name} - {self.user}'


class Board(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='boards')
  name = models.CharField(max_length=40)
  workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name='boards')

  def __str__(self):
    return f'Board: {self.name}'


class Card(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cards')
  name = models.CharField(max_length=100)
  description = models.TextField(max_length=500, blank=True)
  board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='cards')

  def __str__(self):
    return f'Card: {self.name}'


