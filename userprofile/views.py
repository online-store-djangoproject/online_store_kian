from datetime import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Address,DiscountCode
from .serializers import AddressSerializer
import uuid
from rest_framework.views import APIView
from .email import send_discount_email
from django.utils.timezone import now
# Create your views here.


class AddressListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddressUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class RequestDiscountCodeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user


        if not DiscountCode.user_can_get_discount(user):
            return Response({"message": "شما قبلاً در این ماه کد تخفیف دریافت کرده‌اید! 😕"}, status=400)


        discount_code = DiscountCode.objects.create(
            user=user,
            code=uuid.uuid4().hex[:8].upper(),
            percentage=15
        )


        send_discount_email(user, discount_code.code)

        return Response({"message": "✅ کد تخفیف شما به ایمیلتان ارسال شد!"}, status=200)

class ValidateDiscountCodeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        code = request.data.get("code")

        if not code:
            return Response({"valid": False, "message": "❌ لطفاً کد تخفیف را وارد کنید!"}, status=400)


        try:
            discount_code = DiscountCode.objects.get(code=code, user=user)
        except DiscountCode.DoesNotExist:
            return Response({"valid": False, "message": "❌ کد تخفیف نامعتبر است!"}, status=400)


        if discount_code.created_at.month != now().month:
            return Response({"valid": False, "message": "⏳ مهلت استفاده از این کد به پایان رسیده است!"}, status=400)


        return Response({
            "valid": True,
            "discount_percentage": discount_code.percentage,
            "message": f"✅ کد تخفیف معتبر است! {discount_code.percentage}% تخفیف اعمال شد."
        }, status=200)