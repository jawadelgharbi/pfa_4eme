from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from AiMark.forms import MyMarkForm, MyMarkForm
from AiMark.models import MyMark, MyPoint


def home(request):
    if request.user.is_authenticated == True:
        # print(cv.__version__)
        lastmarks = MyMark.objects.filter(created_at=datetime.today())
        nbmarks = MyMark.objects.all().count()
        nbusers = User.objects.all().count()
        nbpoints = MyPoint.objects.all().count()
        greenmarks = MyMark.objects.filter(Q(gravity__lte=30) & Q(created_at=datetime.today())).count()
        yellowmarks = MyMark.objects.filter(
            Q(gravity__gt=30) & Q(gravity__lt=70) & Q(created_at=datetime.today())).count()
        redmarks = MyMark.objects.filter(Q(gravity__gte=70) & Q(created_at=datetime.today())).count()

        todaygravities = {'greenmarks': greenmarks, 'yellowmarks': yellowmarks, 'redmarks': redmarks}

        greenmarks = MyMark.objects.filter(gravity__lte=30).count()
        yellowmarks = MyMark.objects.filter(Q(gravity__gt=30) & Q(gravity__lt=70)).count()
        redmarks = MyMark.objects.filter(gravity__gte=70).count()
        gravitieschart = {'greenmarks': greenmarks, 'yellowmarks': yellowmarks, 'redmarks': redmarks}

        userchart = User.objects.select_related().annotate(nb=Count('marks'))
        data = {'lastmarks': lastmarks, 'nbmarks': nbmarks, 'gravitieschart': gravitieschart,
                'nbusers': nbusers, 'nbpoints': nbpoints, 'todaygravities': todaygravities,
                'userchart':userchart}

        return render(request, 'index.html', data)
    else:
        return redirect('/admins/login')


def index(request):
    if request.user.is_authenticated == False:
        return redirect('/admins/login')

    data = MyMark.objects.all()
    return render(request, 'index.html', {'data': data})


def ajouter(request):
    if request.user.is_authenticated == False:
        return redirect('/admins/login')

    if request.method == 'POST':
        form = MyMarkForm(request.POST, request.FILES)
        # form.user=request.user.id
        # form.created_at=datetime.date.today()
        if form.is_valid():
            mark = MyMark(utilisateur=User.objects.get(id=request.user.id), nom=form.cleaned_data['nom']
                        , desctiption=form.cleaned_data['desctiption'], image=form.cleaned_data['image']
                        , gravit=form.cleaned_data['gravit'] * 10, date=datetime.today())
            mark.save()

            return redirect('/admins/marks/edit/' + str(mark.id))
        else:
            return render(request, 'ajouter.html', {'form': form})

    else:
        form = MyMarkForm()
        return render(request, 'ajouter.html', {'form': form})


def modifier(request, id):
    if request.user.is_authenticated == False:
        return redirect('/admins/login')

    mark = MyMark.objects.get(id=id)
    if request.method == 'POST':
        form = MyMarkForm(request.POST, request.FILES)
        if form.is_valid():

            # mark.user = request.user.id
            mark.nom = form.cleaned_data['nom']
            mark.desctiption = form.cleaned_data['desctiption']
            if form.cleaned_data['image']:
                mark.image = form.cleaned_data['image']

            mark.gravity = form.cleaned_data['gravit'] * 10

            mark.save()

            return redirect('/admins/marks/edit/' + str(id))
        else:
            return render(request, 'modifier.html', {'form': form})

    else:
        form = MyMarkForm(initial={
            'id': mark.id,
            'utilisateur': mark.utilisateur,
            'nom': mark.nom,
            'desctiption': mark.desctiption,
            'image': mark.image,
            'gravit': mark.gravit / 10,
            'date': mark.date,
        })
        points = MyPoint.objects.filter(mymark=id)

        return render(request, 'modifier.html', {'form': form, 'points': points})


def supprimer(request):
    if request.user.is_authenticated == False:
        return redirect('/admins/login')

    if request.method == 'POST':
        mark = MyMark.objects.get(id=request.POST['markid'])
        mark.delete()

    return redirect('/admins')


# def recherche(request):
#     if request.user.is_authenticated == False:
#         return redirect('/admins/login')
# 
#     data = MyMark.objects.filter(
#         Q(name__contains=request.GET['searchtext']) | Q(desctiption__contains=request.GET['searchtext']))
#     return render(request, 'mark/index.html', {'data': data})


def ajouterpoint(request, id):
    if request.user.is_authenticated == False:
        return redirect('/admins/login')

    if request.method == 'POST':
        # HttpResponse(request.POST['x'])
        point = MyPoint(mymark=MyMark.objects.get(id=id), numero=request.POST['count'], x=request.POST['x']
                      , y=request.POST['y'])
        point.save()
        return HttpResponse('good')
    else:
        return redirect('/admins/marks/')


def supprimerpoint(request, id):
    if request.user.is_authenticated == False:
        return redirect('/admins/login')

    if request.method == 'POST':
        # HttpResponse(request.POST['x'])
        MyPoint.objects.filter(mymark=id).delete()
        return redirect('/admins/marks/edit/' + str(id))


