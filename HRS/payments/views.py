from django.shortcuts import render,redirect
from django.views import View
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView
from .models import Product

# Create your views here.

# stripe.api_key=settings.STRIPE_SECRET_KEY



class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


class ProductLandingPageView(TemplateView):
    template_name="landing.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Test Product")
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY": 'pk_test_51NODINSJxRVXZg3hJURtLaXJsfJBQfAWPJV7MGZ827EM8hOClcimQ8bcrIEJFbg1HgQuu7yBwpCaSCiQplOBC33v002yG3JWJY'
        })
        return context

class CreateCheckoutSessionView(View):
    def post(self,request,*args,**kwargs):
        stripe.api_key = 'sk_test_51NODINSJxRVXZg3hle1DXQ4NWjHxQUN0wVaYiFLPFZ6fC6tIALTuV13eWT2jv9YTUriz10phNCkW4z4r8ZER2mAt00yhzdLQtS'
        product_id=self.kwargs["pk"]
        product=Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )

        # return JsonResponse({
        #     'id':checkout_session.id
        # })
        return redirect(checkout_session.url)