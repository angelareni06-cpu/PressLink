from datetime import datetime
from django.shortcuts import render, redirect
from django.db.models import Q
from Admin.models import *
from Guest.models import *
from Reporter.models import *
from Editor.models import *
from User.models import *

def Homepage(request):
    if "Rid" in request.session:
        rep = tbl_reporter.objects.get(id=request.session['Rid'])
        return render(request, 'Reporter/HomePage.html', {"rep": rep})
    return redirect("Guest:Login")

def MyProfile(request):
    if "Rid" in request.session:
        reporterdata = tbl_reporter.objects.get(id=request.session["Rid"])
        return render(request, 'Reporter/MyProfileR.html', {"reporterdata": reporterdata})
    return redirect("Guest:Login")

def EditProfile(request):
    if "Rid" in request.session:
        reporterdata = tbl_reporter.objects.get(id=request.session["Rid"])
        if request.method == 'POST':
            reporterdata.reporter_name = request.POST.get("txt_name")
            reporterdata.reporter_email = request.POST.get("txt_email")
            reporterdata.reporter_contact = request.POST.get("txt_contact")
            reporterdata.reporter_address = request.POST.get("txt_address")
            reporterdata.save()
            return render(request, 'Reporter/EditProfile.html', {'msg': 'Updated Successfully'})
        return render(request, 'Reporter/EditProfile.html', {'reporterdata': reporterdata})
    return redirect("Guest:Login")

def ChangePassword(request):
    if "Rid" in request.session:
        reporterdata = tbl_reporter.objects.get(id=request.session["Rid"])
        if request.method == 'POST':
            old = request.POST.get("txt_old")
            new = request.POST.get("txt_new")
            confirm = request.POST.get("txt_confirm")
            if reporterdata.reporter_password == old:
                if new == confirm:
                    reporterdata.reporter_password = new
                    reporterdata.save()
                    return render(request, 'Reporter/ChangePassword.html', {'msg': 'Password Updated'})
                return render(request, 'Reporter/ChangePassword.html', {'msg1': 'Password Mismatch'})
            return render(request, 'Reporter/ChangePassword.html', {'msg1': 'Incorrect Old Password'})
        return render(request, 'Reporter/ChangePassword.html')
    return redirect("Guest:Login")

def AddNews(request):
    if "Rid" in request.session:
        category = tbl_category.objects.all()
        subcategory = tbl_subcategory.objects.all()
        reporterdata = tbl_reporter.objects.get(id=request.session["Rid"])
        NewsData = tbl_news.objects.filter(reporter=reporterdata)
        if request.method == 'POST':
            tbl_news.objects.create(
                news_title=request.POST.get("txt_title"),
                news_content=request.POST.get("txt_content"),
                news_image=request.FILES.get("file_image"),
                subcategory=tbl_subcategory.objects.get(id=request.POST.get("sel_subcategory")),
                reporter=reporterdata,
                breaking=int(request.POST.get("breaking", 0))
            )
            return render(request, 'Reporter/AddNews.html', {'msg': 'News Added Successfully'})
        return render(request, 'Reporter/AddNews.html', {
            'category': category,
            'subcategory': subcategory,
            'NewsData': NewsData
        })
    return redirect("Guest:Login")

def delnews(request, id):
    if "Rid" in request.session:
        tbl_news.objects.get(id=id).delete()
        return redirect("Reporter:AddNews")
    return redirect("Guest:Login")

def UploadFiles(request, nid):
    if "Rid" in request.session:
        newsdata = tbl_news.objects.get(id=nid)
        uploaddata = tbl_uploadfiles.objects.filter(news=newsdata)
        if request.method == 'POST':
            tbl_uploadfiles.objects.create(
                upload_files=request.FILES.get("file_upload"),
                news=newsdata
            )
            return render(request, 'Reporter/Upload.html', {'msg': 'Uploaded', 'nid': nid})
        return render(request, 'Reporter/Upload.html', {'uploaddata': uploaddata, 'nid': nid})
    return redirect("Guest:Login")

def delfile(request, id, nid):
    if "Rid" in request.session:
        tbl_uploadfiles.objects.get(id=id).delete()
        return redirect("Reporter:UploadFiles", nid)
    return redirect("Guest:Login")

