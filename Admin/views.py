from django.shortcuts import render, redirect
from Admin.models import *
from Guest.models import *
from Reporter.models import *
from Editor.models import *
from User.models import *
from datetime import datetime
from django.db.models import Q
from django.http import HttpResponse

def HomePage(request):
    if "aid" in request.session:
        return render(request, 'Admin/HomePage.html')
    return redirect("Guest:Login")

def Logout(request):
    if "aid" in request.session:
        del request.session["aid"]
    return redirect("Guest:Login")

def AdminRegistration(request):
    if "aid" in request.session:
        data = tbl_admin.objects.all()
        if request.method == 'POST':
            name = request.POST.get("txt_name")
            email = request.POST.get("txt_email")
            password = request.POST.get("txt_password")
            if tbl_admin.objects.filter(admin_email=email).exists():
                return render(request, 'Admin/AdminRegistration.html', {'msg': "Email Already Exist"})
            tbl_admin.objects.create(
                admin_name=name,
                admin_email=email,
                admin_password=password
            )
            return redirect("Admin:AdminRegistration")
        return render(request, 'Admin/AdminRegistration.html', {'AdminRegistration': data})
    return redirect("Guest:Login")

def editadmin(request, id):
    editdata = tbl_admin.objects.get(id=id)
    data = tbl_admin.objects.all()
    if request.method == 'POST':
        editdata.admin_name = request.POST.get("txt_name")
        editdata.admin_email = request.POST.get("txt_email")
        editdata.admin_password = request.POST.get("txt_password")
        editdata.save()
        return redirect('Admin:AdminRegistration')
    return render(request, 'Admin/AdminRegistration.html', {'editdata': editdata, 'AdminRegistration': data})

def deladmin(request, id):
    tbl_admin.objects.get(id=id).delete()
    return redirect("Admin:AdminRegistration")

def EditorRegistration(request):
    if "aid" in request.session:
        district = tbl_district.objects.all()
        place = tbl_place.objects.all()
        editorData = tbl_editor.objects.all()
        if request.method == 'POST':
            name = request.POST.get("txt_name")
            email = request.POST.get("txt_email")
            contact = request.POST.get("txt_contact")
            photo = request.FILES.get("file_photo")
            proof = request.FILES.get("file_proof")
            password = request.POST.get("txt_password")
            place_id = tbl_place.objects.get(id=request.POST.get("sel_place"))
            tbl_editor.objects.create(
                editor_name=name,
                editor_email=email,
                editor_contact=contact,
                editor_photo=photo,
                editor_proof=proof,
                editor_password=password,
                place=place_id,
                editor_status=1
            )
            return redirect("Admin:editorregistration")
        return render(request, 'Admin/EditorRegistration.html', {
            'district': district,
            'place': place,
            'editorData': editorData
        })
    return redirect("Guest:Login")

def BlockEditor(request, eid):
    if "aid" in request.session:
        editor = tbl_editor.objects.get(id=eid)
        editor.editor_status = 0
        editor.save()
        return redirect("Admin:editorregistration")
    return redirect("Guest:Login")

def UnblockEditor(request, eid):
    if "aid" in request.session:
        editor = tbl_editor.objects.get(id=eid)
        editor.editor_status = 1
        editor.save()
        return redirect("Admin:editorregistration")
    return redirect("Guest:Login")

def deleditor(request, id):
    if "aid" in request.session:
        tbl_editor.objects.get(id=id).delete()
        return redirect("Admin:editorregistration")
    return redirect("Guest:Login")

def VerifierRegistration(request):
    if "aid" in request.session:
        district = tbl_district.objects.all()
        place = tbl_place.objects.all()
        verifierData = tbl_verifier.objects.all()
        if request.method == 'POST':
            name = request.POST.get("txt_name")
            email = request.POST.get("txt_email")
            contact = request.POST.get("txt_contact")
            photo = request.FILES.get("file_photo")
            proof = request.FILES.get("file_proof")
            password = request.POST.get("txt_password")
            place_id = tbl_place.objects.get(id=request.POST.get("sel_place"))
            tbl_verifier.objects.create(
                verifier_name=name,
                verifier_email=email,
                verifier_contact=contact,
                verifier_photo=photo,
                verifier_proof=proof,
                verifier_password=password,
                place=place_id,
                verifier_status=1
            )
            return redirect("Admin:verifierregistration")
        return render(request, 'Admin/VerifierRegistration.html', {
            'district': district,
            'place': place,
            'verifierData': verifierData
        })
    return redirect("Guest:Login")

