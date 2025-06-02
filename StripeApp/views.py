import json

from django.shortcuts import render, get_object_or_404, reverse
from django import http
from StripeApp import models, constraints
import stripe


stripe.api_key = constraints.API_KEY


def get_item(request: http.HttpRequest, item_id: int) -> http.HttpResponse:
    item = get_object_or_404(models.Item, pk=item_id)

    return render(
        request,
        'pages/item_page.html',
        {
            'item': item
        }
    )


def buy_item(request: http.HttpRequest, item_id: int):
    item = get_object_or_404(models.Item, pk=item_id)

    session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': item.price * (
                            10 ** constraints.NUMBERS_AFTER_DOT
                    ),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success_page')),
        cancel_url=request.build_absolute_uri(reverse('cancel_page')),
    )

    return http.JsonResponse(
        {
            'sessionId': session.id
        }
    )


def buy_order(request: http.HttpRequest, order_id: int):
    order = get_object_or_404(models.Order, pk=order_id)

    coupon = stripe.Coupon.create(
        percent_off=order.discount.percent,
        duration="once",
    ) if order.discount else None

    tax = stripe.TaxRate.create(
        display_name=order.tax.name,
        inclusive=False,
        percentage=order.tax.percent,
    ) if order.tax else None

    session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'currency': order_item.item.currency,
                    'product_data': {
                        'name': order_item.item.name,
                    },
                    'unit_amount': order_item.item.price * (
                            10 ** constraints.NUMBERS_AFTER_DOT
                    ),
                },
                'quantity': order_item.quantity,
                'tax_rates': [
                    f'{tax.id}'
                ] if tax else None
            }
            for order_item in order.rel_order.select_related().all()
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success_page')),
        cancel_url=request.build_absolute_uri(reverse('cancel_page')),
        discounts=[
            {
                'coupon': f'{coupon.id}'
            }
        ] if coupon else []
    )

    return http.JsonResponse(
        {
            'sessionId': session.id
        }
    )


def success(request: http.HttpRequest) -> http.HttpResponse:
    return http.HttpResponse('Payment success')


def cancel(request: http.HttpRequest) -> http.HttpResponse:
    return http.HttpResponse('Payment canceled')


def add_to_order(request: http.HttpRequest) -> http.HttpResponse:
    if request.method != 'POST':
        raise http.HttpResponseNotAllowed

    data = json.loads(request.body)

    order, _ = models.Order.objects.get_or_create(pk=data['order_id'])
    item = get_object_or_404(models.Item, pk=data['item_id'])

    order_item, created = order.rel_order.get_or_create(item=item.id, defaults={'item': item})
    order_item.quantity += 1
    order_item.save()

    return http.JsonResponse(
        {
            'order_id': order.id,
            'item_id': item.id
        }
    )


def show_order(request: http.HttpRequest, order_id: int = None) -> http.HttpResponse:
    if not order_id:
        order = models.Order()
        order.save()
    else:
        order = get_object_or_404(models.Order, pk=order_id)

    return render(
        request,
        'pages/buy_order.html',
        {
            'order': order
        }
    )


def get_order(request: http.HttpRequest) -> http.HttpResponse:
    return render(
        request,
        'pages/order_redirect.html'
    )
