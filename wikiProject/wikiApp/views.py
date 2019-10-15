from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SearchBarForm, NewEntryForm, NewUserForm
from .models import  NewEntryModel

# Create your views here.
from django.http import HttpResponse


def index(request):
    entry_list = NewEntryModel.objects.all()
    searchform = SearchBarForm(request.POST or None)
    if request.method == "POST":
        if searchform.is_valid():
            searchform.save(commit=True)
        return redirect('index')
    return render(request, 'wikiApp/index.html',{'searchform': searchform,
                                                 'entry_list': entry_list })


def new_user(request):
    if request.method == "POST":
        newUser = NewUserForm(request.POST)
        if newUser.is_valid():
            logInUser = User.objects.create_user(username=request.POST['username'],
                                                 password=request.POST['password'])
            login(request, logInUser)
            return redirect("yourWikiEntries")
        else:
            context = {
                "errors": newUser.errors,
                "form": NewUserForm(),
            }
            return render(request, 'wikiApp/index.html', context)
    else:
        context = {
            "form": NewUserForm()
        }
        return render(request, 'wikiApp/new_user.html', context)


def login_my_user(request):
    if request.method == "POST":
        print(NewUserForm)
        loginUser = authenticate(username=request.POST['username'], password=request.POST["password"])
        if loginUser is not None:
            login(request, loginUser)
            return redirect("index")
    else:
        messages.error(request, "Wrong username or password")
        context = {
            "loginform": NewUserForm,
        }
        return render(request, 'wikiApp/login_my_user.html',context)


def newEntry(request):

    if request.method == "POST":
        print(request.POST)
        form = NewEntryForm(request.POST)
        if form.is_valid():
            form.save()
            tempImageFile = request.FILES
            if not tempImageFile:
                tempImageFile = ''
            else:
                tempImageFile = tempImageFile["Entry_FileUpload"]
            doc = NewEntryModel(Entry_Title=request.POST['Entry_Title'], Entry_Text=request.POST['Entry_Text'], Entry_FileUpload = tempImageFile,)
            doc.save()
        return render(request, "wikiApp/index.html")
    else:
        context = {
            'form': NewEntryForm()
        }
    return render(request, "wikiApp/newEntry.html", context)



def display(request):

    return render(request,'wikiApp/index.html',{})


def edit(request, pk):
    entry = get_object_or_404(NewEntryModel, pk=pk)
    form = NewEntryForm(request.POST or None, instance=entry)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'wikiApp/index.html', {'form': form})



def delete(request, pk):
    entry = get_object_or_404(NewEntryModel, pk=pk)
    entry.delete()
    return redirect('index')








#
# def newEntry(request):
#     if request.method == "POST":
#         print(request.POST)
#         entry_form = NewEntryForm(request.POST)
#         if entry_form.is_valid():
#             entry_form.save()
#
#
#
#             return redirect('index')
#
#     return render(request, "wikiApp/newEntry.html", {'entry_form': NewEntryForm})



def yourWikiEntries(request):
    form = SearchBarForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save(commit=True)
    return render(request, 'wikiApp/yourWikiEntries.html', {'form': form})
