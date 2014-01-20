# RCA-specific extensions to Verdant admin.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.models import UserPagePermissionsProxy

from rca.models import RcaNowPage, RcaNowIndex, StudentPage

def find_rca_now_index_page(user):
    """Look for the RCA Now index page: a page of type RcaNowIndex where this user can add pages"""
    user_perms = UserPagePermissionsProxy(user)

    for page in RcaNowIndex.objects.all():
        if user_perms.for_page(page).can_add_subpage():
            return page

    raise Exception('No usable RCA Now section found (using the RcaNowIndex page type and with add permission for students)')

@login_required
def rca_now_index(request):
    index_page = find_rca_now_index_page(request.user)

    pages = RcaNowPage.objects.filter(owner=request.user)
    return render(request, 'rca/admin/rca_now_index.html', {
        'rca_now_index': index_page,
        'hide_actions': ('move', 'add_subpage'),
        'pages': pages,
    })

@login_required
def student_page_index(request):
    # look for StudentPages owned by this user
    pages = StudentPage.objects.filter(owner=request.user)

    if not pages:
        index_page = find_rca_now_index_page(request.user)

        # Redirect to the interface for adding a StudentPage in this section
        return redirect('verdantadmin_pages_create', 'rca', 'studentpage', index_page.id)

    elif len(pages) == 1:
        # redirect them to edit their existing student page
        return redirect('verdantadmin_pages_edit', pages[0].id)

    else:
        return render(request, 'rca/admin/select_student_page.html', {
            'pages': pages,
            'hide_actions': ('move', 'add_subpage'),
        })
