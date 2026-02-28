from datetime import datetime, date, timedelta
from django.shortcuts import render, redirect
from Admin.models import *
from Guest.models import *
from User.models import *
from Reporter.models import *
from Editor.models import *
from django.db.models import Q
from django.http import HttpResponse

def Homepage(request):
    if "uid" in request.session:
        return render(request, 'User/Homepage.html')
    else:
        return redirect("Guest:Login")

def MyProfile(request):
    if "uid" in request.session:
        userdata = tbl_user.objects.get(id=request.session["uid"])
        return render(request, 'User/MyProfile.html', {"userdata": userdata})
    else:
        return redirect("Guest:Login")

def EditProfile(request):
    if "uid" in request.session:
        userdata = tbl_user.objects.get(id=request.session["uid"])
        if request.method == 'POST':
            userdata.user_name = request.POST.get("txt_name")
            userdata.user_email = request.POST.get("txt_email")
            userdata.user_contact = request.POST.get("txt_contact")
            userdata.user_address = request.POST.get("txt_address")
            userdata.save()
            return render(request, 'User/EditProfile.html', {'msg': 'Updated'})
        else:
            return render(request, 'User/EditProfile.html', {'userdata': userdata})
    else:
        return redirect("Guest:Login")

def ChangePassword(request):
    if "uid" in request.session:
        userdata = tbl_user.objects.get(id=request.session["uid"])
        if request.method == 'POST':
            if userdata.user_password == request.POST.get("txt_old"):
                if request.POST.get("txt_new") == request.POST.get("txt_confirm"):
                    userdata.user_password = request.POST.get("txt_new")
                    userdata.save()
                    return render(request, 'User/ChangePassword.html', {'msg': 'Password Updated'})
                else:
                    return render(request, 'User/ChangePassword.html', {'msg1': 'Password Mismatch'})
            else:
                return render(request, 'User/ChangePassword.html', {'msg1': 'Incorrect Password'})
        else:
            return render(request, 'User/ChangePassword.html')
    else:
        return redirect("Guest:Login")

def UploadNews(request):
    if "uid" in request.session:
        category = tbl_category.objects.all()
        subcategory = tbl_subcategory.objects.all()
        user = tbl_user.objects.get(id=request.session["uid"])
        Newsdata = tbl_news.objects.filter(user=user)
        if request.method == 'POST':
            sub = tbl_subcategory.objects.get(id=request.POST.get("sel_subcategory"))
            tbl_news.objects.create(
                news_title=request.POST.get("txt_title"),
                news_content=request.POST.get("txt_content"),
                news_image=request.FILES.get("file_image"),
                subcategory=sub,
                user=user,
                news_status=0
            )
            return redirect("User:UploadNews")
        return render(request, 'User/UploadNews.html', {
            'category': category,
            'subcategory': subcategory,
            'Newsdata': Newsdata
        })
    else:
        return redirect("Guest:Login")

def delnews(request, id):
    if "uid" in request.session:
        news = tbl_news.objects.get(id=id, user_id=request.session["uid"])
        news.delete()
    return redirect("User:UploadNews")

def EditNews(request, fid):
    if "uid" in request.session:
        category = tbl_category.objects.all()
        NewsData = tbl_news.objects.get(id=fid)
        if request.method == 'POST':
            NewsData.news_title = request.POST.get("txt_title")
            NewsData.news_content = request.POST.get("txt_content")
            if request.FILES.get("file_image"):
                NewsData.news_image = request.FILES.get("file_image")
            NewsData.subcategory = tbl_subcategory.objects.get(id=request.POST.get("sel_subcategory"))
            NewsData.save()
            return redirect("User:UploadNews")
        return render(request, 'User/EditNews.html', {'category': category, 'NewsData': NewsData})
    else:
        return redirect("Guest:Login")

def AcceptAmount(request, id):
    if "uid" in request.session:
        news = tbl_news.objects.get(id=id, user_id=request.session["uid"])
        news.news_status = 4
        news.save()
    return redirect("User:MyNews")

def RejectAmount(request, id):
    if "uid" in request.session:
        news = tbl_news.objects.get(id=id, user_id=request.session["uid"])
        news.news_status = 5
        news.save()
    return redirect("User:MyNews")

