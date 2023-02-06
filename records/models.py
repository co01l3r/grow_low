from django.db import models


class Cycle(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    date = models.DateField(auto_now_add=True)
    genetics = models.CharField(max_length=200, blank=True, null=True)
    seedbank = models.CharField(max_length=80, blank=True, null=True)
    fixture = models.CharField(max_length=200, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Log(models.Model):
    PHASE_CHOICES = [
        ('seedling', 'Seedling'),
        ('vegetative', 'Vegetative'),
        ('bloom', 'Bloom'),
    ]

    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name='Logs')
    temperature_day = models.FloatField(blank=True, null=True)
    temperature_night = models.FloatField(blank=True, null=True)
    humidity_day = models.FloatField(blank=True, null=True)
    humidity_night = models.FloatField(blank=True, null=True)
    pH = models.FloatField(blank=True, null=True)
    ec = models.FloatField(blank=True, null=True)
    phase = models.CharField(max_length=12, choices=PHASE_CHOICES)
    irrigation = models.FloatField(blank=True, null=True)
    light_height = models.FloatField(blank=True, null=True)
    light_power = models.FloatField(blank=True, null=True)
    calibration = models.BooleanField(default=False, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        phase_count = Log.objects.filter(cycle=self.cycle, phase=self.phase).count()
        return f'{self.cycle.name} - {self.get_phase_display()} - Day {phase_count}'


class Nutrient(models.Model):
    name = models.CharField(max_length=80)
    brand = models.CharField(max_length=80)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class NutrientLog(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name='nutrient_logs')
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    concentration = models.FloatField()

    def __str__(self):
        return f" {self.log} - {self.nutrient}"
