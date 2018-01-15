from datetime import datetime

from rest_framework import generics
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product, PricingBlock
from products.serializers import ProductSerializer, PricingBlockSerializer, BestPriceSerializer
from products.utils import get_price


class ProductList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PricingBlockList(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = PricingBlock.objects.all()
    serializer_class = PricingBlockSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BestPrice(APIView):
    """
    Resource used to find the best price based on provided start date, number of nights and product ID

    Improvement ideas:
        1.) Authentication and security
        2.) Better and more granular error/exception handling, localized error messages for the client/UI
    """
    def get(self, request):
        try:
            # Retrieve GET request params
            product_id = request.GET.get('product_id', None)
            start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d')
            num_nights = request.GET.get('num_nights', None)

            # Get the best price for the requested time range
            best_price = get_price(product_id, start_date.date(), int(num_nights))

            # Produce a JSON response
            response = Response(BestPriceSerializer(best_price).data, status=status.HTTP_200_OK)
        except Exception as e:
            response = Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return response
