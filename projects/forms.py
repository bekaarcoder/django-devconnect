from django.forms import ModelForm
from django import forms
from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "demo_link",
            "source_link",
            "tags",
            "featured_image",
        ]
        widgets = {"tags": forms.CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Add Title"}
        )

        self.fields["description"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Write a description for your project...",
                "rows": "3",
            }
        )

        self.fields["demo_link"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Add a demo link"}
        )

        self.fields["source_link"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Add a source link"}
        )

        self.fields["featured_image"].widget.attrs.update(
            {"class": "form-control"}
        )

        self.fields["tags"].widget.attrs.update({"class": "form-tags"})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["body", "value"]
        labels = {"value": "Vote for this project", "body": "Write a review"}

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        self.fields["body"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Write your review here...",
                "rows": "3",
            }
        )

        self.fields["value"].widget.attrs.update({"class": "form-select"})
