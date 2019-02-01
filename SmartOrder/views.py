import operator
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from customer.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

#-----------------------------RESTAURANT SIDE-------------------------------
@login_required(login_url='managerLogin')
def currentOrderList(request):
	# try:
	orders = OrderList.objects.filter(isCompleted=False)			#use get to remove isfinished
	orderNumbers = []
	orderObjectList = []

	for o in orders:
		orderNumbers.append(o.orderNum)
		orderObjectList.append(o)

	currentOrderItems = []

	for oListNum in orderObjectList:
		items = OrderedItem.objects.filter(orderList = oListNum)
		if items :
			orderSet = {'orderNum':oListNum.orderNum,'items':items,'total':oListNum.totalAmount,
			'timeOrderPlaced':oListNum.timeOrderPlaced}
			currentOrderItems.append(orderSet)
	
	# currentOrderItems.sort(key=operator.itemgetter('timeOrderPlaced'),reverse=True)
	
	context = {'currentOrderItems':currentOrderItems}
	return render(request,"currentOrders.html",context)
	# except:
	# 	return render(request,"currentOrders.html",{})


@login_required(login_url='managerLogin')
def showHistory(request):
	# try:
	history = History.objects.all().order_by("timeStamp")
	orderNumbers = []

	for h in history:
		if(h.orderNum not in orderNumbers):
			orderNumbers.append(h.orderNum)


	orderItems = []
	for oListNum in orderNumbers:
		items = History.objects.filter(orderNum = oListNum)
		total=0
		if items:
			for i in items:
				total += i.price

			orderSet = {'orderNum':oListNum,'items':items,'time':items[0].timeStamp,'total':total}
			orderItems.append(orderSet)


	context = {'orderItems':orderItems}
	return render(request,"history.html",context)

@csrf_exempt
def orderCompleted(request):
	orderNo = request.POST['orderNum']
	print(orderNo)
	orderCompleted = OrderList.objects.get(orderNum = orderNo)
	# orderToBeDeleted.delete()
	orderCompleted.isCompleted = True
	orderCompleted.save()
	y = OrderedItem.objects.filter(orderList = orderCompleted)

	for i in y:
		h = History(orderNum = orderCompleted.orderNum)
		h.itemNum = i.menu.itemNum
		h.itemName = i.menu.itemName
		h.price = i.price
		h.quantity = i.quantity
		h.timeStamp = datetime.datetime.now()
		h.save()
		print("Added to history : " + str(h.orderNum)+" "+str(h.timeStamp)+" "+str(h.itemNum)+" "+str(h.price))

	return HttpResponse(200)

@login_required(login_url='managerLogin')
def addItemPrompt(request):
	return render(request,"addItem.html",{})

@login_required(login_url='managerLogin')
def addMenuItem(request):
	try:
		m=Menu.objects.create(itemName = request.POST['itemName'],
		itemDesc = request.POST['itemDesc'],
		itemUnitPrice = int(request.POST['itemUnitPrice']),
		itemImageName = request.POST['itemImageName'],
		)
		if(request.POST['veg'] == 'false'):
			m.isVeg = False
			m.save()

		if(request.POST['isenabled'] == 'false'):
			m.isEnabled = False
			m.save()

		return render(request,"itemAdded.html",{"ack":"The item you added has been saved!!!"})
	except:
		return render(request,"itemAdded.html",{"ack":"Please Enter Valid data!!!"})

@login_required(login_url='managerLogin')
def showMenuItems(request):
	m = Menu.objects.all()
	return render(request,"showMenuItems.html",{'menu':m})

@login_required(login_url='managerLogin')
def toggleItem(request,i):
	m = Menu.objects.get(itemNum = i)
	if(m.isEnabled == False):
		m.isEnabled = True
	else:
		m.isEnabled = False
	m.save()
	response = redirect('showMenuItems')
	return response
	
	# m1=Menu.objects.all()
	# return render(request,"showMenuItems.html",{'menu':m1})

@login_required(login_url='managerLogin')
def removeItem(request,i):
	m = Menu.objects.get(itemNum = i)
	m.delete()
	m1=Menu.objects.all()
	response = redirect('showMenuItems')
	return response

	# return render(request,"showMenuItems.html",{'menu':m1})


