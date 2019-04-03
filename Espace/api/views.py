from rest_framework import generics
from .serializers import (TokenSerializer, RegistrationSerializer,
                          savingsSerializer, loansSerializer,
                          LoanRepaymentsSerializer)
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import (IsAuthenticated, AllowAny,)
from .permissions import (isOwnerOrAdmin, IsAdminUserOrReadOnly)
from django.contrib.auth import login, authenticate, logout
from .models import User, Savings, Loans, LoanRepayment
from .utils import getUser, isAdmin, OwnerOrAdmin
from django.db.models import Sum

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class Users(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUserOrReadOnly, )
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        isAdmin(self, request.user)
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        # email = request.data['email']
        # subject = "Registration"

        body = "<h1> Welcome to Njokeriosacco </h1> <p> Hey {}, We are delighted to have you as part of this amazing team</p><br><br> Regards, Njokeriosacco.".format(request.data['first_name'])  # noqa
        serializer.save()
        try:
            # sendMailThread(subject, body, email).start()
            response = {
                "message": "User registered successfully",
                "user_info": serializer.data
            }
        except Exception:
            response = {
                "message": "User registered successfully but email not sent",
                "user_info": serializer.data
            }

        return Response(response, status=status.HTTP_201_CREATED)


class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdminUserOrReadOnly,
    )


class LoginView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")

        if not username or not password:
            response = Response(
                {'message': "Ensure to give both your username and password"})
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                serializer = TokenSerializer(
                    data={
                        "token": jwt_encode_handler(jwt_payload_handler(user)),
                    })

                serializer.is_valid()
                response = Response({
                    'message': "Logged in successfully",
                    'token': serializer.data['token'],
                })
            else:
                response = Response({'error': "Invalid login credentials"},
                                    status=status.HTTP_401_UNAUTHORIZED)
        return response


def LogoutView(request):
    return logout(request)


class SavingsView(generics.ListCreateAPIView):
    queryset = Savings.objects.all()
    permission_classes = (IsAdminUserOrReadOnly, )
    serializer_class = savingsSerializer

    def post(self, request, pk):
        user = getUser(self, pk)
        serializer = self.serializer_class(
            data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, amount=request.data.get('amount'))
        response = {
            'message': 'Savings added successfully',
            'savings_info': serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def get(self, request, pk=None):
        if pk:
            getUser(self, pk)
            OwnerOrAdmin(self, request.user, pk)
            savings = Savings.objects.filter(user_id=pk)
        else:
            isAdmin(self, request.user)
            savings = Savings.objects.all()
        if not savings:
            return Response(
                {'error': 'User with that ID does not have any savings yet'})
        else:
            total = savings.aggregate(Sum('amount'))
            serializer = self.serializer_class(savings.all(), many=True)
            data = {
                'total savings': total['amount__sum'],
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)


class SavingsDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        IsAuthenticated,
        isOwnerOrAdmin,
        IsAdminUserOrReadOnly,
    )
    serializer_class = savingsSerializer
    queryset = Savings.objects.all()


class LoansApiView(generics.ListCreateAPIView):
    queryset = Loans.objects.all()
    permission_classes = (IsAdminUserOrReadOnly, )
    serializer_class = loansSerializer

    def post(self, request, pk):
        user = getUser(self, pk)
        loans = Loans.objects.filter(user_id=pk, status='pending')

        if not loans:
            serializer = self.serializer_class(
                data=request.data, context={'request': request})

            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, amount=request.data.get('amount'))
            response = {
                'message': 'Loan added successfully',
                'loan_info': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': 'User with that ID already has an active loan'})

    def get(self, request, pk=None):
        if pk:
            getUser(self, pk)
            OwnerOrAdmin(self, request.user, pk)
            loans = Loans.objects.filter(user_id=pk)
        else:
            isAdmin(self, request.user)
            loans = Loans.objects.all()
            total = loans.aggregate(Sum('amount'))
        if not loans:
            return Response(
                {'error': 'User with that ID does not have any loans yet'})
        else:
            serializer = self.serializer_class(loans.all(), many=True)
            if not pk:
                data = {
                    'total loans': total['amount__sum'],
                    'data': serializer.data
                }
            else:
                data = serializer.data

            return Response(data, status=status.HTTP_200_OK)


class LoansDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        IsAuthenticated,
        isOwnerOrAdmin,
        IsAdminUserOrReadOnly,
    )
    serializer_class = loansSerializer
    queryset = Loans.objects.all()


class LoansRepaymentsView(generics.ListCreateAPIView):
    permission_classes = (
        IsAuthenticated,
        isOwnerOrAdmin,
        IsAdminUserOrReadOnly,
    )
    serializer_class = LoanRepaymentsSerializer
    queryset = LoanRepayment.objects.all()

    def existing_loan(self, pk):
        user = getUser(self, pk)
        loan = Loans.objects.filter(user_id=user.id, status='pending').first()
        if not loan:
            return Response({'message': 'User has no pending loan'})
        return loan

    def post(self, request, pk):
        user = getUser(self, pk)
        loan = Loans.objects.filter(user_id=user.id, status='pending').first()

        if not loan:
            response = {'message': 'User has no pending loan'}
        else:
            repayments = LoanRepayment.objects.filter(loan_id=loan.id)
            total_repayments = 0
            excess = 0
            message = ''
            if repayments:
                total_repayments = sum([item.amount for item in repayments])

            total = total_repayments + request.data['amount']

            # check interest rates and modify this
            total_loan = loan.amount * 104/100

            if total >= total_loan:
                loan.status = 'completed'
                loan.save()
                excess = total - loan.amount
                if excess > 0:
                    pass
                    Savings.objects.create(
                        amount=excess, mode="loan overpayment", user=user)
                    message = ' overpayment added to user savings'

            data = request.data.get('amount') - excess

            serializer = self.serializer_class(
                data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(loan=loan, amount=data)
            response = {
                'message': 'Loan repayment successful' + message,
                'loan_info': serializer.data
            }

        return Response(response, status=status.HTTP_201_CREATED)

    def get(self, request, pk):
        user = getUser(self, pk)
        loan = Loans.objects.filter(user_id=user.id, status='pending').first()

        if not loan:
            response = {'message': 'User has no pending loan'}
        else:
            repayments = LoanRepayment.objects.filter(loan_id=loan.id)
            serializer = self.serializer_class(repayments.all(), many=True)
            response = serializer.data
        return Response(response, status=status.HTTP_200_OK)


class LoansRepaymentsDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        IsAuthenticated,
        IsAdminUserOrReadOnly,
    )
    serializer_class = LoanRepaymentsSerializer
    queryset = LoanRepayment.objects.all()
