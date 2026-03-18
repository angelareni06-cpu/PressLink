from django.shortcuts import render, redirect
from Admin.models import *
from Reporter.models import *
from Editor.models import *
from User.models import *
from datetime import datetime
from django.db.models import Q

def Homepage(request):
    if "Eid" in request.session:
        return render(request, 'Editor/Homepage.html')
    else:
        return redirect("Guest:Login")

def MyProfile(request):
    if "Eid" in request.session:
        editordata = tbl_editor.objects.get(id=request.session["Eid"])
        return render(request, 'Editor/MyProfileE.html', {"editordata": editordata})
    else:
        return redirect("Guest:Login")

def EditProfile(request):
    if "Eid" in request.session:
        editordata = tbl_editor.objects.get(id=request.session["Eid"])
        if request.method == 'POST':
            editordata.editor_name = request.POST.get("txt_name")
            editordata.editor_email = request.POST.get("txt_email")
            editordata.editor_contact = request.POST.get("txt_contact")
            editordata.save()
            return render(request, 'Editor/EditProfile.html', {'msg': 'updated'})
        else:
            return render(request, 'Editor/EditProfile.html', {"editordata": editordata})
    else:
        return redirect("Guest:Login")

def ChangePassword(request):
    if "Eid" in request.session:
        editordata = tbl_editor.objects.get(id=request.session["Eid"])
        if request.method == 'POST':
            oldpassword = request.POST.get("txt_old")
            newpassword = request.POST.get("txt_new")
            confirm = request.POST.get("txt_confirm")
            if editordata.editor_password == oldpassword:
                if newpassword == confirm:
                    editordata.editor_password = newpassword
                    editordata.save()
                    return render(request, 'Editor/ChangePassword.html', {'msg': 'Password Updated'})
                else:
                    return render(request, 'Editor/ChangePassword.html', {'msg1': 'Password Mismatch'})
            else:
                return render(request, 'Editor/ChangePassword.html', {'msg1': 'Password Incorrect'})
        else:
            return render(request, 'Editor/ChangePassword.html')
    else:
        return redirect("Guest:Login")

def ViewVerifiednews(request):
    if "Eid" in request.session:
        reporternews = tbl_news.objects.filter(
            news_status=1,
            reporter__isnull=False
        )
        freelancernews = tbl_news.objects.filter(
            news_status=6,
            user__isnull=False
        )
        return render(request, 'Editor/ViewVerifiednews.html', {
            'reporternews': reporternews,
            'freelancernews': freelancernews
        })
    else:
        return redirect("Guest:Login")

def TakeNews(request, nid):
    if "Eid" in request.session:
        newsdata = tbl_news.objects.get(id=nid)
        editor = tbl_editor.objects.get(id=request.session["Eid"])
        newsdata.editor = editor
        newsdata.news_status = 7
        newsdata.save()
        return redirect('Editor:MyTakenNews')
    else:
        return redirect("Guest:Login")

def MyTakenNews(request):
    if "Eid" in request.session:
        editor = tbl_editor.objects.get(id=request.session["Eid"])
        NewsData = tbl_news.objects.filter(editor=editor).order_by('-news_date')
        return render(request, 'Editor/MyTakenNews.html', {"NewsData": NewsData})
    else:
        return redirect("Guest:Login")

def PublishedNews(request, pid):
    if "Eid" in request.session:
        publishdata = tbl_news.objects.get(id=pid)
        publishdata.news_status = 8
        publishdata.save()
        return redirect('Editor:MyTakenNews')
    else:
        return redirect("Guest:Login")

def FPublishedNews(request, fid):
    if "Eid" in request.session:
        fpublishdata = tbl_news.objects.get(id=fid)
        fpublishdata.news_status = 8
        fpublishdata.save()
        return redirect('Editor:MyTakenNews')
    else:
        return redirect("Guest:Login")