def BlockVerifier(request, vid):
    if "aid" in request.session:
        verifier = tbl_verifier.objects.get(id=vid)
        verifier.verifier_status = 0
        verifier.save()
        return redirect("Admin:verifierregistration")
    return redirect("Guest:Login")

def UnblockVerifier(request, vid):
    if "aid" in request.session:
        verifier = tbl_verifier.objects.get(id=vid)
        verifier.verifier_status = 1
        verifier.save()
        return redirect("Admin:verifierregistration")
    return redirect("Guest:Login")

def delverifier(request, id):
    if "aid" in request.session:
        tbl_verifier.objects.get(id=id).delete()
        return redirect("Admin:verifierregistration")
    return redirect("Guest:Login")

def Reporterverification(request):
    if "aid" in request.session:
        pending = tbl_reporter.objects.filter(reporter_status=0)
        accept = tbl_reporter.objects.filter(reporter_status=1)
        reject = tbl_reporter.objects.filter(reporter_status=2)
        return render(request, 'Admin/ReporterVerification.html', {
            'pending': pending,
            'accept': accept,
            'reject': reject
        })
    return redirect("Guest:Login")

def ReporterAccept(request, aid):
    if "aid" in request.session:
        acceptdata = tbl_reporter.objects.get(id=aid)
        acceptdata.reporter_status = 1
        acceptdata.save()
        return redirect('Admin:reporterverification')
    return redirect("Guest:Login")

def ReporterReject(request, rid):
    if "aid" in request.session:
        rejectdata = tbl_reporter.objects.get(id=rid)
        rejectdata.reporter_status = 2
        rejectdata.save()
        return redirect('Admin:reporterverification')
    return redirect("Guest:Login")

def Userverification(request):
    if "aid" in request.session:
        users = tbl_user.objects.all()
        return render(request, 'Admin/UserVerification.html', {'users': users})
    return redirect("Guest:Login")

def BlockUser(request, uid):
    if "aid" in request.session:
        user = tbl_user.objects.get(id=uid)
        user.user_status = 0
        user.save()
        return redirect("Admin:userverification")
    return redirect("Guest:Login")

def UnblockUser(request, uid):
    if "aid" in request.session:
        user = tbl_user.objects.get(id=uid)
        user.user_status = 1
        user.save()
        return redirect("Admin:userverification")
    return redirect("Guest:Login")

def District(request):
    if "aid" in request.session:
        data = tbl_district.objects.all()
        if request.method == 'POST':
            district = request.POST.get("txt_district")
            if tbl_district.objects.filter(district_name=district).exists():
                return render(request, 'Admin/District.html', {'msg': "District Already Exist"})
            tbl_district.objects.create(district_name=district)
            return redirect("Admin:District")
        return render(request, 'Admin/District.html', {'district': data})
    return redirect("Guest:Login")

def editdistrict(request, id):
    editdata = tbl_district.objects.get(id=id)
    data = tbl_district.objects.all()
    if request.method == 'POST':
        editdata.district_name = request.POST.get("txt_district")
        editdata.save()
        return redirect('Admin:District')
    return render(request, 'Admin/District.html', {'editdata': editdata, 'district': data})

def deldistrict(request, id):
    tbl_district.objects.get(id=id).delete()
    return redirect("Admin:District")

def Place(request):
    if "aid" in request.session:
        data = tbl_district.objects.all()
        placedata = tbl_place.objects.all()
        if request.method == 'POST':
            place = request.POST.get("txt_place")
            district = tbl_district.objects.get(id=request.POST.get("sel_district"))
            tbl_place.objects.create(place_name=place, district=district)
            return redirect("Admin:Place")
        return render(request, 'Admin/Place.html', {'district': data, 'place': placedata})
    return redirect("Guest:Login")

def editplace(request, id):
    district = tbl_district.objects.all()
    editdata = tbl_place.objects.get(id=id)
    if request.method == 'POST':
        editdata.place_name = request.POST.get("txt_place")
        editdata.district = tbl_district.objects.get(id=request.POST.get("sel_district"))
        editdata.save()
        return redirect("Admin:Place")
    return render(request, 'Admin/Place.html', {'editdata': editdata, 'district': district})

def delplace(request, id):
    tbl_place.objects.get(id=id).delete()
    return redirect("Admin:Place")

