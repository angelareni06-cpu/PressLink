from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
# Create your views here.

def index(request):
    return render(request,'Guest/index.html')

def UserRegistration(request):
    district = tbl_district.objects.all()
    place = tbl_place.objects.all()
    freelancerdata = tbl_freelancertype.objects.all()

    if request.method == 'POST':

        name = request.POST.get("txt_name")
        email = request.POST.get("txt_email")
        contact = request.POST.get("txt_contact")
        address = request.POST.get("txt_address")
        password = request.POST.get("txt_password")

        photo = request.FILES.get("file_photo")
        place_id = request.POST.get("sel_place")

        # ===== REQUIRED FIELD VALIDATION =====
        if not all([name, email, contact, address, password, photo, place_id]):
            return render(request, 'Guest/UserRegistration.html', {
                'msg': 'Please fill all required fields',
                'district': district,
                'place': place,
                'freelancerdata': freelancerdata
            })

        # ===== OPTIONAL FIELDS =====
        gender = request.POST.get("txt_gender")
        dob = request.POST.get("txt_dob")
        proof = request.FILES.get("file_proof")
        work = request.FILES.get("file_work")
        level = request.POST.get("txt_level")
        bio = request.POST.get("txt_bio")
        social = request.POST.get("txt_social")

        skilltype = None
        skill_id = request.POST.get("sel_skill")
        if skill_id:
            skilltype = tbl_skilltype.objects.get(id=skill_id)

        place_obj = tbl_place.objects.get(id=place_id)

        # Email uniqueness check
        if tbl_user.objects.filter(user_email=email).exists():
            return render(request, 'Guest/UserRegistration.html', {
                'msg': 'Email already exists',
                'district': district,
                'place': place,
                'freelancerdata': freelancerdata
            })

        tbl_user.objects.create(
            user_name=name,
            user_email=email,
            user_contact=contact,
            user_address=address,
            user_password=password,
            user_photo=photo,
            place=place_obj,
            user_gender=gender,
            user_dob=dob,
            user_proof=proof,
            user_work=work,
            user_level=level,
            user_bio=bio,
            user_social=social,
            skill_type=skilltype,
            user_status=1  # default active
        )

        return render(request, 'Guest/UserRegistration.html', {
            'msg': 'Registration Successful',
            'district': district,
            'place': place,
            'freelancerdata': freelancerdata
        })

    else:
        return render(request, 'Guest/UserRegistration.html', {
            'district': district,
            'place': place,
            'freelancerdata': freelancerdata
        })
def AjaxPlace(request):
    district=tbl_district.objects.get(id=request.GET.get("did"))
    place=tbl_place.objects.filter(district=district)
    return render(request,'Guest/AjaxPlace.html',{'place':place})

def AjaxSkilltype(request):
    freelancerdata=tbl_freelancertype.objects.get(id=request.GET.get("fid"))
    skilldata=tbl_skilltype.objects.filter( freelancer_type=freelancerdata)
    return render(request,'Guest/AjaxSkilltype.html',{'skilltype':skilldata}) 

def Login(request):
    if request.method == 'POST':

        email = request.POST.get('txt_email')
        password = request.POST.get('txt_password')

        admincount = tbl_admin.objects.filter(admin_email=email, admin_password=password).count()
        usercount = tbl_user.objects.filter(user_email=email, user_password=password).count()
        reportercount = tbl_reporter.objects.filter(reporter_email=email, reporter_password=password).count()
        editorcount = tbl_editor.objects.filter(editor_email=email, editor_password=password).count()
        verifiercount = tbl_verifier.objects.filter(verifier_email=email, verifier_password=password).count()

        # ===== ADMIN =====
        if admincount > 0:
            admindata = tbl_admin.objects.get(admin_email=email, admin_password=password)
            request.session["aid"] = admindata.id
            return redirect("Admin:HomePage")

        # ===== USER =====
        elif usercount > 0:
            userdata = tbl_user.objects.get(user_email=email, user_password=password)

            if userdata.user_status == 0:
                return render(request, 'Guest/Login.html', {
                    'msg': 'Your account is blocked by Admin'
                })

            request.session["uid"] = userdata.id
            return redirect("User:Homepage")

        # ===== REPORTER =====
        elif reportercount > 0:
            reporterdata = tbl_reporter.objects.get(reporter_email=email, reporter_password=password)
            request.session["Rid"] = reporterdata.id
            return redirect("Reporter:Homepage")

        # ===== EDITOR =====
        elif editorcount > 0:
            editordata = tbl_editor.objects.get(editor_email=email, editor_password=password)
            request.session["Eid"] = editordata.id
            return redirect("Editor:Homepage")

        # ===== VERIFIER =====
        elif verifiercount > 0:
            verifierData = tbl_verifier.objects.get(verifier_email=email, verifier_password=password)
            request.session["Vid"] = verifierData.id
            return redirect("Verifier:Homepage")

        else:
            return render(request, 'Guest/Login.html', {
                'msg': 'Invalid Email or Password'
            })

    else:
        return render(request, 'Guest/Login.html')  
        
def Reporter(request):
    district = tbl_district.objects.all()
    place = tbl_place.objects.all()

    if request.method == 'POST':

        name = request.POST.get("txt_name")
        email = request.POST.get("txt_email")
        contact = request.POST.get("txt_contact")
        address = request.POST.get("txt_address")
        password = request.POST.get("txt_password")
        photo = request.FILES.get("file_photo")
        place_id = request.POST.get("sel_place")
        proof = request.FILES.get("file_proof")

        # ===== REQUIRED CHECK =====
        if not all([name, email, contact, address, password, photo, place_id]):
            return render(request, 'Guest/Reporter.html', {
                'msg': 'Please fill all required fields',
                'district': district,
                'place': place
            })

        # ===== OPTIONAL FIELDS =====
        gender = request.POST.get("txt_gender")
        dob = request.POST.get("txt_dob")
        

        # ===== EMAIL CHECK =====
        if tbl_reporter.objects.filter(reporter_email=email).count() > 0:
            return render(request, 'Guest/Reporter.html', {
                'msg': 'Email already exists',
                'district': district,
                'place': place
            })

        place_obj = tbl_place.objects.get(id=place_id)

        tbl_reporter.objects.create(
            reporter_name=name,
            reporter_email=email,
            reporter_contact=contact,
            reporter_address=address,
            reporter_password=password,
            reporter_photo=photo,
            place=place_obj,
            reporter_gender=gender,
            reporter_dob=dob,
            reporter_proof=proof,
        )

        return render(request, 'Guest/Reporter.html', {
            'msg': 'Registration Successful',
            'district': district,
            'place': place
        })

    else:
        return render(request, 'Guest/Reporter.html', {
            'district': district,
            'place': place
        }) 