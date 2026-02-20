from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    new_category = forms.CharField(
        max_length=100, 
        required=False, 
        label="Or Create New Category",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type a new category name...'})
    )

    class Meta:
        model = Product
        fields = ['title', 'category', 'new_category', 'description', 'price', 'stock', 'image_url', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/image.jpg'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category')

        if not category and not new_category:
            self.add_error('category', 'Please select an existing category or type a new one below.')
            self.add_error('new_category', 'Please select an existing category or type a new one above.')
        
        return cleaned_data
