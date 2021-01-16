from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, DeviceListView, \
    DeviceDetailView, DeviceCreateView, UserListView, CommentCreateView, ProjectListView, ProjectDetailView, \
    TaskDetailView, ProjectCreateView, ProjectUserListView, ProjectUpdateView, TaskCreateView, TaskUpdateView, \
    ProjectDeleteView, TodoCreateView

urlpatterns = [
    # path('', PostListView.as_view(), name='app-home'),

    path('', views.home, name='app-home'),
    path('admin_dashboard/', views.admin_user, name='admin-dashboard'),

    # Post Routes
    path('post/<int:pk>', login_required(PostDetailView.as_view()), name='post-detail'),
    path('post/new', login_required(PostCreateView.as_view()), name='post-create'),
    path('post/<int:pk>/update/', login_required(PostUpdateView.as_view()), name='post-update'),
    path('post/<int:pk>/delete/', login_required(PostDeleteView.as_view()), name='post-delete'),
    path('posts/', login_required(PostListView.as_view()), name='post-list'),

    # Device routes
    path('device/<int:pk>', login_required(DeviceDetailView.as_view()), name='device-detail'),
    path('device_category_select/', csrf_exempt(views.DeviceCategorySelectView.as_view()), name='device_category_select'),
    path('device/new', login_required(DeviceCreateView.as_view()), name='device-create'),
    path('devices/', login_required(DeviceListView.as_view()), name='device-list'),

    # Comment routes
    path('post/<int:pk>/comment/new', login_required(CommentCreateView.as_view()), name='comment-create'),

    # User routes
    path('users/', login_required(UserListView.as_view()), name='user-list'),

    # Projects routes
    path('projects/', login_required(ProjectListView.as_view()), name='project-list'),
    path('project/new', login_required(ProjectCreateView.as_view()), name='project-create'),
    path('project/<int:pk>/update/', login_required(ProjectUpdateView.as_view()), name='project-update'),
    path('project/<int:pk>/delete/', login_required(ProjectDeleteView.as_view()), name='project-delete'),
    path('project/<int:pk>', login_required(ProjectDetailView.as_view()), name='project-detail'),

    # ProjectUser routes
    path('projects/<int:pk>', login_required(ProjectUserListView.as_view()), name='project-user-list'),

    # Task routes
    path('task/<int:pk>/', login_required(TaskDetailView.as_view()), name='task-detail'),
    path('project/<int:pk>/task/new', login_required(TaskCreateView.as_view()), name='project-task-create'),

    path('task/new', login_required(TaskCreateView.as_view()), name='project-task-create'),
    path('task_delete/<int:pk>/', views.TaskDeleteView.as_view(), name="project-task-delete"),
    path('task_user_select/', csrf_exempt(views.TaskUserSelectView.as_view()), name='task_user_select'),

    path('project/<int:pk>/task/update/', login_required(TaskUpdateView.as_view()), name='project-task-update'),

    path('task/<int:pk>/todo/new', login_required(TodoCreateView.as_view()), name='todo-create'),

]
