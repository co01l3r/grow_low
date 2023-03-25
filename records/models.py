from django.db import models
import uuid
from django.db.models import Case, Value, When
from typing import List, Tuple


# Record model
class Cycle(models.Model):
    BEHAVIORAL_RESPONSE_CHOICES: List[Tuple[str, str]] = [
        ('auto-flowering', 'Auto-flowering'),
        ('photoperiodic', 'Photoperiodic'),
    ]
    SEED_TYPE_CHOICES: List[Tuple[str, str]] = [
        ('regular', 'Regular'),
        ('feminized', 'Feminized'),
        ('clones', 'Clones'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now_add=True)
    genetics = models.CharField(max_length=200)
    seedbank = models.CharField(max_length=80, blank=True, null=True)
    fixture = models.CharField(max_length=200)
    behavioral_response = models.CharField(max_length=30, blank=True, null=True, choices=BEHAVIORAL_RESPONSE_CHOICES)
    seed_type = models.CharField(max_length=30, blank=True, null=True, choices=SEED_TYPE_CHOICES)
    grow_medium = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=80, blank=True)

    def __str__(self) -> str:
        quarter: str = "Q" + str((self.date.month - 1) // 3 + 1)
        year: str = str(self.date.year)

        if self.name:
            name: str = self.name if quarter in self.name else f"{self.name} - {quarter}"
            return f"{name}/{year}"
        else:
            return f"{self.genetics} - {quarter}/{year}"


# Log model
class Log(models.Model):
    PHASE_CHOICES: List[Tuple[str, str]] = [
        ('seedling', 'Seedling'),
        ('vegetative', 'Vegetative'),
        ('bloom', 'Bloom'),
    ]
    LIGHT_POWER_CHOICES: List[Tuple[int, str]] = [
        (0, 'Darkness'),
        (25, '25%'),
        (50, '50%'),
        (75, '75%'),
        (100, '100%'),
    ]
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField(auto_now_add=True)
    phase = models.CharField(max_length=12, choices=PHASE_CHOICES)
    temperature_day = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    temperature_night = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    humidity_day = models.IntegerField(blank=True, null=True)
    humidity_night = models.IntegerField(blank=True, null=True)
    ph = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ec = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    irrigation = models.CharField(max_length=20, blank=True, null=True)
    light_height = models.IntegerField(blank=True, null=True)
    light_power = models.IntegerField(blank=True, null=True, choices=LIGHT_POWER_CHOICES)
    calibration = models.BooleanField(default=False, blank=True, null=True)
    featured_image = models.ImageField(null=True, blank=True)
    water = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering: List = [
            Case(
                When(phase='seedling', then=Value(1)),
                When(phase='vegetative', then=Value(2)),
                When(phase='bloom', then=Value(3)),
            ),
            'date',
            'id',
        ]

    def __str__(self) -> str:
        logs_of_same_phase: models.QuerySet = Log.objects.filter(cycle=self.cycle, phase=self.phase)
        day_in_phase: int = list(logs_of_same_phase).index(self) + 1
        return str(day_in_phase)


# Nutrient model
class Nutrient(models.Model):
    NUTRIENT_TYPE_CHOICES: List[Tuple[str, str]] = [
        ('medium_conditioner', 'Medium conditioner'),
        ('base_line', 'Base'),
        ('root_expander', 'Root expander'),
        ('bud_strengthener', 'Bud strengthener'),
        ('bud_enlarger', 'Bud enlarger'),
        ('bud_taste', 'Bud taste'),
    ]
    name = models.CharField(max_length=80)
    brand = models.CharField(max_length=80)
    nutrient_type = models.CharField(max_length=18, blank=True, null=True, choices=NUTRIENT_TYPE_CHOICES)
    featured_image = models.ImageField(null=True, blank=True, default="default_fertilizer.jpg")
    detail = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


# NutrientLog model
class NutrientLog(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name='nutrient_logs')
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    concentration = models.IntegerField()

    class Meta:
        ordering: List = ['nutrient__nutrient_type']

    def __str__(self) -> str:
        return f"{self.nutrient} - {self.concentration}"

    def save(self, *args, **kwargs) -> None:
        existing_logs = NutrientLog.objects.filter(log_id=self.log_id, nutrient=self.nutrient)
        if existing_logs.exists():
            self.concentration += sum(log.concentration for log in existing_logs)
            existing_logs.delete()
        super().save(*args, **kwargs)
