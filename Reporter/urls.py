from django.urls import path
from Reporter import views

app_name = "Reporter"

urlpatterns = [

    # Dashboard
    path("Homepage/", views.Homepage, name="Homepage"),

    # Profile
    path("MyProfile/", views.MyProfile, name="MyProfile"),
    path("EditProfile/", views.EditProfile, name="EditProfile"),
    path("ChangePassword/", views.ChangePassword, name="ChangePassword"),

    # News
    path("AddNews/", views.AddNews, name="AddNews"),
    path("EditNews/<int:nid>/", views.EditNews, name="EditNews"),
    path("delnews/<int:id>/", views.delnews, name="delnews"),

    # Upload
    path("UploadFiles/<int:nid>/", views.UploadFiles, name="UploadFiles"),
    path("delfile/<int:id>/<int:nid>/", views.delfile, name="delfile"),


    # Complaint
    path("Complaint/", views.Complaint, name="Complaint"),
    path("delcomplaint/<int:id>/", views.delcomplaint, name="delcomplaint"),

    # Chat
    path("chatpage/<int:id>/", views.chatpage, name="chatpage"),
    path("ajaxchat/", views.ajaxchat, name="ajaxchat"),
    path("ajaxchatview/", views.ajaxchatview, name="ajaxchatview"),
    path("clearchat/", views.clearchat, name="clearchat"),

    # My News
    path("MyNews/", views.MyNews, name="MyNews"),
    path("ConfirmEdits/<int:id>/", views.ConfirmEdits, name="ConfirmEdits"),
    path("ViewUpdatesR/<int:nid>/", views.ViewUpdatesR, name="ViewUpdatesR"),

    # Logout
    path("Logout/", views.Logout, name="Logout"),

]