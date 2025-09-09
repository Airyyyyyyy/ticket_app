from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Ticket(models.Model):
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Reopened', 'Reopened'),
        ('Closed', 'Closed'),
    )
    CATEGORY_CHOICES = (
        ('POS Issue', 'POS Issue'),
        ('Transaction Issue', 'Transaction Issue'),
        ('Other', 'Other'),
    )
    LOCATION_CHOICES = (
        ('Warri', 'Warri'),
        ('Lagos', 'Lagos'),
        ('Osun', 'Osun'),
    )

    ticket_id = models.CharField(max_length=50, unique=True, editable=False)
    agent_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.ticket_id
    
    def save(self, *args, **kwargs):
        if not self.ticket_id:
            date_str = datetime.date.today().strftime("%Y-%m-%d")
            last_ticket = Ticket.objects.filter(created_at__date=datetime.date.today()).order_by('created_at').last()

            if last_ticket:
                last_id = int(last_ticket.ticket_id.split('-')[-1])
                new_id = last_id + 1
            else:
                new_id = 1

            self.ticket_id = f"TCKT-{date_str}-{new_id:05d}"
        super().save(*args, **kwargs)