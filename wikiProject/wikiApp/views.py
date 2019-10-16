from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SearchBarForm, NewEntryForm, NewUserForm, RelatedEntryForm
from .models import NewEntryModel, RelatedEntryModel

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

# Creating a sign up user
def new_user(request):
    if request.method == "POST":
        newUser = NewUserForm(request.POST)
        if newUser.is_valid():
            logInUser = User.objects.create_user(username=request.POST['username'],
                                                 password=request.POST['password'])
            login(request, logInUser)
            return redirect("index")
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


def log_me_out(request):
    logout(request)
    return redirect("index")


def newEntry(request):
    #________________________ CREATE NEW ENTRIES ________________________#

    if request.method == "POST":
        print(request.POST)
        form = NewEntryForm(request.POST)
        if form.is_valid():
            tempImageFile = request.FILES
            if not tempImageFile:
                tempImageFile = ''
            else:
                tempImageFile = tempImageFile["Entry_FileUpload"]
            doc = NewEntryModel(Entry_Title=request.POST['Entry_Title'], Entry_Text=request.POST['Entry_Text'], Entry_FileUpload = tempImageFile,foreignKeyUser = request.user)
            doc.save()
        return render(request, "wikiApp/index.html")

    context = {
         'form': NewEntryForm(),

        }
    return render(request, "wikiApp/newEntry.html", context)


def edit(request, pk):
    entry = get_object_or_404(NewEntryModel, pk=pk)
    form = NewEntryForm(request.POST or None, instance = entry)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('yourWikiEntries')
    context = {'form': form,
                   "allRelatedEntries": RelatedEntryModel.objects.filter(RelatedforeignKeyUser = entry),
               'pk': pk


                   }
    return render(request, 'wikiApp/edit.html', context)


def delete(request, pk):
    entry = get_object_or_404(NewEntryModel, pk=pk)
    entry.delete()
    return redirect('yourWikiEntries')


def yourWikiEntries(request):
    if request.user.is_authenticated:

        context = {
            "allEntries": NewEntryModel.objects.filter(foreignKeyUser=request.user),

        }
        print(context)
        return render(request, 'wikiApp/yourWikiEntries.html', context)
    else:
        context = {
            "Message_Please_login": "Please Log in to see all your entries"
        }
        return render(request, 'wikiApp/yourWikiEntries.html', context)



#________________________ CREATE RELATED ENTRIES ________________________#

def relatedEntries(request,pk):
    if request.method == "POST":
        print(request.POST)
        relatedform = RelatedEntryForm(request.POST)
        if relatedform.is_valid():
            tempImageFile = request.FILES
            if not tempImageFile:
                tempImageFile = ''
            else:
                tempImageFile = tempImageFile["Related_FileUpload"]

            doc = RelatedEntryModel(Related_Title=request.POST['Related_Title'], Related_Text=request.POST['Related_Text'], Related_FileUpload = tempImageFile,RelatedforeignKeyUser = get_object_or_404(NewEntryModel, pk=pk))
            doc.save()
        return redirect ('edit', pk)

    context = {
        'relatedform': RelatedEntryForm()
    }
    return render(request, "wikiApp/relatedEntries.html", context)


