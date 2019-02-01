import operator
from datetime import datetime,timedelta
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
import os

def loginpage(request):
	token = Token.objects.create(timetokenPlaced=datetime.datetime.now())
	context={'tokenNum':token.tokenNum}
	print(context)
	return render(request,"login.html",context)


def menu(request,tokenNum,category):
	#for already added items
	try:
		intTokenNum = int(tokenNum)
		token = Token.objects.get(tokenNum = intTokenNum)			#got the token object

		addedItems = TokenItem.objects.filter(tokens = token)

		if(category == 'VEGONLY'):
			MenuItems = Menu.objects.filter(isVeg = True,isEnabled=True)
			addedMenuItems =[]
			#print("\n\n\n\n\n\n")
			for a in addedItems:
				addedMenuItems.append({'itemNum':a.menu.itemNum,'quantity':a.quantity})
			#print(addedMenuItems)
			context={'isVeg':True,'MenuItems':MenuItems,'tokenNum':tokenNum,'addedMenuItems':addedMenuItems}
			return render(request,"menu.html",context)

		elif(category == 'ALL'):
			MenuItems = Menu.objects.filter(isEnabled=True)
			addedMenuItems =[]
			#print("\n\n\n\n\n\n")
			for a in addedItems:
				addedMenuItems.append({'itemNum':a.menu.itemNum,'quantity':a.quantity})
			#print(addedMenuItems)
			context={'isVeg':False,'MenuItems':MenuItems,'tokenNum':tokenNum,'addedMenuItems':addedMenuItems}
			return render(request,"menu.html",context)
	except:
		context = {'tokenNum':intTokenNum}
		return render(request,"UCannotGoThere.html",context)

@csrf_exempt
def menuConfirmation(request,tokenNum):
	# print(request,orderId)
	intTokenNum = int(tokenNum)
	token = Token.objects.get(tokenNum = intTokenNum)			#got the token object

	confirmationItems = TokenItem.objects.filter(tokens = token)

	confirmedList = []
	for c in confirmationItems:
		d = {
		'itemNum':c.menu.itemNum,
		'itemName':c.menu.itemName,
		'quantity':c.quantity,
		'price':round(c.menu.itemUnitPrice * c.quantity,2),
		'image':c.menu.itemImageName}
		confirmedList.append(d)

	confirmedList.sort(key=operator.itemgetter('itemNum'))
	# list of the order items with given orderId
	context={'confirmationList':confirmedList}
	# return render(request,"confirm.html",context)
	return JsonResponse(confirmedList,safe=False)


#call this to update orders total amount 
def updateTokenListAmount(tokenNum):
	try:
		token = Token.objects.get(tokenNum = tokenNum)

		confirmationItems = TokenItem.objects.filter(tokens = token)		#get all orderItems
		totalAmount = 0

		for c in confirmationItems:
			totalAmount += round(c.menu.itemUnitPrice * c.quantity,2)

		token.totalAmount = totalAmount
		token.save()
		return token
	except:
		return None


def placeOrder(request):
	tokenNum = request.POST.get('tokenNum',False)
	print(tokenNum)
	if(tokenNum != False):
		intTokenNum = int(tokenNum)
		try:
			t=updateTokenListAmount(intTokenNum)				#final update to token totalAmount

			token = Token.objects.get(tokenNum = intTokenNum)
			tokenItem = TokenItem.objects.filter(tokens = token)
		
			orderList = OrderList.objects.create(tokenNum = token.tokenNum,totalAmount = token.totalAmount,timeOrderPlaced = datetime.datetime.now())
			for item in tokenItem : 
				OrderedItem.objects.create(orderList=orderList,menu=item.menu,quantity=item.quantity,price=round(item.menu.itemUnitPrice*item.quantity,2))
			token.delete()

		except:
			orderList = OrderList.objects.get(tokenNum = intTokenNum)
		finally:
			confirmationItems = OrderedItem.objects.filter(orderList = orderList)
			confirmedList = []
			for c in confirmationItems:
				d = {
				'itemNum':c.menu.itemNum,
				'itemName':c.menu.itemName,
				'quantity':c.quantity,
				'price':round(c.menu.itemUnitPrice * c.quantity,2),
				'image':c.menu.itemImageName}
				confirmedList.append(d)
			
			confirmedList.sort(key=operator.itemgetter('itemNum'))
			# list of the order items with given orderId
			estimatedTimeOfDelivery = orderList.timeOrderPlaced+timedelta(minutes=5)
			context={'confirmationList':confirmedList,'orderId':orderList.orderNum,'isEmpty':False,
			'timeOrderPlaced':str(orderList.timeOrderPlaced),'estimatedTimeOfDelivery':str(estimatedTimeOfDelivery),'total':round(orderList.totalAmount,2)}

			if len(confirmationItems) == 0 :
				context['isEmpty'] = True

			# return render(request,"confirm.html",context)
			return render(request,"orderAck.html",context)
	else:
		htmlToSend = """<html><h1>An exception occured as the server restarted and/or the Http request sent to the server was invalid...
						<br>
						Sorry for the Inconvience</h1>
						<h2>You can try to go back to previous page(s) and reload to return to acknowledgement page.</h2>
						</html>"""
		return HttpResponse(htmlToSend)
