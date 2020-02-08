from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect
from django.shortcuts import get_list_or_404, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from .models import destination
from .models import package
from . import views

from .models import visaInfoFile

from math import ceil
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

auth = login_required(login_url='/sairweb/admin_signin/')
# Create your views here.
def test(request):
    if request.session.has_key('is_logged'):
        return render(request, 'test.html')
    return redirect('admin_signin')

def index(request):
    destinations= destination.objects.all()
    n = len(destinations)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))
    allpkg = []
    destpkgs = package.objects.values('pkg_dest_name', 'id') # getting all destination name against id
    pkgs = {item['pkg_dest_name'] for item in destpkgs} # getting all destination name without id
    print(pkgs)
    for pkg in pkgs:
        pk = package.objects.filter(pkg_dest_name=pkg) # in pk we ar soring the packages against destination
        n = len(pk)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allpkg.append([pk, range(1, nSlides), nSlides])
    params = {'no_of_slides': nSlides, 'range': range(1, nSlides), 'destination': destinations,'allpkg':allpkg, 'x':range(1,6)}
    return render(request,'index.html',params)

def packages(request,pid):
    packages = package.objects.filter(id=pid)
    params= {'packages':packages[0]}
    latests = package.objects.order_by('-pkg_created_date')[0:4] #latest 4 ta post show korbe
    params = {'packages': packages[0],'latests':latests}
    return render(request,'packages.html',params)


def about(request):
    #if request.session.has_key('is_logged'):
    return render(request, 'about.html')
    #return redirect('admin_signin')

def contact(request):
    return render(request,'contact.html')

#Destination_part

def destination_list(request):
    if request.session.has_key('is_logged'):
        destinations=destination.objects.all()
        params={'destination': destinations}
        return render(request,'destination_list.html',params)
    return redirect('admin_signin')

def add_destination(request):
    if request.session.has_key('is_logged'):
        if request.method == 'POST':
            form = destinationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('destination_list')
        else:
            form = destinationForm()
        return render(request, 'add_destination.html', {
            'form': form
        })
    return redirect('admin_signin')

def add_package(request):
    if request.session.has_key('is_logged'):
        if request.method == 'POST':
            form = packageForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('package_list')
        else:
            form = packageForm()
        return render(request, 'add_package.html', {
            'form': form
        })
    return redirect('admin_signin')

def package_list(request):
    if request.session.has_key('is_logged'):
        packages = package.objects.all()
        params = {'package': packages}
        return render(request, 'package_list.html', params)
    return redirect('admin_signin')

def delete_plist_info(request,lid):
    plist = package.objects.filter(id=lid)
    plist.delete()
    return redirect('package_list')


def edit_plist_info(request,lid):
    plists = package.objects.filter(id=lid)
    params = {'plist': plists}
    return render(request,'update_package.html',params)

def update_plist_info(request,lid):
    if request.method == 'POST':
        pkg_img = request.FILES.get('pkg_img')  # Use request.FILES

        pkg_name = request.POST.get('pkg_name')
        pkg_dest_name = request.POST.get('pkg_dest_name')
        pkg_rating = request.POST.get('pkg_rating')
        pkg_price = request.POST.get('pkg_price')
        pkg_desc = request.POST.get('pkg_desc')

        if 'pkg_img' in request.FILES :
            packages = package.objects.get(id=lid)
            packages.pkg_name = pkg_name
            packages.pkg_dest_name = pkg_dest_name
            packages.pkg_rating = pkg_rating
            packages.pkg_price = pkg_price
            packages.pkg_desc = pkg_desc
            packages.pkg_img = pkg_img
            packages.save()
        else:
            packages = package.objects.get(id=lid)
            packages.pkg_name = pkg_name
            packages.pkg_dest_name = pkg_dest_name
            packages.pkg_rating = pkg_rating
            packages.pkg_price = pkg_price
            packages.pkg_desc = pkg_desc
            packages.save()

    return redirect('package_list')

def admin_signin(request):
    return render(request, 'admin_signin.html')

def admin_signup(request):
    return render(request, 'admin_signup.html')

def signup(request):
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        obj = wadmin(username=username, email=email, password=password)
        obj.save()
        return redirect('/sairweb/admin_signup')


def signin(request):

    if request.POST:
        u_email = request.POST['email']
        u_password = request.POST['password']

        #strore value in session
        ob1 = wadmin.objects.get(email=u_email)
        request.session['username'] = ob1.username
        request.session['type'] = ob1.type

        # search in database
        count = wadmin.objects.filter(email=u_email, password=u_password).count()
        if count > 0:
            request.session['is_logged'] = True
            return redirect('wadmin_index')
        else:
            return redirect('/sairweb/admin_signin')

    return render(request, 'sairweb/admin_signin.html')

def logout(request):
    del request.session['is_logged']
    return redirect('/sairweb/admin_signin')

def wadmin_index(request):
    if request.session.has_key('is_logged'):
        if 'username' in request.session:
            username = request.session['username']
            type = request.session['type']
            params={'username':username,'type':type}
        return render(request, 'wadmin_index.html',params)
    return redirect('admin_signin')



