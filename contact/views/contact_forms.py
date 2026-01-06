from django.shortcuts import render, redirect, get_list_or_404
from contact.forms import ContactForm
from contact.models import Contact
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='contact:login')
def create(request):
    form_action = reverse('contact:create')
    context = {
        'form': ContactForm(),
        'form_action': form_action
    }

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        context = {
            'form': form,
            'form_action': form_action
        }
        if form.is_valid():
            # form.save()
            contact = form.save(commit=False)
            contact.show = True
            contact.owner = request.user
            contact.save()
            return redirect('contact:update', contact_id=contact.pk)

    return render(request, 'contact/create.html', context)


@login_required(login_url='contact:login')
def update(request, contact_id):
    contact = get_list_or_404(Contact, id=contact_id, show=True,
                              owner=request.user)[0]
    form_action = reverse('contact:update', args=(contact_id,))
    context = {
        'form': ContactForm(instance=contact),
        'form_action': form_action
    }

    print(f'{request.method} request.method')

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        context = {
            'form': form,
            'form_action': form_action
        }
        if form.is_valid():
            # form.save()
            contact = form.save(commit=False)
            contact.show = True
            contact.save()
            return redirect('contact:update', contact_id=contact.pk)

    return render(request, 'contact/create.html', context)


@login_required(login_url='contact:login')
def delete(request, contact_id):
    contact = get_list_or_404(Contact, id=contact_id, owner=request.user,
                              show=True)[0]

    confirmation = request.POST.get('confirmation', 'no')

    if confirmation == 'yes':
        contact.delete()
        return redirect('contact:index')

    return render(request, 'contact/contact.html', context={
        'contact': contact,
        'confirmation': confirmation
    })