def Category(request):
    if "aid" in request.session:
        data = tbl_category.objects.all()
        if request.method == 'POST':
            category = request.POST.get("txt_category")
            tbl_category.objects.create(category_name=category)
            return redirect("Admin:Category")
        return render(request, 'Admin/Category.html', {'category': data})
    return redirect("Guest:Login")

def editcategory(request, id):
    editdata = tbl_category.objects.get(id=id)
    data = tbl_category.objects.all()
    if request.method == 'POST':
        editdata.category_name = request.POST.get("txt_category")
        editdata.save()
        return redirect('Admin:Category')
    return render(request, 'Admin/Category.html', {'editdata': editdata, 'category': data})

def delcategory(request, id):
    tbl_category.objects.get(id=id).delete()
    return redirect("Admin:Category")

def Subcategory(request):
    if "aid" in request.session:
        catdata = tbl_category.objects.all()
        subdata = tbl_subcategory.objects.all()
        if request.method == 'POST':
            subcategory = request.POST.get("txt_subcategory")
            category = tbl_category.objects.get(id=request.POST.get("sel_category"))
            tbl_subcategory.objects.create(subcategory_name=subcategory, category=category)
            return redirect("Admin:Subcategory")
        return render(request, 'Admin/Subcategory.html', {'category': catdata, 'subcategory': subdata})
    return redirect("Guest:Login")

def editsub(request, id):
    category = tbl_category.objects.all()
    editdata = tbl_subcategory.objects.get(id=id)
    if request.method == 'POST':
        editdata.subcategory_name = request.POST.get("txt_subcategory")
        editdata.category = tbl_category.objects.get(id=request.POST.get("sel_category"))
        editdata.save()
        return redirect("Admin:Subcategory")
    return render(request, 'Admin/Subcategory.html', {'editdata': editdata, 'category': category})

def delsub(request, id):
    tbl_subcategory.objects.get(id=id).delete()
    return redirect("Admin:Subcategory")

def FreelancerType(request):
    if "aid" in request.session:
        freelancerdata = tbl_freelancertype.objects.all()
        if request.method == 'POST':
            freelancertype = request.POST.get("txt_type")
            tbl_freelancertype.objects.create(freelancer_type=freelancertype)
            return redirect("Admin:freelancertype")
        return render(request, 'Admin/FreelancerType.html', {'freelancer': freelancerdata})
    return redirect("Guest:Login")

def editfreelancer(request, id):
    editdata = tbl_freelancertype.objects.get(id=id)
    freelancerdata = tbl_freelancertype.objects.all()
    if request.method == 'POST':
        editdata.freelancer_type = request.POST.get("txt_type")
        editdata.save()
        return redirect('Admin:freelancertype')
    return render(request, 'Admin/FreelancerType.html', {'editdata': editdata, 'freelancer': freelancerdata})    

def delfreelancer(request, id):
    if "aid" in request.session:
        tbl_freelancertype.objects.get(id=id).delete()
        return redirect("Admin:freelancertype")
    return redirect("Guest:Login")

def SkillType(request):
    if "aid" in request.session:
        freelancerdata = tbl_freelancertype.objects.all()
        skilldata = tbl_skilltype.objects.all()
        if request.method == 'POST':
            skilltype = request.POST.get("txt_skill")
            freelancer = tbl_freelancertype.objects.get(id=request.POST.get("sel_freelancertype"))
            tbl_skilltype.objects.create(skill_type=skilltype, freelancer_type=freelancer)
            return redirect("Admin:SkillType")
        return render(request, 'Admin/Skill.html', {'freelancer': freelancerdata, 'skilltype': skilldata})
    return redirect("Guest:Login")

def editskill(request, id):
    freelancerdata = tbl_freelancertype.objects.all()
    skilldata = tbl_skilltype.objects.get(id=id)
    if request.method == 'POST':
        skilldata.skill_type = request.POST.get("txt_skill")
        skilldata.freelancerdata = tbl_freelancertype.objects.get(id=request.POST.get("sel_freelancertype"))
        skilldata.save()
        return redirect("Admin:SkillType")
    return render(request, 'Admin/Skill.html', {'skilldata': skilldata, 'freelancer': freelancerdata})

def delskill(request, id):
    if "aid" in request.session:
        tbl_skilltype.objects.get(id=id).delete()
        return redirect("Admin:SkillType")
    return redirect("Guest:Login")

