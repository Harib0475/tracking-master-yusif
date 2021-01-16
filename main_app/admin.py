from django.contrib import admin
from .models import Post, Device, DeviceCategory, BrandName, Country, Role, Department, Comment, Project, ProjectUser, \
    Task, Discussion, TaskDiscussion, Todo

# Register your models here.

admin.site.register(Country)
admin.site.register(BrandName)
admin.site.register(DeviceCategory)
admin.site.register(Device)
admin.site.register(Post)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(Comment)
admin.site.register(Project)
admin.site.register(ProjectUser)
admin.site.register(Task)
admin.site.register(Discussion)
admin.site.register(TaskDiscussion)
admin.site.register(Todo)