def delete_dlist_info(request,lid):
    plist = destination.objects.filter(id=lid)
    plist.delete()
    return redirect('destination_list')


def edit_dlist_info(request,lid):
    plists = destination.objects.filter(id=lid)
    params = {'plist': plists}
    return render(request,'update_destination.html',params)

def update_dlist_info(request,lid):
    if request.method == 'POST':
        dest_img = request.FILES.get('dest_img')  # Use request.FILES
        dest_name = request.POST.get('dest_name')
        dest_desc = request.POST.get('dest_desc')

        if 'dest_img' in request.FILES :
            destinations = destination.objects.get(id=lid)
            destinations.dest_name = dest_name
            destinations.dest_img = dest_img
            destinations.dest_desc = dest_desc
            destinations.save()
        else:
            destinations = destination.objects.get(id=lid)
            destinations.dest_name = dest_name
            destinations.dest_desc = dest_desc
            destinations.save()

    return redirect('destination_list')

def visaTrackingEdit(request):
    if request.method == 'POST':
        form = visaInfoForm(request.POST)
        file_form = visaInfoFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('visa_img')  # field name in model
        if form.is_valid() and file_form.is_valid():
            visa_instance = form.save(commit=False)
            visa_instance.save()
            for f in files:
                visa_file_instance = visaInfoFile(visa_img=f, visaInfo=visa_instance)
                visa_file_instance.save()
            return redirect('visaTrackingEdit')
    else:
        form = visaInfoForm()
        file_form = visaInfoFileForm()
        latests = visaInfo.objects.latest('visa_id')
        newRef = latests.visa_id + 1
    return render(request, 'visaTrackingEdit.html', {'form': form,'file_form':file_form,'newRef':newRef})


def visaTrackingUpdate(request,vid):
    instance = get_object_or_404(visaInfo, visa_id=vid) # instance creating
    form = visaInfoForm(request.POST or None, instance=instance) # instance er against e form
    files = request.FILES.getlist('visa_img')
    if form.is_valid():
        form.save()
        for f in files:
            visa_file_instance = visaInfoFile(visa_img=f, visaInfo=instance) # instance er against e image upload
            visa_file_instance.save()
        return redirect('visaTrackingList')

def visa_Filedelete(request,vid,fid):
    instance = get_object_or_404(visaInfo, visa_id=vid) #visaId er against e instance create
    flist = visaInfoFile(id=fid, visaInfo=instance) # oi instance er against e file neya
    flist.delete() # file delete kore deya
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def visaTrackingView(request):
    if request.method == 'POST':
        visa_id = request.POST.get('visa_id')
        pass_no = request.POST.get('passport_no')

        try:
            visas = visaInfo.objects.get(passport_no=pass_no)
        except visaInfo.DoesNotExist:
            visas = None

        if visas!=None:
            if visas.visa_id==int(visa_id):
                params = {'visa': visas}
                return render(request, 'visaTrackingView.html', params)
            else:
                messages.info(request, 'Please insert correct Ref / Passport no')
                return redirect('visaTrackingUser')
        else:
            messages.info(request, 'Please input correct Ref / Passport no')
            return redirect('visaTrackingUser')
    else:
        return redirect('visaTrackingUser')

def visaTrackingUser(request):
    return render(request, 'visaTrackingUser.html')

def visaTrackingList(request):
    if request.session.has_key('is_logged'):
        visas = visaInfo.objects.all()
        params = {'visa': visas}
        return render(request, 'visaTrackingList.html', params)
    return redirect('admin_signin')

def visaTrackingDelete(request,vid):
    visas = visaInfo.objects.filter(visa_id=vid)
    visas.delete()
    return redirect('visaTrackingList')

def visaTrackingUpdateView(request,vid):
    visas = visaInfo.objects.filter(visa_id=vid)
    #as visaInfoFile has a foreignkey of visaInfo
    visasFile = visaInfoFile.objects.filter(visaInfo=vid)
    print(visasFile)
    params = {'visa': visas,'visasFile': visasFile}
    return render(request,'visaTrackingUpdateView.html',params)


