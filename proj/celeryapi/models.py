from typing import Any
from django.db import models

# Create your models here.

class Plot(models.Model):
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.plot_id = models.UUIDField(primary_key=True)
        self.plot_case = models.ForeignKey(PlotCase, on_delete = models.CASCADE)
        self.plot_lot_number = models.CharField(max_length=100)
        self.plot_sale_order = models.CharField(max_length=100)
        self.plot_type = models.CharField(max_length=100)
        self.plot_size = models.FloatField()
        self.plot_upload_date = models.CharField(max_length=100)
        super().__init__(*args, **kwargs)