def PublishedNews(request):
    if "aid" in request.session:
        msg = request.session.pop('msg', None)
        NewsData = tbl_news.objects.filter(news_status__in=[1, 7, 8, 9, 10], reporter__isnull=False)
        return render(request, 'Admin/PublishedNews.html', {"NewsData": NewsData, "msg": msg})
    return redirect("Guest:Login")

def FPublishedNews(request):
    if "aid" in request.session:
        msg = request.session.pop('msg', None)
        NewsData = tbl_news.objects.filter(news_status__in=[1, 3, 4, 5, 6, 7, 8, 9, 10], user__isnull=False)
        return render(request, 'Admin/FPublishedNews.html', {"Newsdata": NewsData, "msg": msg})
    return redirect("Guest:Login")

def ViewFiles(request, fid):
    if "aid" in request.session:
        news = tbl_news.objects.filter(id=fid).first()
        if news:
            UploadF = tbl_uploadfiles.objects.filter(news=news, upload_status=1)
            return render(request, 'Admin/ViewFiles.html', {'UploadF': UploadF, 'news': news})
        return redirect("Admin:FPublishedNews")
    return redirect("Guest:Login")

def AdminPayUser(request, id):
    news = tbl_news.objects.get(id=id)
    if request.method == "POST":
        news.news_status = 6  
        news.save()
        return redirect("Admin:FPublishedNews")
    else:
        return render(request,"Admin/Payment2.html",{'total':news.news_amount})

def PublishNews(request, id):
    if "aid" in request.session:
        news = tbl_news.objects.get(id=id)
        if news.news_status == 9:
            news.news_status = 10  # 10 means Published
            news.save()
        else:
            # only allow admin publish after editor+user/reporter confirmation
            # keep status unchanged and optionally add warning via session
            request.session['msg'] = 'News must be in status 9 to publish.'
        if news.user:
            return redirect("Admin:FPublishedNews")
        else:
            return redirect("Admin:PublishedNews")
    return redirect("Guest:Login")

def AddPayment(request, id):
    if "aid" in request.session:
        news = tbl_news.objects.get(id=id)
        if request.method == "POST":
            news.news_amount = request.POST.get("txt_amount")
            news.news_status = 3
            news.save()
            return redirect("Admin:FPublishedNews")
        return render(request, "Admin/Payment.html", {"news": news})
    return redirect("Guest:Login")

def ViewComplaints(request):
    if "aid" in request.session:
        user_complaints = tbl_complaint.objects.filter(user_id__isnull=False)
        reporter_complaints = tbl_complaint.objects.filter(reporter_id__isnull=False)
        verifier_complaints = tbl_complaint.objects.filter(verifier_id__isnull=False)
        editor_complaints = tbl_complaint.objects.filter(editor_id__isnull=False)
        return render(request, 'Admin/ViewComplaints.html', {
            'user_complaints': user_complaints,
            'reporter_complaints': reporter_complaints,
            'verifier_complaints': verifier_complaints,
            'editor_complaints': editor_complaints
        })
    return redirect("Guest:Login")

def Reply(request, id):
    if "aid" in request.session:
        complaintdata = tbl_complaint.objects.filter(id=id).first()
        if not complaintdata:
            return redirect("Admin:viewComplaints")
        if request.method == 'POST':
            reply = request.POST.get("txt_reply")
            complaintdata.complaint_reply = reply
            complaintdata.complaint_status = 1
            complaintdata.save()
            return redirect("Admin:viewComplaints")
        return render(request, 'Admin/Reply.html', {'complaintdata': complaintdata})
    return redirect("Guest:Login")

def Plan(request):
    if "aid" in request.session:
        plandata = tbl_plan.objects.all()
        if request.method == 'POST':
            name = request.POST.get("txt_name")
            duration = request.POST.get("txt_duration")
            amount = request.POST.get("txt_amount")
            if tbl_plan.objects.filter(plan_name=name).exists():
                return render(request, 'Admin/Plan.html', {
                    'plandata': plandata,
                    'msg': 'Plan already exists'
                })
            tbl_plan.objects.create(
                plan_name=name,
                plan_duration=duration,
                plan_amount=amount
            )
            return redirect("Admin:Plan")
        return render(request, 'Admin/Plan.html', {'plandata': plandata})
    return redirect("Guest:Login")

