import json
from django.shortcuts import render
from rest_framework.response import Response
from web3 import Web3
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate
from Auction.models import Contract, CustomUser
import datetime
import os
from rest_framework.viewsets import ModelViewSet
from Auction.serializer import BiddersSerializer, ContractSerializer, CustomUserSerializer, LoginSerializer

web3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
PRIVATE_KEY = '0xe6c92058fdd4e22740f6346c0f0661a52f5234b3fa319aeb03df3b702f86a867'

with open('bin/Auction/Auction.json') as f:
    contract_json = json.load(f)

contract_abi = contract_json['abi']
contract_bytecode = contract_json['bytecode']

# Deploy the contract
deployed_contract = web3.eth.contract(
    bytecode=contract_bytecode, abi=contract_abi)
transaction = deployed_contract.constructor().build_transaction({
    'from': web3.eth.accounts[0],
    'gas': 6721975,
    'nonce': web3.eth.get_transaction_count(web3.eth.accounts[0])
})

# Get the transaction receipt
signed_transaction = web3.eth.account.sign_transaction(
    transaction, private_key=PRIVATE_KEY)
transaction_hash = web3.eth.send_raw_transaction(
    signed_transaction.rawTransaction)
transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)


# Retrieve the contract address from the transaction receipt
CONTRACT_ADDRESS = transaction_receipt['contractAddress']
print("Contract deployed at address:", CONTRACT_ADDRESS)

contract = web3.eth.contract(
    address=CONTRACT_ADDRESS, abi=contract_abi)
web3.eth.default_account = web3.eth.accounts[0]


@swagger_auto_schema(
    method='POST',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'startTime': openapi.Schema(type=openapi.TYPE_INTEGER),
            'finishTime': openapi.Schema(type=openapi.TYPE_INTEGER),
            'minBid': openapi.Schema(type=openapi.TYPE_INTEGER),
            'members': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
            ),
            'publicAuction': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        },
    ),
)
@api_view(['POST'])
def create_contract(request):
    contract_address = web3.eth.accounts[0]
    start_time = request.data.get('startTime')
    finish_time = request.data.get('finishTime')
    min_bid = request.data.get('minBid')
    members = [web3.to_checksum_address(address)
               for address in request.data.get('members')]
    public_auction = bool(request.data.get('publicAuction'))

    # Call the createContract method on the contract
    tx_hash = contract.functions.createContract(
        contract_address,
        start_time,
        finish_time,
        min_bid,
        members,
        public_auction
    ).transact()

    web3.eth.wait_for_transaction_receipt(tx_hash)

    # Create a new Contract object and save it to the database
    c = Contract(
        contract_address=contract_address,
        start_time=datetime.datetime.fromtimestamp(int(start_time/1000)),
        finish_time=datetime.datetime.fromtimestamp(int(finish_time/1000)),
        min_bid=min_bid,
        public_auction=public_auction
    )
    c.save()
    for member in members:
        try:
            m = CustomUser.objects.get(
                wallet_address=member, role='bidder')
        except:
            return Response('user not found', 404)
        c.members.add(m)
    c.save()

    return Response('object saved', status=200)

    # Render the create contract form


@swagger_auto_schema(method='POST', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'bid_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
    },
),)
@api_view(['POST'])
def place_bid(request, contractId, userId):
    # Get the Contract object from the database
    c = Contract.objects.prefetch_related('members').get(pk=contractId)
    user = CustomUser.objects.get(pk=userId)

    # Get the form data
    bid_amount = int(request.data.get('bid_amount'))

    if bid_amount < c.min_bid:
        return Response('Bid amount is less than the minimum bid.', status=400)

    if not c.public_auction:
        allowed = c.members.filter(wallet_address=user.wallet_address).exists()
        if not allowed:
            return Response('You are not allowed to bid in this auction.', status=406)

    temp = []
    if c.bidders is not None:
        for item in c.bidders:
            temp.append(item.split(',')[0])
    # Perform the bid
    if c.bidders is None or user.wallet_address not in temp:
        c.bidders = []
        c.bidders.append(f'{user.wallet_address}, {bid_amount}')
    else:
        for bidder in c.bidders:
            parts = bidder.split(',')
            if parts[0].strip() == user.wallet_address:
                c.bidders.remove(bidder)
                break
        c.bidders.append(f'{user.wallet_address}, {bid_amount}')

    c.save()

    return Response('Bid placed successfully.', status=200)