@csrf_exempt
def orderCompleted(request,orderId):
	try:
		o = OrderList.objects.get(orderNum = int(orderId))
		return HttpResponse(200)
	except:
		return HttpResponse(201)


@csrf_exempt
def getWeight(request):
	print(request.body.decode())

	recieved_request = json.loads(request.body.decode())
	tokenNum = int(recieved_request['tokenNum'])
	itemNum = int(recieved_request['itemNum'])
	
	#to read from weight.txt file stored in the project root folder
	Project_root = os.path.dirname(os.path.dirname(__file__))
		
	with open(Project_root+"/weightBuffer.txt","r") as file:
		weight = float(file.read())
		file.close()
	print(weight)
	try:
		

		token = Token.objects.get(tokenNum = tokenNum)
		itemObj = Menu.objects.get(itemNum = itemNum)

		tokenItem,create = TokenItem.objects.get_or_create(
		tokens = token,
		menu = itemObj, 
		)
		tokenItem.quantity = weight
		tokenItem.save()

		if(weight==0.0):
			tokenItem.delete()
			print("deleted item"+str(itemNum))

		token=updateTokenListAmount(tokenNum)

		return HttpResponse(weight)
	except:
		return HttpResponse(-1)


@csrf_exempt
def removeWeight(request):
	print(request.body.decode())
	recieved_request = json.loads(request.body)
	tokenNum = int(recieved_request['tokenNum'])
	itemNum = int(recieved_request['itemNum'])
	
	try:
		token = Token.objects.get(tokenNum = tokenNum)
		itemObj = Menu.objects.get(itemNum = itemNum)

		tokenItem = TokenItem.objects.get(
		tokens = token,
		menu = itemObj, 
		)
		tokenItem.delete()
		print("deleted item"+str(itemNum))

		token=updateTokenListAmount(tokenNum)

		return HttpResponse(0)
	except:
		return HttpResponse(-1)


def printBill(request):
	orderId = request.POST.get('orderId',False)
	if(orderId != False):
		orderListObj = OrderList.objects.get(orderNum = orderId)
		orderItems = OrderedItem.objects.filter(orderList = orderListObj)
		context={'orderItems':orderItems,'orderListObj':orderListObj}
	return render(request,"printBill.html",context)




























#------------------------------------extra---------------------------------------------------
@csrf_exempt
def ack(request):
	token = Token.objects.get(tokenNum = intTokenNum)

	itemObj = Menu.objects.get(itemNum = itemNo)

	tokenItem,create = TokenItem.objects.get_or_create(
		tokens = token,
		menu = itemObj, 
		)
	
	tokenItem.quantity = int(qty)
	tokenItem.save()
	
	#x =  Menu.objects.get(itemNum = itemNo)
	print(tokenNum,itemNo,qty)

	if(qty==str(0)):
		tokenItem.delete()
		print("deleted")

	token=updateTokenListAmount(intTokenNum)   #OR TOKEN LIST AMOUNT
 	# orderItem.price = int(qty) * int(x.itemUnitPrice)
	# orderItem.save()
	# to update orderList.totalAmount
	# if(qty==str(0)):
	# 	orderItem.delete()
	#	# Updating OrderList object
	# o = OrderItem.objects.filter(orderList = orderListObj)
	# total=0
	# for item in o:
	# 	total += item.price
	# orderListObj.totalAmount = total
	# orderListObj.save()
	return HttpResponse(token.totalAmount)