def delplan(request, id):
    if "aid" in request.session:
        plan = tbl_plan.objects.filter(id=id).first()
        if plan:
            plan.delete()
        return redirect("Admin:Plan")
    return redirect("Guest:Login")

def Advertisement(request):
    if "aid" in request.session:
        Advertisement = tbl_advertisement.objects.filter(advertisement_status__in=[2, 3, 4, 5, 6])
        return render(request, 'Admin/Advertisement.html', {"Advertisement": Advertisement})
    return redirect("Guest:Login")

def PublishAdvertisement(request, id):
    if "aid" in request.session:
        ad = tbl_advertisement.objects.get(id=id)
        ad.advertisement_status = 6
        ad.save()
        return redirect("Admin:Advertisement")
    return redirect("Guest:Login")

def PaymentAdvertisement(request, id):
    if "aid" in request.session:
        advertise = tbl_advertisement.objects.filter(id=id).first()
        if not advertise:
            return redirect("Admin:Advertisement")
        if request.method == 'POST':
            amount = request.POST.get("txt_amount")
            advertise.advertisement_amount = amount
            advertise.advertisement_status = 3
            advertise.save()
            return redirect("Admin:Advertisement")
        return render(request, 'Admin/PaymentAdvertisement.html', {'advertise': advertise})
    return redirect("Guest:Login")



def AddSalary(request, id, type):
    if "aid" in request.session:
        data = None
        if type == "editor":
            data = tbl_editor.objects.get(id=id)
        elif type == "verifier":
            data = tbl_verifier.objects.get(id=id)
        elif type == "reporter":
            data = tbl_reporter.objects.get(id=id)
        
        if request.method == "POST":
            amt = request.POST.get("txt_amount")
            if type == "editor":
                tbl_salary.objects.create(editor=data, salary_amount=amt)
            elif type == "verifier":
                tbl_salary.objects.create(verifier=data, salary_amount=amt)
            elif type == "reporter":
                tbl_salary.objects.create(reporter=data, salary_amount=amt)
            
            if type == "editor":
                return redirect("Admin:editorregistration")
            elif type == "verifier":
                return redirect("Admin:verifierregistration")
            elif type == "reporter":
                return redirect("Admin:reporterverification")

        return render(request, "Admin/AddSalary.html", {"data": data, "type": type})
    return redirect("Guest:Login")


def chatpage(request, id):
    if "aid" in request.session:
        user = tbl_user.objects.get(id=id)
        return render(request, "Admin/Chat.html", {"user": user})
    else:
        return render(request, "Guest/Login.html")

def ajaxchat(request):
    if "aid" in request.session:

        from_admin = tbl_admin.objects.get(id=request.session["aid"])
        to_user = tbl_user.objects.get(id=request.POST.get("tid"))

        tbl_chat.objects.create(
            chat_content=request.POST.get("msg"),
            chat_time=datetime.now(),
            admin_from=from_admin,
            user_to=to_user,
            chat_file=request.FILES.get("file")
        )

        return render(request, "Admin/Chat.html")

    else:
        return render(request, "Guest/Login.html")

def ajaxchatview(request):
    if "aid" in request.session:

        tid = request.GET.get("tid")

        admin = tbl_admin.objects.get(id=request.session["aid"])
        user = tbl_user.objects.get(id=tid)

        chat_data = tbl_chat.objects.filter(
            (
                Q(admin_from=admin) & Q(user_to=user)
            ) |
            (
                Q(user_from=user) & Q(admin_to=admin)
            )
        ).order_by("chat_time")

        return render(request, "Admin/ChatView.html", {
            "data": chat_data,
            "tid": tid
        })

    else:
        return render(request, "Guest/Login.html")

def clearchat(request):
    if "aid" in request.session:

        tid = request.GET.get("tid")

        admin = tbl_admin.objects.get(id=request.session["aid"])
        user = tbl_user.objects.get(id=tid)

        tbl_chat.objects.filter(
            (
                Q(admin_from=admin) & Q(user_to=user)
            ) |
            (
                Q(user_from=user) & Q(admin_to=admin)
            )
        ).delete()

        return render(request, "Admin/ClearChat.html", {
            "msg": "Chat Deleted Successfully..."
        })

    else:
        return render(request, "Guest/Login.html")




def Loader(request):
    return render(request,"Admin/Loader.html")

def Payment_suc(request):
    return render(request,"Admin/Payment_suc.html")
