from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
import json
from django.contrib.auth import authenticate, login, logout
from .models import Person
from django.contrib.auth.models import User as us
from .models import mods, Streets, Route_Street, Routes


# Create your views here.


def main(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/dms/login/')
    else:
        print('It doesn\'t work')
    return render(request, 'dms/index.html')


def api(request):
    if request.method == 'POST':
        print('getting post')
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        what = data['what']
        if what == 'update':
            item = mods[data['name']].objects.get(id=data['id'])
            setattr(item, data['header'], data['value'])
            try:
                item.save()
            except Exception as e:
                return HttpResponse(e, status=220)
            return HttpResponse('All is ok')
        if what == 'insert':
            try:
                new_item = mods[data['name']]()
                for i in range(len(data['headers'])):
                    setattr(new_item, data['headers'][i], data['values'][i])
                new_item.save()
                return HttpResponse(new_item.id)
            except Exception as e:
                return HttpResponse(e, status=221)
        if what == 'delete':
            item = mods[data['name']].objects.get(pk=data['id'])
            print(item)
            item.delete()
            return HttpResponse(status=200)
        if what == 'addroute':
            new_route = Routes(time_arrive=data['time_arrive'], time_departure=data['time_departure'],
                               route_owner=Person.objects.get(id=data['personId']), type=data['type'])
            new_route.save()
            for street in data['streets']:
                print(street)
                Route_Street(street=Streets.objects.get(id=street), route=new_route).save()
            return HttpResponse('Route added')
        return HttpResponse('post')

    if request.method == 'GET':
        print(request.GET)
        what = request.GET['what']
        print(what)
        if what == 'links':
            with connection.cursor() as c:
                query = "select TABLE_NAME from INFORMATION_SCHEMA.TABLES where TABLE_NAME like '%dms%'"
                c.execute(query)
                table_names = [a[0] for a in c.fetchall()]
                print(table_names)
                return HttpResponse(json.dumps([{'name': name} for name in table_names]))
        if what == 'table':
            try:
                answer = {'name': request.GET['name'],
                          'headers': [*list(mods[request.GET['name']].objects.values()[0])][1:],
                          'rows': [{'id': a[0], 'cells':[str(item) for item in a[1:]]}
                                   for a in mods[request.GET['name']].objects.values_list()]}
                return HttpResponse(json.dumps(answer))
            except IndexError:
                with connection.cursor() as c:
                    query = "select * from {} order by id desc limit 1".format(request.GET['name'])
                    c.execute(query)
                answer = {'name': request.GET['name'],
                          'headers': [a[0] for a in c.description][1:]}
                return HttpResponse(json.dumps(answer))
        if what == 'search':
            with connection.cursor() as c:
                query = "select TABLE_NAME from INFORMATION_SCHEMA.TABLES where TABLE_NAME like '%dms%'"
                c.execute(query)
                table_names = [a[0] for a in c.fetchall()]
                tables = []
                for table_name in table_names:
                    query = "select * from {} order by id desc limit 1".format(table_name)
                    c.execute(query)
                    table_answer_rows = []
                    columns = [col[0] for col in c.description]
                    for column in columns:
                        if column == 'id':
                            continue
                        query = "select * from {} where {} like '%{}%'".format(table_name, column, request.GET['value'])
                        c.execute(query)
                        rows = list(c.fetchall())
                        rows = [{'id': row[0], 'cells': [str(item) for item in row[1:]]} for row in rows]
                        table_answer_rows += rows
                    if table_answer_rows:
                        tables.append({'name': table_name, 'rows': table_answer_rows})
                return HttpResponse(json.dumps(tables))
        if what == 'streets':
            return HttpResponse(json.dumps(list(Streets.objects.values())))
        if what == 'persons':
            return HttpResponse(json.dumps([{'id': person['id'], 'first_name': person['first_name'],
                                             'last_name': person['last_name']} for person in Person.objects.values()]))
        if what == 'person_routes':
            data = [
                {'first_name': person.first_name,
                 'last_name': person.last_name,
                 'routes': [{'streets': [street.street_name for street in route.streets.all()],
                             'time_departure': str(route.time_departure),
                             'time_arrive': str(route.time_arrive),
                             'type': route.type}
                            for route in Routes.objects.filter(route_owner=person)]
                 } for person in Person.objects.all()]
            print(data)
            return HttpResponse(json.dumps(data))


def adduser_form(request):
    a = request.POST
    print(a)
    person = Person(first_name=a['first_name'], last_name=a['last_name'], date_of_birth=a['date_of_birth'])
    person.save()
    return HttpResponseRedirect('/dms/main')


def auth(request):
    print('hjkl')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/dms/main')
    else:
        return HttpResponseRedirect('/dms/login')


def login_page(request):
    return render_to_response('dms/login.html')


def reg(request):
    username, password = request.POST['username'], request.POST['password']
    print(username, ' ', password)
    user = us.objects.create_user(username, 'example@ex.ua', password)
    print(user)
    user.save()
    return HttpResponseRedirect('/dms/login/')


def registration_page(request):
    return render_to_response('dms/registration.html')

def lgout(request):
    logout(request)
    return HttpResponseRedirect('/dms/login/')

def addstreet_form(request):
    Streets(street_name=request.POST['street_name']).save()
    return HttpResponseRedirect('/dms/main')
