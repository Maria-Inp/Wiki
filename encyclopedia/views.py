import random
import markdown
from . import util
from django import forms
from django.shortcuts import render


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title", widget=forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(label="Page Content", widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


def convert_to_HTML(title):
    entry = util.get_entry(title)
    html = markdown.markdown(entry) if entry else None

    return html


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entryPage = util.get_entry(title)

    if entryPage is None:
        return render(request, "encyclopedia/nonExistingEntry.html", {
            "entryTitle": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": convert_to_HTML(title),
            "entryTitle": title
        })


def randomPage(request):
    entries = util.list_entries()
    randomEntry = random.choice(entries)
    html = convert_to_HTML(randomEntry)
    return render(request, "encyclopedia/entry.html", {
        "entry": html,
        "entryTitle": randomEntry
    })


def newEntry(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if(util.get_entry(title) is None or form.cleaned_data['edit'] is True):
                util.save_entry(title, content)
                return render(request, "encyclopedia/entry.html", {
                    "entry": convert_to_HTML(title),
                    "entryTitle": title
                })
            else:
                return render(request, "encyclopedia/newEntry.html", {
                    "form": form,
                    "existing": True,
                    "entry": title
                })
        else:
            return render(request, "encyclopedia/newEntry.html", {
                "form": form,
                "existing": False
            })
    else:
        return render(request, "encyclopedia/newEntry.html", {
            "form": NewEntryForm(),
            "existing": False
        })


def edit(request, title):
    entryPage = util.get_entry(title)

    if entryPage is None:
        return render(request, "encyclopedia/nonExistingEntry.html", {
            "entryTitle": title
        })
    else:
        form = NewEntryForm()
        form.fields["title"].initial = title
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/newEntry.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "entryTitle": form.fields["title"].initial
        })


def search(request):
    value = request.POST['q']
    if (util.get_entry(value) is not None):
        return render(request, "encyclopedia/entry.html", {
            "entry": convert_to_HTML(value),
            "entryTitle": value
        })    
    else:
        subStringEntries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subStringEntries.append(entry)
        if (len(subStringEntries) != 0):
            return render(request, "encyclopedia/index.html", {
                "entries": subStringEntries,
                "search": True,
                "value": value
            })
        else:
            return render(request, "encyclopedia/nonExistingEntry.html", {
                "entryTitle": value
        })
        


    