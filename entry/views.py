from os import replace
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from django.core.serializers import serialize

from .models import Orders, Business, Offices, Plans, Stocks, Customers
from .forms import crearUserForm, orderForm, customerForm
from .decorators import *

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import connection

from django.core.paginator import Paginator

import datetime

##########    login     ##########


@unauthenticated_user
def registerPage(request):
    form = crearUserForm()
    if request.method == 'POST':
        form = crearUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user.__dict__)
            try:
                group = Group.objects.get(name='manager')
                user.groups.add(group)
                nb = Business.objects.create(
                    bs=user, email=user.email, name=user.username)
                p_id = Plans.objects.get(plan_id=1)
                Offices.objects.create(
                    business=nb, plan=p_id, desc=f'main office {user.username}')
                return redirect('login')
            except ObjectDoesNotExist:
                print("Oops! Group Not found!")
                return HttpResponseNotFound('Oops! Group Not found!')
    context = {'form': form}
    return render(request, 'register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'usuario o pass incorrecto')
    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

##########    Profile     ##########


@login_required(login_url='login')
def getProfile(request):
    user = request.user
    id = user.business.id
    Bus = Business.objects.get(id=id)
    Ofi = Offices.objects.get(business_id=id)
    context = {'Bus': Bus, 'Ofi': Ofi}
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def edit(request):
    user = request.user
    id = user.business.id
    Bus = Business.objects.get(id=id)
    Ofi = Offices.objects.get(business_id=id)
    if request.method == 'POST':
        bs = request.POST.get('bs')
        te = request.POST.get('te')
        ma = request.POST.get('ma')
        try:
            Business.objects.filter(id=id).update(name=bs, tel=te, email=ma)
            return redirect('profile')
        except Exception as e:
            print("cant delete", e)
    context = {'Bus': Bus, 'Ofi': Ofi}
    return render(request, 'edit.html', context)

##########    Plans     ##########


@login_required(login_url='login')
def get_plans(request, id):
    ofi_id = id
    Ofi = Offices.objects.get(ofi_id=id)
    pl = Plans.objects.all().order_by('plan_id')
    context = {'Plans': pl, 'ofi_id': ofi_id, 'Ofi': Ofi}
    return render(request, 'plans.html', context)


@login_required(login_url='login')
def set_plans(request):
    plan = request.GET.get('id')
    office = request.GET.get('ofi')
    cantidad = request.GET.get('quantity')
    existing = Stocks.objects.filter(office=office)
    existing.delete()
    if plan == '1':
        c = connection.cursor()
        try:
            c.execute("BEGIN")
            c.execute("CALL insert_stock_1('{0}','{1}','{2}');".format(
                office, plan, cantidad))
            c.execute("COMMIT")
        finally:
            c.close()
        data = {'message': 'plan 1 ok', }
        return JsonResponse(data)
    elif plan == '2':
        c = connection.cursor()
        try:
            c.execute("BEGIN")
            c.execute("CALL insert_stock_2('{0}','{1}','{2}');".format(
                office, plan, cantidad))
            c.execute("COMMIT")
        finally:
            c.close()
        data = {'message': 'plan 2 ok', }
        return JsonResponse(data)
    else:
        c = connection.cursor()
        try:
            c.execute("BEGIN")
            c.execute("CALL insert_stock_3('{0}','{1}','{2}');".format(
                office, plan, cantidad))
            c.execute("COMMIT")
        finally:
            c.close()
    data = {'message': 'plan 3 ok', }
    return JsonResponse(data)

##########    Stocks     ##########


@login_required(login_url='login')
def get_stocks(request, id):
    ofi = id
    Ofi = Offices.objects.get(ofi_id=id)
    today = datetime.date.today()
    existing = Stocks.objects.filter(
        office=ofi, st_date__gte=today).order_by('st_date', 'st_time')
    paginator = Paginator(existing, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'Stocks': page_obj, 'Ofi': Ofi}
    return render(request, 'stocks.html', context)


##########    Orders     ##########


@login_required(login_url='login')
def getOrder(request, id):
    Ofi = Offices.objects.get(ofi_id=id)
    today = datetime.date.today()
    existing = Orders.objects.filter(
        office=id, odate__gte=today).order_by('odate', 'otime')
    paginator = Paginator(existing, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    try:
        print(existing[0].office)
    except:
        print("no data")
    context = {'Orders': page_obj, 'Ofi': Ofi}
    return render(request, 'orders.html', context)


def delete_order(request, id):
    try:
        dl = Orders.objects.get(order_id=id)
        of = dl.office.ofi_id
        print('\033[91m' + str(dl), str(of) + '\033[0m')
        if Stocks.objects.filter(office=of, st_date=dl.odate, st_time=dl.otime):
            ast = Stocks.objects.filter(
                office=of, st_date=dl.odate, st_time=dl.otime)[0].qt + 1
            print(ast, "ast")
            Stocks.objects.filter(
                office=of, st_date=dl.odate, st_time=dl.otime).update(qt=ast)
        dl.delete()
    except Exception as e:
        print("cant delete", e)
    return redirect('get_orders', of)


def add_orders(request):
    ofi = request.GET.get('of')
    dat = request.GET.get('date')
    tim = request.GET.get('time')
    id = Offices.objects.get(desc=ofi)
    cust = Customers.objects.get(customer_id=1)
    checkStock = Stocks.objects.get(st_date=dat, st_time=tim, office=id)
    if checkStock.qt > 0:
        try:
            Orders.objects.create(
                office=id, customer=cust, odate=dat, otime=tim)
            ast = Stocks.objects.filter(
                st_date=dat, st_time=tim, office=id)[0].qt - 1
            temp = Stocks.objects.get(st_date=dat, st_time=tim, office=id)
            temp.qt = ast
            temp.save()
        except:
            print("no se pudo guardar")
    return redirect('get_orders', id=id.ofi_id)


############  customer view #############


def cus_view(request):
    return render(request, 'customer.html')


def customer_view(request, id):
    office = Offices.objects.get(ofi_id=id)
    form2 = customerForm()
    form = orderForm()
    context = {'formCustomer': form2, 'formOrder': form, 'ofi': office}
    return render(request, 'customer-form.html', context)


def my_ticket(request):
    hoy = datetime.datetime.today()
    if request.method == 'POST':
        username = request.POST.get('username')
        ordenes = Orders.objects.select_related('customer').filter(
            customer__email=username, odate__gte=hoy).order_by('-odate')[:5]
        print(ordenes)
        return render(request, 'my-ticket.html', {'ordenes': ordenes})
    return render(request, 'my-ticket.html')


######### ajax ##############

def get_date(request):
    ofi = request.GET.get('ofi')
    today = datetime.datetime.today()

    st = Stocks.objects.filter(
        office=ofi, st_date__gte=today).distinct('st_date')
    qs_json = serialize('json', st)
    return HttpResponse(qs_json, content_type='application/json')


def get_time(request):
    st_id = request.GET.get('st_id')
    stid = Stocks.objects.get(st_id=st_id)
    st = Stocks.objects.filter(st_date=stid.st_date)
    lista = []
    for s in st:
        if s.qt > 0:
            print(s.qt)
            lista.append(s)
    return render(request, 'dd_otime.html', {'st': lista})


def save_customer(request):
    if request.method == 'POST':
        form = customerForm(request.POST)
        if form.is_valid():
            form.save()
            data = {'message': 'saved customer'}
    return JsonResponse(data)


def add_customer_or(request):
    ofi = request.POST.get('office')
    dat = request.POST.get('dat')
    stock_id = request.POST.get('tim')
    cus = request.POST.get('cus')
    checkStock = Stocks.objects.get(st_id=stock_id).qt
    if checkStock > 0:
        desc = Offices.objects.get(ofi_id=ofi)
        cust = Customers.objects.filter(email=cus).order_by('-customer_id')[0]
        print('\033[91m' + str(cust) + '\033[0m')
        temp = Stocks.objects.get(st_id=stock_id)
        Orders.objects.create(office=desc, customer=cust,
                              odate=dat, otime=temp.st_time)
        ast = Stocks.objects.filter(
            st_date=dat, st_time=temp.st_time, office=ofi)[0].qt - 1
        Stocks.objects.filter(st_date=dat, st_time=temp.st_time).update(qt=ast)
    data = {'message': 'saved order'}
    return JsonResponse(data)