def ConfirmEdits(request, id):
    if "uid" in request.session:
        news = tbl_news.objects.get(id=id, user_id=request.session["uid"])
        news.news_status = 9
        news.save()
    return redirect("User:MyNews")

def MyNews(request):
    if "uid" in request.session:
        newsdata = tbl_news.objects.filter(user_id=request.session["uid"])
        return render(request, 'User/MyNews.html', {'newsdata': newsdata})
    else:
        return redirect("Guest:Login")

def AjaxSubcategory(request):
    category = tbl_category.objects.get(id=request.GET.get("cid"))
    subcategory = tbl_subcategory.objects.filter(category=category)
    return render(request, 'User/AjaxSubcategory.html', {'subcategory': subcategory})

def UploadF(request, fid):
    newsdata = tbl_news.objects.get(id=fid)
    fdata = tbl_uploadfiles.objects.filter(news=newsdata)
    if request.method == 'POST':
        tbl_uploadfiles.objects.create(
            upload_files=request.FILES.get("file_extra"),
            news=newsdata
        )
        return redirect("User:UploadF", fid)
    return render(request, 'User/UploadF.html', {'fdata': fdata, 'fid': fid})

def delfile(request, id, fid):
    tbl_uploadfiles.objects.get(id=id).delete()
    return redirect("User:UploadF", fid)

def ViewUpdatesF(request, fid):
    newsdata = tbl_news.objects.get(id=fid)
    updatedataf = tbl_newsupdatesr.objects.filter(news=newsdata)
    return render(request, 'User/ViewUpdatesF.html', {'news': newsdata, 'updates': updatedataf, 'fid': fid})

def Complaint(request):
    if "uid" in request.session:
        userdata = tbl_user.objects.get(id=request.session["uid"])
        complaintdata = tbl_complaint.objects.filter(user_id=userdata)
        if request.method == 'POST':
            tbl_complaint.objects.create(
                complaint_title=request.POST.get("txt_title"),
                complaint_content=request.POST.get("txt_content"),
                user_id=userdata
            )
            return redirect("User:Complaint")
        return render(request, 'User/Complaint.html', {'userdata': userdata, 'complaintdata': complaintdata})
    else:
        return redirect("Guest:Login")

def delcomplaint(request, id):
    tbl_complaint.objects.get(id=id).delete()
    return redirect("User:Complaint")

def Advertisement(request):
    if "uid" in request.session:
        userdata = tbl_user.objects.get(id=request.session["uid"])
        Advdata = tbl_advertisement.objects.filter(user_id=userdata)
        if request.method == 'POST':
            tbl_advertisement.objects.create(
                advertisement_title=request.POST.get("txt_title"),
                advertisement_content=request.POST.get("txt_content"),
                advertisement_file=request.FILES.get("txt_file"),
                user_id=userdata
            )
            return redirect("User:Advertisement")
        return render(request, 'User/Advertisement.html', {'Advdata': Advdata, 'userdata': userdata})
    else:
        return redirect("Guest:Login")

def delAdv(request, id):
    tbl_advertisement.objects.get(id=id).delete()
    return redirect("User:Advertisement")

def MyAdvertisement(request):
    if "uid" in request.session:
        AdvData = tbl_advertisement.objects.filter(user_id=request.session['uid'])
        return render(request, 'User/MyAdvertisement.html', {'AdvData': AdvData})
    else:
        return redirect("Guest:Login")

def Payment(request, pid):
    data = tbl_advertisement.objects.get(id=pid)
    amt = data.advertisement_amount
    if request.method == 'POST':
        data.advertisement_status = 4
        data.save()
        return redirect("User:loader")
    return render(request, 'User/Payment.html', {'total': amt})

def loader(request):
    return render(request, "User/Loader.html")

def paymentsuc(request):
    return render(request, "User/Payment_suc.html")

def Logout(request):
    if "uid" in request.session:
        del request.session["uid"]
    return redirect("Guest:Login")

def viewplan(request):
    plans = tbl_plan.objects.all()
    subscription= tbl_subscription.objects.get(user=request.session['uid'],subscription_status=1)
    today = date.today()
    remaining_days = (subscription.expiry_date - today).days
    if remaining_days < 0:
        remaining_days = 0
    return render(request,"User/ViewPlan.html",{'plans':plans,'subscription':subscription,'remaining_days': remaining_days})

