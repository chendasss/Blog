from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    # 蜜罐字段：正常用户看不到，机器人填了就静默丢弃
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput, label="")
    parent_id = forms.IntegerField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Comment
        fields = ["name", "email", "content"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "昵称", "class": "input"}),
            "email": forms.EmailInput(attrs={"placeholder": "邮箱（不会公开显示）", "class": "input"}),
            "content": forms.Textarea(attrs={"placeholder": "写下你的评论…", "rows": 4, "class": "input"}),
        }
