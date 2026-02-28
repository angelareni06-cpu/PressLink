from django.urls import path
from User import views

app_name = "User"

urlpatterns = [

    # ===== HOME =====
    path("Homepage/", views.Homepage, name="Homepage"),

    # ===== PROFILE =====
    path("MyProfile/", views.MyProfile, name="MyProfile"),
    path("EditProfile/", views.EditProfile, name="EditProfile"),
    path("ChangePassword/", views.ChangePassword, name="ChangePassword"),

    # ===== NEWS =====
    path("UploadNews/", views.UploadNews, name="UploadNews"),
    path("EditNews/<int:fid>/", views.EditNews, name="EditNews"),
    path("delnews/<int:id>/", views.delnews, name="delnews"),
    path("AjaxSubcategory/", views.AjaxSubcategory, name="AjaxSubcategory"),

    # ===== EXTRA FILES =====
    path("UploadF/<int:fid>/", views.UploadF, name="UploadF"),
    path("delfile/<int:id>/<int:fid>/", views.delfile, name="delfile"),
    path("ViewUpdatesF/<int:fid>/", views.ViewUpdatesF, name="ViewUpdatesF"),

    # ===== MY NEWS TRACKING =====
    path("MyNews/", views.MyNews, name="MyNews"),
    path("AcceptAmount/<int:id>/", views.AcceptAmount, name="AcceptAmount"),
    path("RejectAmount/<int:id>/", views.RejectAmount, name="RejectAmount"),
    path("ConfirmEdits/<int:id>/", views.ConfirmEdits, name="ConfirmEdits"),

    # ===== COMPLAINT =====
    path("Complaint/", views.Complaint, name="Complaint"),
    path("delcomplaint/<int:id>/", views.delcomplaint, name="delcomplaint"),

    # ===== CHAT WITH ADMIN =====
    path("chatpage_usertoadmin/",views.chatpage_usertoadmin,name="chatpage_usertoadmin"),
    path("ajaxchat_usertoadmin/",views.ajaxchat_usertoadmin,name="ajaxchat_usertoadmin"),
    path("ajaxchatview_usertoadmin/",views.ajaxchatview_usertoadmin,name="ajaxchatview_usertoadmin"),
    path("clearchat_usertoadmin/",views.clearchat_usertoadmin,name="clearchat_usertoadmin"),

    # ===== CHAT WITH EDITOR =====
    path("chatpage_usertoeditor/<int:id>/",views.chatpage_usertoeditor,name="chatpage_usertoeditor"),
    path("ajaxchat_usertoeditor/",views.ajaxchat_usertoeditor,name="ajaxchat_usertoeditor"),
    path("ajaxchatview_usertoeditor/",views.ajaxchatview_usertoeditor,name="ajaxchatview_usertoeditor"),
    path("clearchat_usertoeditor/",views.clearchat_usertoeditor,name="clearchat_usertoeditor"), 

    # ===== ADVERTISEMENT =====
    path("Advertisement/", views.Advertisement, name="Advertisement"),
    path("delAdv/<int:id>/", views.delAdv, name="delAdv"),
    path("MyAdvertisement/", views.MyAdvertisement, name="MyAdvertisement"),

    # ===== PAYMENT GATEWAY =====
    path("Payment/<int:pid>/", views.Payment, name="Payment"),
    path("loader/", views.loader, name="loader"),
    path("paymentsuc/", views.paymentsuc, name="paymentsuc"),

    # ===== LOGOUT =====
    path("Logout/", views.Logout, name="Logout"),

    path("viewplan/", views.viewplan, name="viewplan"),
    path("Subscribe/<int:pid>", views.Subscribe, name="Subscribe"),

]