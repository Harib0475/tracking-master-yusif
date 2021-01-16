from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Country(models.Model):
    country_name = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.country_name


class BrandName(models.Model):
    brand_name = models.CharField(max_length=20, null=True)
    manufacturer = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.brand_name


class DeviceCategory(models.Model):
    category_name = models.CharField(max_length=20)
    brand = models.ForeignKey(BrandName, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.category_name


class Device(models.Model):
    name = models.CharField(max_length=10)
    Ram_size = models.IntegerField(null=True, blank=True)
    HDD_size = models.IntegerField(null=True, blank=True)
    CPU_size = models.IntegerField(null=True, blank=True)
    OS = models.CharField(max_length=20, null=True, blank=True)

    device_user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_category = models.ForeignKey(DeviceCategory, on_delete=models.CASCADE, null=True)
    brand_name = models.ForeignKey(BrandName, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('device-detail', kwargs={'pk': self.pk})


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    date_solved = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    priority = models.CharField(max_length=20, null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Project(models.Model):  # Many to Many
    name = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_completed = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    project_leader = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='project_leader')
    project_user = models.ManyToManyField(User, null=True,blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    body = models.CharField(max_length=500)
    created_on = models.DateTimeField(default=timezone.now)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    # active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
        # return self.body


class Department(models.Model):
    department_name = models.CharField(max_length=20)
    department_description = models.CharField(max_length=100, null=True, blank=True)

    department_leader = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.department_name


class Role(models.Model):
    role_name = models.CharField(max_length=30, null=True)
    role_description = models.CharField(max_length=50, null=True, blank=True)

    department_name = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.role_name


class ProjectUser(models.Model):
    date_joined = models.DateField(default=timezone.now)
    join_reason = models.CharField(max_length=64)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class Task(models.Model):
    name = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_completed = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    deadline = models.DateField(default=timezone.now)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    priority = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})


class Todo(models.Model):
    title = models.CharField(max_length=20, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_completed = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})


class Feedback(models.Model):
    body = models.TextField(max_length=500, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.body


class Discussion(models.Model):
    body = models.CharField(max_length=500)
    created_on = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    # active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return reverse('project-detail', kwargs={'pk': self.pk})


class TaskDiscussion(models.Model):
    body = models.CharField(max_length=500)
    created_on = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return reverse('task-detail', kwargs={'pk': self.pk})
