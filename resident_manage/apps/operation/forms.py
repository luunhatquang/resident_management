from django import forms
from .models import OperationExpense

class OperationExpenseForm(forms.ModelForm):
    class Meta:
        model = OperationExpense
        fields = '__all__'
        widgets = {
            'expense_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'VD: EXP12345'
            }),
            'expense_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tiêu đề chi phí'
            }),
            'category_type': forms.Select(attrs={'class': 'form-control'}),
            'building': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }), 
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'recorded_by': forms.Select(attrs={'class': 'form-control'}),
        }
        