from django.db import models

# Create your models here.
class viewer_cmd(models.Model):

    cmd_input = models.TextField()

    cmd_output = models.TextField()

