from django.shortcuts import render, redirect
from Admin.models import *
from Reporter.models import *
from User.models import *

def Homepage(request):
    if "Vid" in request.session:
        return render(request, 'Verifier/HomePage.html')
    return redirect("Guest:Login")

def MyProfile(request):
    if "Vid" in request.session:
        verifierData = tbl_verifier.objects.get(id=request.session["Vid"])
        return render(request, 'Verifier/MyProfile.html', {"verifierData": verifierData})
    return redirect("Guest:Login")

def EditProfile(request):
    if "Vid" in request.session:
        verifierData = tbl_verifier.objects.get(id=request.session["Vid"])
        if request.method == 'POST':
            verifierData.Verifier_name = request.POST.get("txt_name")
            verifierData.Verifier_email = request.POST.get("txt_email")
            verifierData.Verifier_contact = request.POST.get("txt_contact")
            verifierData.save()
            return render(request, 'Verifier/EditProfile.html', {'msg': 'Updated'})
        return render(request, 'Verifier/EditProfile.html', {"verifierData": verifierData})
    return redirect("Guest:Login")

def ChangePassword(request):
    if "Vid" in request.session:
        verifierData = tbl_verifier.objects.get(id=request.session["Vid"])
        if request.method == 'POST':
            if verifierData.verifier_password == request.POST.get("txt_old"):
                if request.POST.get("txt_new") == request.POST.get("txt_confirm"):
                    verifierData.verifier_password = request.POST.get("txt_new")
                    verifierData.save()
                    return render(request, 'Verifier/ChangePassword.html', {'msg': 'Password Updated'})
                else:
                    return render(request, 'Verifier/ChangePassword.html', {'msg1': 'Password Mismatch'})
            else:
                return render(request, 'Verifier/ChangePassword.html', {'msg1': 'Incorrect Password'})
        return render(request, 'Verifier/ChangePassword.html')
    return redirect("Guest:Login")

def ViewNewsF(request):
    if "Vid" in request.session:
        newsdata = tbl_news.objects.filter(user__isnull=False, news_status=0)
        return render(request, 'Verifier/ViewNewsF.html', {'news': newsdata})
    return redirect("Guest:Login")

def ViewAccept(request, aid):
    if "Vid" in request.session:
        acceptdata = tbl_news.objects.get(id=aid)
        acceptdata.news_status = 1
        acceptdata.verifier = tbl_verifier.objects.get(id=request.session['Vid'])
        acceptdata.save()
    return redirect('Verifier:ViewNewsF')

def ViewReject(request, rid):
    if "Vid" in request.session:
        rejectdata = tbl_news.objects.get(id=rid)
        rejectdata.news_status = 2
        rejectdata.save()
    return redirect('Verifier:ViewNewsF')

def ViewNewsR(request):
    if "Vid" in request.session:
        newsdata = tbl_news.objects.filter(reporter__isnull=False, news_status=0)
        return render(request, 'Verifier/ViewNewsR.html', {'news': newsdata})
    return redirect("Guest:Login")

def ViewRAccept(request, aid):
    if "Vid" in request.session:
        acceptdata = tbl_news.objects.get(id=aid)
        acceptdata.news_status = 1
        acceptdata.verifier = tbl_verifier.objects.get(id=request.session['Vid'])
        acceptdata.save()
    return redirect('Verifier:ViewNewsR')

def ViewRReject(request, rid):
    if "Vid" in request.session:
        rejectdata = tbl_news.objects.get(id=rid)
        rejectdata.news_status = 2
        rejectdata.save()
    return redirect('Verifier:ViewNewsR')

def Complaint(request):
    if "Vid" in request.session:
        verifierData = tbl_verifier.objects.get(id=request.session["Vid"])
        complaintData = tbl_complaint.objects.filter(verifier_id=verifierData)
        if request.method == 'POST':
            tbl_complaint.objects.create(
                complaint_title=request.POST.get("txt_title"),
                complaint_content=request.POST.get("txt_content"),
                verifier_id=verifierData
            )
            return render(request, 'Verifier/Complaint.html', {'msg': 'Inserted'})
        return render(request, 'Verifier/Complaint.html',
                      {'verifierData': verifierData, 'complaintData': complaintData})
    return redirect("Guest:Login")

def delcomplaint(request, id):
    if "Vid" in request.session:
        tbl_complaint.objects.get(id=id).delete()
    return redirect("Verifier:Complaint")

def ViewAdvertisement(request):
    if "Vid" in request.session:
        Advdata = tbl_advertisement.objects.filter(advertisement_status=0)
        return render(request, 'Verifier/ViewAdvertisement.html', {'Advdata': Advdata})
    return redirect("Guest:Login")

def AdvAccept(request, aid):
    if "Vid" in request.session:
        acceptdata = tbl_advertisement.objects.get(id=aid)
        acceptdata.advertisement_status = 2   # Approved by Verifier
        acceptdata.verifier = tbl_verifier.objects.get(id=request.session['Vid'])
        acceptdata.save()
    return redirect('Verifier:ViewAdvertisement')

def AdvReject(request, rid):
    if "Vid" in request.session:
        rejectdata = tbl_advertisement.objects.get(id=rid)
        rejectdata.advertisement_status = 1   # Rejected
        rejectdata.save()
    return redirect('Verifier:ViewAdvertisement')

def Logout(request):
    if "Vid" in request.session:
        del request.session["Vid"]
    return redirect("Guest:Login")