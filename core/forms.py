from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
  ('S', 'Stripe'),
  ('P', 'Paypal')
)

class CheckoutForm(forms.Form):
  address1 = forms.CharField(label='Address 1', widget=forms.TextInput(
    attrs={
      'class':'form-control'
    }
  ))
  address2 = forms.CharField(required=False, widget=forms.TextInput(
    attrs={
      'class':'form-control'
    }
  ) , label='Address 2')
  country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(
    attrs={
      'class':'form-control'
    }
  ))
  zip_code = forms.CharField(max_length=10, widget=forms.TextInput(
    attrs={
      'class':'form-control'
    }
  ) , label='Zpi Code')
  same_shipping_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
  save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
  payment_options = forms.ChoiceField(
                    widget=forms.RadioSelect(),
                    choices=PAYMENT_CHOICES
                    )


class ReviewForm(forms.Form):
  review = forms.CharField(widget=forms.TextInput(
    attrs={
      'class':'form-control',
      'placeholder':'Add a review ...'
    }
  ))