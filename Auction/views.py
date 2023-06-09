import json
from django.shortcuts import render
from requests import Response
from web3 import Web3
from rest_framework.decorators import api_view
from Auction.models import Contract
import datetime

web3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

with open('Auction\Auction.json') as f:
    contract_json = json.load(f)
abi = contract_json['abi']

contract = web3.eth.contract(address='0x076a4390ee353C8c6A07861BaDf49dd39fbF827D', abi=abi)
web3.eth.default_account = web3.eth.accounts[0]

@api_view(['POST'])
def create_contract(request):
    contract_address = request.data.get('contract_address')
    start_time = request.data.get('start_time')
    finish_time = request.data.get('finish_time')
    min_bid = request.data.get('min_bid')
    members = [address for address in request.data.get('members')]
    public_auction = bool(request.data.get('public_auction'))

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
        creator_address=contract_address,
        created_time=datetime.datetime.fromtimestamp(int(start_time)),
        finish_time=datetime.datetime.fromtimestamp(int(finish_time)),
        cost=min_bid,
    )
    c.save()

    return Response(c, status=200)

    # Render the create contract form

def place_bid(request, pk):
    # Get the Contract object from the database
    c = Contract.objects.get(pk=pk)

    if request.method == 'POST':
        # Get the form data
        bid_amount = int(request.POST.get('bid_amount'))

        # Call the placeBid method on the contract
        tx_hash = contract.functions.placeBid(pk).transact({'value': bid_amount})

        # Update the Contract object in the database
        c.bids[msg.sender][pk] += bid_amount
        c.tx_hash = tx_hash
        c.save()

        # Redirect to the contract detail page
        return redirect('contract_detail', pk=pk)

    # Render the place bid form
    return render(request, 'place_bid.html', {'contract': c})

def find_winner(request, pk):
    # Get the Contract object from the database
    c = Contract.objects.get(pk=pk)

    if request.method == 'POST':
        # Call the findTheWinner method on the contract
        tx_hash = contract.functions.findTheWinner(pk).transact()

        # Update the Contract object in the database
        c.tx_hash = tx_hash
        c.save()

        # Redirect to the contract detail page
        return redirect('contract_detail', pk=pk)

    # Render the find winner form
    return render(request, 'find_winner.html', {'contract': c})

def add_member(request, pk):
    # Get the Contract object from the database
    c = Contract.objects.get(pk=pk)

    if request.method == 'POST':
        # Get the form data
        member = request.POST.get('member')

        # Call the addMember method on the contract
        tx_hash = contract.functions.addMember(pk, member).transact()

        # Update the Contract object in the database
        c.members.append(member)
        c.tx_hash = tx_hash
        c.save()

        # Redirect to the contract detail page
        return redirect('contract_detail', pk=pk)

    # Render the add member form
    return render(request, 'add_member.html', {'contract': c})