def packageShow(request):
    if request.method == 'POST':
        star5=request.POST.get('pstar5')
        star4=request.POST.get('pstar4')
        star3=request.POST.get('pstar3')
        star2=request.POST.get('pstar2')
        star1=request.POST.get('pstar1')

        destinations = destination.objects.all()
        n = len(destinations)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allpkg = []
        destpkgs = package.objects.values('pkg_dest_name', 'id')  # getting all destination name against id
        pkgs = {item['pkg_dest_name'] for item in destpkgs}  # getting all destination name without id
        print(pkgs)
        for pkg in pkgs:
            pk5 = package.objects.filter(pkg_dest_name=pkg, pkg_rating=star5) # in pk(1-5) we are sorting the packages against star
            pk4= package.objects.filter(pkg_dest_name=pkg, pkg_rating=star4)
            pk3 = package.objects.filter(pkg_dest_name=pkg, pkg_rating=star3)
            pk2 = package.objects.filter(pkg_dest_name=pkg, pkg_rating=star2)
            pk1 = package.objects.filter(pkg_dest_name=pkg, pkg_rating=star1)
            pk=pk5 | pk4 | pk3 | pk2 | pk1 # appending query
            n = len(pk)
            if n>0:
                nSlides = n // 4 + ceil((n / 4) - (n // 4))
                allpkg.append([pk, range(1, nSlides), nSlides])

        latests = package.objects.order_by('-pkg_created_date')[0:4]
        params = {'no_of_slides': nSlides, 'range': range(1, nSlides), 'destination': destinations, 'allpkg': allpkg,
                  'x': range(1, 6), 'latests': latests}
        return render(request, 'packageShow.html', params)

    destinations = destination.objects.all()
    n = len(destinations)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))
    allpkg = []
    destpkgs = package.objects.values('pkg_dest_name', 'id')  # getting all destination name against id
    pkgs = {item['pkg_dest_name'] for item in destpkgs}  # getting all destination name without id
    for pkg in pkgs:
        pk = package.objects.filter(pkg_dest_name=pkg)  # in pk we ar soring the packages against destination
        n = len(pk)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allpkg.append([pk, range(1, nSlides), nSlides])

    latests = package.objects.order_by('-pkg_created_date')[0:4]
    params = {'no_of_slides': nSlides, 'range': range(1, nSlides), 'destination': destinations, 'allpkg': allpkg,
              'x': range(1, 6),'latests': latests}
    return render(request,'packageShow.html',params)

def aviation(request):
    return render(request, 'aviation.html')

def visa_country(request):
    return render(request, 'visa_country.html')

def visa_requirements(request,rid):
    if rid==1:
        return render(request, 'visa_requirements_thiland.html')
    elif rid==2:
        return render(request, 'visa_requirements_malaysia.html')
    elif rid==3:
        return render(request, 'visa_requirements_vietnam.html')
    elif rid==4:
        return render(request, 'visa_requirements_singapore.html')
    elif rid==5:
        return render(request, 'visa_requirements_china.html')
    elif rid==6:
        return render(request, 'visa_requirements_egypt.html')
    elif rid==7:
        return render(request, 'visa_requirements_mayanmar.html')
    elif rid==8:
        return render(request, 'visa_requirements_srilanka.html')

def sentMail(request):
    if request.POST:
        cName = request.POST['cName']
        cEmail = request.POST['cEmail']
        checkin_date = request.POST['checkin_date']
        checkout_date = request.POST['checkout_date']
        guestNo = request.POST['guestNo']
        childNo = request.POST['childNo']
        pk = request.POST['pk']

        send_mail(
            'Customer Package Inquiry',
            'Customer Name: '+cName+'\n'+'Email: '+cEmail+'\n'+'Checkin Date: '+
              checkin_date+'\n'+'Checkout Date: '+checkout_date+'\n'+'Guest No: '+guestNo+'\n'+'Child No: '+childNo,
            'info@sair-bd.com',
            ['info@sair-bd.com'],
            fail_silently=False,
        )
        messages.info(request, 'Form Submitted')

    return redirect(views.packages,pk)

def sentMailCustom(request):
    if request.POST:
        cName = request.POST['cName']
        cEmail = request.POST['cEmail']
        subject = request.POST['subject']
        cMessage = request.POST['cMessage']

        send_mail(
            'Customer Inquiry',
            'Customer Name: '+cName+'\n'+'Email: '+cEmail+'\n'+'Subject: '+
              subject+'\n'+'Message: '+cMessage,
            'info@sair-bd.com',
            ['info@sair-bd.com'],
            fail_silently=False,
        )
        messages.info(request, 'Form Submitted')

    return redirect(views.contact)


def modarator_list(request):
    if request.session.has_key('is_logged'):
        admins = wadmin.objects.all()
        params = {'admin': admins}

        if request.POST:
            pemail = request.POST['email']
            checkMail = wadmin.objects.filter(email=pemail)

            if checkMail:
                messages.info(request, 'Email already exists')
            else:
                username = request.POST['username']
                password = request.POST['password']
                obj = wadmin(username=username, email=pemail, password=password)
                obj.save()
        return render(request, 'modarator_list.html', params)
    return redirect('admin_signin')

def edit_mlist_info(request,lid):
    wlists = wadmin.objects.filter(user_id=lid)
    params = {'wlist': wlists}
    return render(request,'update_modarator.html',params)


def update_mlist_info(request,lid):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        type = request.POST.get('type')
        print(type)

        wadmins = wadmin.objects.get(user_id=lid)
        wadmins.username = username
        wadmins.password = password
        wadmins.email = email
        wadmins.type = type
        wadmins.save()
    return redirect('modarator_list')

def delete_mlist_info(request,lid):
    mlist = wadmin.objects.filter(user_id=lid)
    mlist.delete()
    return redirect('modarator_list')

def destinations(request):
    destinations = destination.objects.all()
    params={'destination':destinations}
    return render(request, 'destinations.html',params)