def Subscribe(request, pid):
    if "uid" in request.session:
        plan = tbl_plan.objects.get(id=pid)
        amount = plan.plan_amount
        if request.method == "POST" :

            user = tbl_user.objects.get(id=request.session["uid"])
           
            today = date.today()
            expiry = today + timedelta(days=plan.plan_duration)
            tbl_subscription.objects.filter(user=user, subscription_status=1).update(subscription_status=2)
            tbl_subscription.objects.create(
                user=user,
                plan=plan,
                expiry_date=expiry
            )
            return redirect("User:viewplan")
        else:
            return render(request,"User/Payment.html",{'total':amount})
    else:
        return redirect("Guest:Login")

def chatpage_usertoadmin(request):
    if "uid" in request.session:
        admin = tbl_admin.objects.first()
        return render(request, "User/Admin_Chat.html", {"admin": admin})
    else:
        return redirect("Guest:Login")

def ajaxchat_usertoadmin(request):
    if "uid" in request.session:
        from_user = tbl_user.objects.get(id=request.session["uid"])
        admin = tbl_admin.objects.first()
        tbl_chat.objects.create(
            chat_content=request.POST.get("msg"),
            chat_time=datetime.now(),
            user_from=from_user,
            admin_to=admin,
            chat_file=request.FILES.get("file")
        )
        return render(request, "User/Admin_Chat.html")
    else:
        return redirect("Guest:Login")

def ajaxchatview_usertoadmin(request):
    if "uid" in request.session:
        user = tbl_user.objects.get(id=request.session["uid"])
        admin = tbl_admin.objects.first()
        chat_data = tbl_chat.objects.filter(
            (Q(user_from=user) & Q(admin_to=admin)) |
            (Q(admin_from=admin) & Q(user_to=user))
        ).order_by('chat_time')
        return render(request, "User/Admin_ChatView.html", {"data": chat_data})
    else:
        return redirect("Guest:Login")

def clearchat_usertoadmin(request):
    if "uid" in request.session:
        user = tbl_user.objects.get(id=request.session["uid"])
        admin = tbl_admin.objects.first()
        tbl_chat.objects.filter(
            (Q(user_from=user) & Q(admin_to=admin)) |
            (Q(admin_from=admin) & Q(user_to=user))
        ).delete()
        return render(request, "User/ClearChat.html", {"msg": "Chat Deleted Successfully...."})
    else:
        return redirect("Guest:Login")

def chatpage_usertoeditor(request, id):
    if "uid" in request.session:
        editor = tbl_editor.objects.get(id=id)
        return render(request, "User/Editor_Chat.html", {"editor": editor})
    else:
        return redirect("Guest:Login")

def ajaxchat_usertoeditor(request):
    if "uid" in request.session:
        from_user = tbl_user.objects.get(id=request.session["uid"])
        to_editor = tbl_editor.objects.get(id=request.POST.get("tid"))
        tbl_chat.objects.create(
            chat_content=request.POST.get("msg"),
            chat_time=datetime.now(),
            user_from=from_user,
            editor_to=to_editor,
            chat_file=request.FILES.get("file")
        )
        return render(request, "User/Editor_Chat.html")
    else:
        return redirect("Guest:Login")

def ajaxchatview_usertoeditor(request):
    if "uid" in request.session:
        tid = request.GET.get("tid")
        user = tbl_user.objects.get(id=request.session["uid"])
        editor = tbl_editor.objects.get(id=tid)
        chat_data = tbl_chat.objects.filter(
            (Q(user_from=user) & Q(editor_to=editor)) |
            (Q(editor_from=editor) & Q(user_to=user))
        ).order_by("chat_time")
        return render(request, "User/Editor_ChatView.html", {
            "data": chat_data,
            "tid": tid
        })
    else:
        return redirect("Guest:Login")

def clearchat_usertoeditor(request):
    if "uid" in request.session:
        tid = request.GET.get("tid")
        user = tbl_user.objects.get(id=request.session["uid"])
        editor = tbl_editor.objects.get(id=tid)
        tbl_chat.objects.filter(
            (Q(user_from=user) & Q(editor_to=editor)) |
            (Q(editor_from=editor) & Q(user_to=user))
        ).delete()
        return render(request, "User/ClearChat.html", {
            "msg": "Chat Deleted Successfully..."
        })
    else:
        return redirect("Guest:Login")