def NewsUpdatesR(request, nid):
    if "Eid" in request.session:
        newsdata = tbl_news.objects.get(id=nid)
        NewsUpdatesR = tbl_newsupdatesr.objects.filter(news=newsdata)
        if request.method == 'POST':
            if request.POST.get('action') == 'mark_ready':
                if newsdata.news_status == 7:
                    newsdata.news_status = 8
                    newsdata.save()
                    return render(request, 'Editor/NewsUpdatesR.html', {
                        'msg': 'Marked as edited. Awaiting source confirmation.',
                        'newsdata': newsdata,
                        'NewsUpdatesR': NewsUpdatesR,
                        'nid': nid
                    })
                else:
                    return render(request, 'Editor/NewsUpdatesR.html', {
                        'msg': 'News must be in editing status to mark ready.',
                        'newsdata': newsdata,
                        'NewsUpdatesR': NewsUpdatesR,
                        'nid': nid
                    })

            remarks = request.POST.get("txt_remarks")
            editorId = tbl_editor.objects.get(id=request.session['Eid'])
            tbl_newsupdatesr.objects.create(
                newsupdatesr_remarks=remarks,
                news=newsdata,
                editor=editorId
            )
            if newsdata.news_status < 7:
                newsdata.news_status = 7
            newsdata.save()
            return render(request, 'Editor/NewsUpdatesR.html', {
                'msg': 'Remark added and status set to editing (7).',
                'newsdata': newsdata,
                'NewsUpdatesR': NewsUpdatesR,
                'nid': nid
            })
        else:
            return render(request, 'Editor/NewsUpdatesR.html', {
                'newsdata': newsdata,
                'NewsUpdatesR': NewsUpdatesR,
                'nid': nid
            })
    else:
        return redirect("Guest:Login")


def EditNews(request, nid):
    if "Eid" in request.session:
        newsdata = tbl_news.objects.get(id=nid)
        subcategories = tbl_subcategory.objects.all()
        if request.method == 'POST':
            newsdata.news_title = request.POST.get('txt_title')
            newsdata.news_content = request.POST.get('txt_content')
            if request.FILES.get('file_image'):
                newsdata.news_image = request.FILES.get('file_image')
            newsdata.subcategory = tbl_subcategory.objects.get(id=request.POST.get('sel_subcategory'))
            newsdata.news_status = 8
            newsdata.save()
            return redirect('Editor:NewsUpdatesR', nid=nid)
        return render(request, 'Editor/EditNews.html', {
            'newsdata': newsdata,
            'subcategories': subcategories
        })
    else:
        return redirect('Guest:Login')


def delremarks(request, did, nid):
    tbl_newsupdatesr.objects.get(id=did).delete()
    return redirect("Editor:NewsUpdatesR", nid)

def ViewFiles(request, nid):
    if "Eid" in request.session:
        uploaddata = tbl_uploadfiles.objects.filter(news=nid)
        return render(request, 'Editor/ViewFiles.html', {'uploaddata': uploaddata, 'nid': nid})
    else:
        return redirect("Guest:Login")

def ViewAdvertisement(request):
    if "Eid" in request.session:
        advdata = tbl_advertisement.objects.filter(advertisement_status=4)
        return render(request, 'Editor/ViewAdvertisement.html', {'advdata': advdata})
    else:
        return redirect("Guest:Login")

def Confirm(request, fid):
    if "Eid" in request.session:
        confirmdata = tbl_advertisement.objects.get(id=fid)
        editor = tbl_editor.objects.get(id=request.session["Eid"])
        confirmdata.advertisement_status = 5
        confirmdata.editor_id = editor
        confirmdata.save()
        return redirect('Editor:ViewAdvertisement')
    else:
        return redirect("Guest:Login")

def Reject(request, fid):
    if "Eid" in request.session:
        confirmdata = tbl_advertisement.objects.get(id=fid)
        confirmdata.advertisement_status = 6
        confirmdata.save()
        return redirect('Editor:ViewAdvertisement')
    else:
        return redirect("Guest:Login")
    
def ViewRAccept(request,aid,nid):
    acceptdata=tbl_uploadfiles.objects.get(id=aid)
    acceptdata.upload_status=1
    acceptdata.editor=tbl_editor.objects.get(id=request.session['Eid'])
    acceptdata.save()
    return redirect('Editor:ViewFiles',nid)

def ViewRReject(request,rid,nid):
    rejectdata=tbl_uploadfiles.objects.get(id=rid)
    rejectdata.upload_status=2
    rejectdata.save()
    return redirect('Editor:ViewFiles',nid)  

def Complaint(request):
    if "Eid" in request.session:
        editor = tbl_editor.objects.get(id=request.session["Eid"])
        complaintdata = tbl_complaint.objects.filter(editor_id=editor)
        if request.method == "POST":
            title = request.POST.get("txt_title")
            content = request.POST.get("txt_content")
            tbl_complaint.objects.create(
                complaint_title=title,
                complaint_content=content,
                editor_id=editor,
                complaint_date=datetime.now()
            )
            return render(request, "Editor/Complaint.html", {
                "msg": "Complaint Submitted",
                "complaintdata": complaintdata
            })
        else:
            return render(request, "Editor/Complaint.html", {"complaintdata": complaintdata})
    else:
        return redirect("Guest:Login")

