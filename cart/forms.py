from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)]

#This is a add-to-cart-form mentioned in iFood.views
#It handles adding and updating item quantity in the cart
#User can add between 1 and 26 instances of each dish to the cart
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False, widget=forms.HiddenInput)
