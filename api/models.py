from django.db import models

class District(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    geometry = models.TextField()
    area_km2 = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class SubDistrict(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=30, unique=True)
    geometry = models.TextField()
    area_km2 = models.FloatField()

class PopulationData(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    sub_district = models.ForeignKey(SubDistrict, on_delete=models.CASCADE, null=True, blank=True)
    year = models.IntegerField()
    population = models.IntegerField()
    density_per_km2 = models.FloatField()
    children_0_6 = models.IntegerField(default=0)
    children_7_17 = models.IntegerField(default=0)
    adults_18_64 = models.IntegerField(default=0)
    seniors_65_plus = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['district', 'sub_district', 'year']

class School(models.Model):
    SCHOOL_TYPES = [
        ('primary', 'Начальная школа'),
        ('secondary', 'Средняя школа'),
        ('high', 'Старшая школа'),
        ('gymnasium', 'Гимназия'),
        ('lyceum', 'Лицей'),
    ]
    
    name = models.CharField(max_length=200)
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPES)
    location = models.CharField(max_length=100)
    capacity = models.IntegerField()
    current_enrollment = models.IntegerField()
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    sub_district = models.ForeignKey(SubDistrict, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    established_year = models.IntegerField()

class Hospital(models.Model):
    HOSPITAL_TYPES = [
        ('clinic', 'Поликлиника'),
        ('hospital', 'Больница'),
        ('emergency', 'Скорая помощь'),
        ('specialized', 'Специализированная'),
    ]
    
    name = models.CharField(max_length=200)
    hospital_type = models.CharField(max_length=20, choices=HOSPITAL_TYPES)
    location = models.CharField(max_length=100)
    beds_count = models.IntegerField()
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

class FireStation(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    response_radius_km = models.FloatField(default=3.0)
    vehicles_count = models.IntegerField()
    personnel_count = models.IntegerField()
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

class BuildingZone(models.Model):
    ZONE_TYPES = [
        ('residential', 'Жилая зона'),
        ('commercial', 'Коммерческая'),
        ('industrial', 'Промышленная'),
        ('educational', 'Образовательная'),
        ('recreational', 'Рекреационная'),
        ('restricted', 'Ограниченная'),
    ]
    
    zone_type = models.CharField(max_length=20, choices=ZONE_TYPES)
    geometry = models.TextField()
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    can_build_school = models.BooleanField(default=False)
    max_building_height = models.IntegerField(null=True)
    restrictions = models.TextField(blank=True)

class SchoolDemand(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    sub_district = models.ForeignKey(SubDistrict, on_delete=models.CASCADE, null=True)
    year = models.IntegerField()
    current_capacity = models.IntegerField()
    required_capacity = models.IntegerField()
    shortage = models.IntegerField()
    avg_distance_to_school = models.FloatField()
    
    @property
    def utilization_rate(self):
        return (self.current_capacity / self.required_capacity) * 100 if self.required_capacity > 0 else 0

class OptimalLocation(models.Model):
    location = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    score = models.FloatField()
    population_coverage = models.IntegerField()
    avg_distance = models.FloatField()
    competition_factor = models.FloatField()
    accessibility_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-score']