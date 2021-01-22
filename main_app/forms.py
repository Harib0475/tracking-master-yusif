from django import forms

from .models import Post, Comment, Project, Task, Todo, Device


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'device',
        ]


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'device'
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'body',
            'post',
        ]


# Create your models here.
class DateInput(forms.DateInput):
    input_type = 'date'


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'project_leader',
            # 'date_created',
            'deadline',
            'project_user'
        ]
        widgets = {
            'deadline': DateInput()
        }


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        # fields = [
        #     'name',
        #     'description',
        #     'deadline',
        #     'user',
        #     'project',
        # ]
        exclude = ('date_created', 'date_completed', 'is_active')
        widgets = {
            'deadline': DateInput()
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['device_user'].required = False
    #     self.fields['device_user'].disabled = True
    #     self.fields['device_user'].hidden = True
    #     self.fields['device_user'].label = False
    #     self.fields['device_user'].widget.attrs.update({'hidden': True})
    #


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        # fields = [
        #     'name',
        #     'description',
        #     'deadline',
        #     'user',
        #     'project',
        # ]
        exclude = ('date_created', 'date_completed', 'is_active')
        widgets = {
            'deadline': DateInput()
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['device_user'].required = False
    #     self.fields['device_user'].disabled = True
    #     self.fields['device_user'].hidden = True
    #     self.fields['device_user'].label = False
    #     self.fields['device_user'].widget.attrs.update({'hidden': True})
    #


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = [
            'title',
            'task'
        ]

    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', None)
        super().__init__(*args, **kwargs)
        if project_id:
            self.fields['task'].queryset = Task.objects.filter(project__id=project_id)


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['device_user'].required = False
        self.fields['device_user'].disabled = True
        self.fields['device_user'].hidden = True
        self.fields['device_user'].label = False
        self.fields['device_user'].widget.attrs.update({'hidden': True})

    def save(self, commit=True):
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:
            if self.data.get('device_user'):
                self.instance.device_user = self.data.get('device_user')
            self.instance.save()
            self._save_m2m()
        else:
            self.save_m2m = self._save_m2m
        return self.instance