@api_view(['GET'])
def find_winner(request, contractId):
    # Get the Contract object from the database
    c = Contract.objects.get(pk=contractId)

    highest_amount = 0
    highest_address = None
    highest_string = None

    bidders = c.bidders
    if bidders is None:
        return Response('پیشنهادی ثبت نشده است.', 400)

    for entry in bidders:
        # Split the entry into address and amount
        address, amount = entry.split(', ')
        amount = int(amount)

        if amount > highest_amount:
            highest_amount = amount
            highest_address = address

    # tx_hash = contract.functions.transferFunds(
    #     highest_address, int(highest_amount)
    # ).transact()

    web3.eth.send_transaction({
        'from': highest_address,
        'to': web3.eth.accounts[0],
        'value': web3.to_wei(str(highest_amount), 'ether')
    })

    # web3.eth.wait_for_transaction_receipt(tx_hash)
    c.is_done = True
    c.save()
    return Response({'address_winner': highest_address, 'amount': highest_amount, 'username': CustomUser.objects.get(wallet_address=highest_address).username or None}, 200)


@swagger_auto_schema(method='POST', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'member_id': openapi.Schema(type=openapi.TYPE_STRING),
    },
),)
@api_view(['POST'])
def add_member(request, contractId):
    # Get the Contract object from the database
    c = Contract.objects.get(pk=contractId)

    member_id = request.data.get('member_id')
    member = CustomUser.objects.get_or_create(
        wallet_address=member_id, role='1')
    # Call the addMember method on the contract
    print(member)
    print(CONTRACT_ADDRESS)

    # contract.functions.addMember(
    #     (pk-1),  request.data.get('member_id')).transact()

    # Update the Contract object in the database
    c.members.add(member[0])
    c.save()

    # Redirect to the contract detail page
    return Response('member added', 200)


@api_view(['GET'])
def get_contract(request, contractId):
    # Get the Contract object from the database
    c = Contract.objects.get(pk=contractId)

    # contract_data = contract.functions.getContract(contract_id-1)

    # # Format the response data
    # response_data = {
    #     'contract_address': contract_data[0],
    #     'start_time': contract_data[1],
    #     'finish_time': contract_data[2],
    #     'min_bid': contract_data[3],
    #     'bidders': contract_data[4],
    #     'members': contract_data[5],
    #     'public_auction': contract_data[6]
    # }

    return Response(ContractSerializer(c).data, status=200)


@api_view(['GET'])
def get_contracts(request):
    # Get the Contract object from the database
    c = Contract.objects.all()

    # contract_data = contract.functions.getContract(contract_id-1)

    # # Format the response data
    # response_data = {
    #     'contract_address': contract_data[0],
    #     'start_time': contract_data[1],
    #     'finish_time': contract_data[2],
    #     'min_bid': contract_data[3],
    #     'bidders': contract_data[4],
    #     'members': contract_data[5],
    #     'public_auction': contract_data[6]
    # }

    return Response(ContractSerializer(c, many=True).data, status=200)


class CustomUserView(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    http_method_names = ['post']


@swagger_auto_schema(method='POST', request_body=LoginSerializer)
@api_view(['POST'])
def login(request):
    try:
        user = authenticate(
            request, username=request.data['username'], password=request.data['password'])
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=200)
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
    except:
        return Response({'error': 'Invalid credentials'}, status=401)


@api_view(['GET'])
def current_user(request):
    try:
        return Response(CustomUserSerializer(CustomUser.objects.get(id=request.user.id)).data)
    except:
        return Response({'message': 'user not valid'}, 403)


@api_view(['GET'])
def get_bidders(self):
    list = CustomUser.objects.filter(role='bidder')
    return Response(BiddersSerializer(list, many=True).data)