def Complaint(request):
    if "Rid" in request.session:
        reporterdata = tbl_reporter.objects.get(id=request.session["Rid"])
        complaintdata = tbl_complaint.objects.filter(reporter_id=reporterdata)
        if request.method == 'POST':
            tbl_complaint.objects.create(
                complaint_title=request.POST.get("txt_title"),
                complaint_content=request.POST.get("txt_content"),
                reporter_id=reporterdata
            )
            return render(request, 'Reporter/Complaint.html', {'msg': 'Complaint Added'})
        return render(request, 'Reporter/Complaint.html', {
            'reporterdata': reporterdata,
            'complaintdata': complaintdata
        })
    return redirect("Guest:Login")

def delcomplaint(request, id):
    if "Rid" in request.session:
        tbl_complaint.objects.get(id=id).delete()
        return redirect("Reporter:Complaint")
    return redirect("Guest:Login")

def MyNews(request):
    if "Rid" in request.session:
        newsdata = tbl_news.objects.filter(reporter=request.session['Rid'])
        return render(request, 'Reporter/MyNews.html', {'newsdata': newsdata})
    return redirect("Guest:Login")

def ConfirmEdits(request, id):
    if "Rid" in request.session:
        news = tbl_news.objects.get(id=id, reporter_id=request.session['Rid'])
        news.news_status = 9
        news.save()
    return redirect("Reporter:MyNews")

def ViewUpdatesR(request, nid):
    if "Rid" in request.session:
        news = tbl_news.objects.get(id=nid)
        updates = tbl_newsupdatesr.objects.filter(news=news)
        return render(request, 'Reporter/ViewUpdatesR.html', {'news': news, 'updates': updates})
    return redirect("Guest:Login")

def chatpage(request, id):
    if "Rid" in request.session:
        editor = tbl_editor.objects.get(id=id)
        return render(request, "Reporter/Chat.html", {"editor": editor})
    return redirect("Guest:Login")

def ajaxchat(request):
    if "Rid" in request.session:
        from_reporter = tbl_reporter.objects.get(id=request.session["Rid"])
        to_editor = tbl_editor.objects.get(id=request.POST.get("tid"))
        tbl_chat.objects.create(
            chat_content=request.POST.get("msg"),
            chat_time=datetime.now(),
            reporter_from=from_reporter,
            editor_to=to_editor,
            chat_file=request.FILES.get("file")
        )
        return render(request, "Reporter/Chat.html")
    return redirect("Guest:Login")

def ajaxchatview(request):
    if "Rid" in request.session:
        tid = request.GET.get("tid")
        reporter = tbl_reporter.objects.get(id=request.session["Rid"])
        chat_data = tbl_chat.objects.filter(
            (Q(reporter_from=reporter) & Q(editor_to=tid)) |
            (Q(editor_from=tid) & Q(reporter_to=reporter))
        ).order_by('chat_time')
        return render(request, "Reporter/ChatView.html", {
            "data": chat_data,
            "tid": int(tid)
        })
    return redirect("Guest:Login")

def clearchat(request):
    if "Rid" in request.session:
        tid = request.GET.get("tid")
        reporter = tbl_reporter.objects.get(id=request.session["Rid"])
        tbl_chat.objects.filter(
            (Q(reporter_from=reporter) & Q(editor_to=tid)) |
            (Q(editor_from=tid) & Q(reporter_to=reporter))
        ).delete()
        return render(request, "Reporter/ClearChat.html", {"msg": "Chat Deleted Successfully"})
    return redirect("Guest:Login")

def EditNews(request, nid):
    if "Rid" in request.session:
        category = tbl_category.objects.all()
        NewsData = tbl_news.objects.get(id=nid)
        if request.method == 'POST':
            NewsData.news_title = request.POST.get("txt_title")
            NewsData.news_content = request.POST.get("txt_content")
            NewsData.subcategory = tbl_subcategory.objects.get(id=request.POST.get("sel_subcategory"))
            if request.FILES.get("file_image"):
                NewsData.news_image = request.FILES.get("file_image")
            NewsData.save()
            return render(request, 'Reporter/EditNews.html', {'msg': 'Updated Successfully'})
        return render(request, 'Reporter/EditNews.html', {
            'category': category,
            'NewsData': NewsData
        })
    return redirect("Guest:Login")

def Logout(request):
    if "Rid" in request.session:
        del request.session["Rid"]
    return redirect("Guest:Login")