def delcomplaint(request, id):
    if "Eid" in request.session:
        tbl_complaint.objects.get(id=id).delete()
        return redirect("Editor:Complaint")
    else:
        return redirect("Guest:Login")

def chatpage(request, id):
    if "Eid" in request.session:
        user = tbl_user.objects.get(id=id)
        return render(request, "Editor/Chat.html", {"user": user})
    else:
        return redirect("Guest:Login")

def ajaxchat(request):
    if "Eid" in request.session:
        from_editor = tbl_editor.objects.get(id=request.session["Eid"])
        to_user = tbl_user.objects.get(id=request.POST.get("tid"))
        tbl_chat.objects.create(
            chat_content=request.POST.get("msg"),
            chat_time=datetime.now(),
            editor_from=from_editor,
            user_to=to_user,
            chat_file=request.FILES.get("file")
        )
        return render(request, "Editor/Chat.html")
    else:
        return redirect("Guest:Login")

def ajaxchatview(request):
    if "Eid" in request.session:
        tid = request.GET.get("tid")
        editor = tbl_editor.objects.get(id=request.session["Eid"])
        user = tbl_user.objects.get(id=tid)
        chat_data = tbl_chat.objects.filter(
            (Q(editor_from=editor) & Q(user_to=user)) |
            (Q(user_from=user) & Q(editor_to=editor))
        ).order_by("chat_time")
        return render(request, "Editor/ChatView.html", {
            "data": chat_data,
            "tid": tid
        })
    else:
        return redirect("Guest:Login")

def clearchat(request):
    if "Eid" in request.session:
        tid = request.GET.get("tid")
        editor = tbl_editor.objects.get(id=request.session["Eid"])
        user = tbl_user.objects.get(id=tid)
        tbl_chat.objects.filter(
            (Q(editor_from=editor) & Q(user_to=user)) |
            (Q(user_from=user) & Q(editor_to=editor))
        ).delete()
        return render(request, "Editor/ClearChat.html", {
            "msg": "Chat Deleted Successfully..."
        })
    else:
        return redirect("Guest:Login")

def chatpager(request, id):
    if "Eid" in request.session:
        reporter = tbl_reporter.objects.get(id=id)
        return render(request, "Editor/ChatR.html", {"reporter": reporter})
    else:
        return redirect("Guest:Login")

def ajaxchatr(request):
    if "Eid" in request.session:
        from_editor = tbl_editor.objects.get(id=request.session["Eid"])
        to_reporter = tbl_reporter.objects.get(id=request.POST.get("tid"))
        tbl_chat.objects.create(
            chat_content=request.POST.get("msg"),
            chat_time=datetime.now(),
            editor_from=from_editor,
            reporter_to=to_reporter,
            chat_file=request.FILES.get("file")
        )
        return render(request, "Editor/ChatR.html")
    else:
        return redirect("Guest:Login")

def ajaxchatviewr(request):
    if "Eid" in request.session:
        tid = request.GET.get("tid")
        editor = tbl_editor.objects.get(id=request.session["Eid"])
        reporter = tbl_reporter.objects.get(id=tid)
        chat_data = tbl_chat.objects.filter(
            (Q(editor_from=editor) & Q(reporter_to=reporter)) |
            (Q(reporter_from=reporter) & Q(editor_to=editor))
        ).order_by("chat_time")
        return render(request, "Editor/ChatViewR.html", {
            "data": chat_data,
            "tid": tid
        })
    else:
        return redirect("Guest:Login")

def clearchatr(request):
    if "Eid" in request.session:
        tid = request.GET.get("tid")
        editor = tbl_editor.objects.get(id=request.session["Eid"])
        reporter = tbl_reporter.objects.get(id=tid)
        tbl_chat.objects.filter(
            (Q(editor_from=editor) & Q(reporter_to=reporter)) |
            (Q(reporter_from=reporter) & Q(editor_to=editor))
        ).delete()
        return render(request, "Editor/ClearChat.html", {
            "msg": "Chat Deleted Successfully..."
        })
    else:
        return redirect("Guest:Login")

def Logout(request):
    if "Eid" in request.session:
        del request.session["Eid"]
    return redirect("Guest:Login")