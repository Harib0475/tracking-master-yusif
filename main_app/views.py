from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import ModelFormMixin

from main_app.forms import CommentForm, ProjectCreateForm, PostCreateForm, TaskCreateForm, TaskUpdateForm, \
    PostUpdateForm, TodoForm, DeviceForm
from main_app.models import Post, Device, Country, BrandName, DeviceCategory, Department, Comment, Project, Task, \
    ProjectUser, Discussion, TaskDiscussion, Todo


# Function based View
@login_required
def home(request):
    context = {
        'posts': Post.objects.all(),
        'devices': Device.objects.all(),
        'users': User.objects.all(),
        'categories': DeviceCategory.objects.all(),
        'departments': Department.objects.all(),

        'total_devices': Device.objects.count(),
        'total_users': User.objects.count(),
        'total_posts': Post.objects.count(),

    }

    return render(request, 'main/index.html', context)


def admin_user(request):
    user = User.objects.get(request.user.id)

    context = {
        'users': User.objects.all(),
        'devices': Device.objects.all(),
        'posts': User.objects.all(),
        'countries': Country.objects.all(),
        'brands': BrandName.objects.all(),
    }
    if user.is_authenticated:
        return render(request, 'admin/admin_dashboard.html', context)


# Post Controller
class PostListView(ListView):
    model = Post

    template_name = 'post/post_list.html'

    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['devices'] = Device.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        return context


class PostCreateView(CreateView):
    model = Post
    template_name = 'post/post_form.html'

    context_object_name = 'posts'
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment/comment_form.html'

    success_url = reverse_lazy('post-list')

    context_object_name = 'comments'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post/post_form.html'
    form_class = PostUpdateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# Device Controller


class DeviceCreateView(CreateView):
    model = Device
    template_name = 'device/device_form.html'
    # fields = ['name', 'device_user','CPU_size', 'HDD_size', 'OS', 'brand_name', 'device_category']
    #
    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)
    form_class = DeviceForm

    def post(self, request, *args, **kwargs):
        dict = self.request.POST.copy()
        dict['device_user'] = self.request.user
        form = DeviceForm(data=dict)
        if form.is_valid():
            device = form.save()
            return redirect(reverse('device-detail', args=[device.id]))
        return render(request, self.template_name, {'form': form})


class DeviceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Device
    template_name = 'main_pages/device/device_form.html'
    fields = ['name', 'CPU_size', 'HDD_size', 'OS']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        device = self.get_object()
        if self.request.user == device.device_user_id:
            return True
        return False


class DeviceListView(ListView):
    model = Device
    template_name = 'device/device_list.html'

    context_object_name = 'devices'


class CommentListView(ListView):
    model = Comment
    template_name = 'post/post_detail.html'

    context_object_name = 'comments'


class DeviceDetailView(DetailView):
    model = Device
    template_name = 'device/device_detail.html'

    context_object_name = 'devices'


class UserListView(ListView):
    model = User
    template_name = 'user/user_list.html'

    context_object_name = 'users'


# Project Controller

class ProjectCreateView(CreateView):
    model = Project
    template_name = 'project/project_create_form.html'
    form_class = ProjectCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.date_created = timezone.now()
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    template_name = 'project/project_update_form.html'
    fields = [
        'name',
        'description',
        'project_leader'
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.project_leader:
            return True
        else:
            return False


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'project/project_delete_confirm.html'
    success_url = '/'

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.project_leader:
            return True
        return False


class ProjectListView(ListView):
    model = Project

    template_name = 'project/project_list.html'

    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Count
        context['total_tasks'] = Task.objects.count()
        context['total_members'] = Project.objects.count()
        context['total_projects'] = Project.objects.count()
        return context


class ProjectDetailView(DetailView):
    model = Project

    template_name = 'project/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['discussions'] = Discussion.objects.all()
        context['tasks'] = Task.objects.all()
        context['projects'] = Project.objects.all()

        # Count
        context['total_tasks'] = Task.objects.count()
        return context


class ProjectUserListView(ListView):
    model = ProjectUser

    template_name = 'project/project_detail.html'

    context_object_name = 'project_users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Count
        context['total_members'] = ProjectUser.objects.count()
        return context


class TaskCreateView(CreateView):
    model = Task
    template_name = 'task/task_create_form.html'
    form_class = TaskCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    template_name = 'task/task_update_form.html'
    form_class = TaskUpdateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user.id == task.user.id:
            return True
        else:
            print(self.request.user.id, 'and', task.user.id)
            return False


class TaskDetailView(ModelFormMixin, DetailView):
    model = Task
    template_name = 'task/task_detail.html'
    form_class = TodoForm

    context_object_name = 'tasks'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs()
        task = Task.objects.filter(id=self.kwargs.get('pk')).first()
        kwargs['project_id'] = task.project.id
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context['task_discussions'] = TaskDiscussion.objects.all()
        # import pdb;pdb.set_trace()
        # todo = Todo.objects.filter(id=self.kwargs.get('pk')).first()
        context['todos'] = Todo.objects.filter(task=self.kwargs.get('pk'), user=self.request.user)
        context['form'] = self.get_form()
        return context

    # def post(self, request, *args, **kwargs):
    #     self.todo = self.get_object()
    #     print(self.todo.id)
    #     form = TodoForm(request.POST or None)
    #     if form.is_valid():
    #         print(form.cleaned_data)
    #         form.save()
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        dict = request.POST.copy()
        dict['task'] = self.kwargs.get('pk')
        form = TodoForm(dict)
        if form.is_valid():
            form.instance.user = self.request.user
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # def form_valid(self, form):
    #     form.save()
    #     return super(TaskDetailView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('task-detail', kwargs={'pk': self.object.task.pk})


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('project-task-create')


class TodoCreateView(CreateView):
    model = Todo
    template_name = 'task/task_detail.html'
    form_class = TodoForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeviceCategorySelectView(TemplateView):

    def post(self, request, *args, **kwargs):
        styles = DeviceCategory.objects.filter(id=int(request.POST.get('id'))).first()
        brands = BrandName.objects.filter(id=styles.brand.id)
        data = serializers.serialize('json', brands, fields=('id', 'brand_name'))
        return JsonResponse({'device_categories': data})


class TaskUserSelectView(TemplateView):

    def post(self, request, *args, **kwargs):
        project = Project.objects.filter(id=int(request.POST.get('id'))).first()
        users = User.objects.filter(id__in=project.project_user.all())
        data = serializers.serialize('json', users, fields=('id', 'username'))
        return JsonResponse({'device_categories': data})
