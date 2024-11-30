from django.db import models
from django.contrib.auth.models import User


class ExecutionModel(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True)
    
    keys = models.CharField(blank=False, null=False, max_length=50, db_index=True)
    value = models.TextField()
    
    @classmethod
    def sort_ingredients(cls, ingredients: str) -> str:
        keys_list = ingredients.replace(' ','').split(',')
        keys_list.sort()
        return ','.join(keys_list)
        
    
    def save(self, *args, **kwargs):
        self.keys = self.sort_ingredients(self.keys)
        
        super().save(*args, **kwargs)


class UserExecution(models.Model):
    user: User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="executions")
    execution: ExecutionModel = models.ForeignKey(ExecutionModel, on_delete=models.CASCADE, related_name="users")
    called_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Call {self.execution.keys} from {self.user.username}"
