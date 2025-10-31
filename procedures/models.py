from django.db import models

# Create your models here.


class ProcedureCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10)
    description = models.TextField()
    filename = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Procedure Categories"
    
    def __str__(self):
        return self.name
