from django.urls import path
from Verifier import views

app_name = "Verifier"

urlpatterns = [

    # ===== HOME =====
    path("Homepage/", views.Homepage, name="Homepage"),

    # ===== PROFILE =====
    path("MyProfile/", views.MyProfile, name="MyProfile"),
    path("EditProfile/", views.EditProfile, name="EditProfile"),
    path("ChangePassword/", views.ChangePassword, name="ChangePassword"),

    # ===== FREELANCER NEWS =====
    path("ViewNewsF/", views.ViewNewsF, name="ViewNewsF"),
    path("ViewAccept/<int:aid>/", views.ViewAccept, name="ViewAccept"),
    path("ViewReject/<int:rid>/", views.ViewReject, name="ViewReject"),

    # ===== REPORTER NEWS =====
    path("ViewNewsR/", views.ViewNewsR, name="ViewNewsR"),
    path("ViewRAccept/<int:aid>/", views.ViewRAccept, name="ViewRAccept"),
    path("ViewRReject/<int:rid>/", views.ViewRReject, name="ViewRReject"),

    # ===== COMPLAINT =====
    path("Complaint/", views.Complaint, name="Complaint"),
    path("delcomplaint/<int:id>/", views.delcomplaint, name="delcomplaint"),

    # ===== ADVERTISEMENT =====
    path("ViewAdvertisement/", views.ViewAdvertisement, name="ViewAdvertisement"),
    path("AdvAccept/<int:aid>/", views.AdvAccept, name="AdvAccept"),
    path("AdvReject/<int:rid>/", views.AdvReject, name="AdvReject"),

    # ===== LOGOUT =====
    path("Logout/", views.Logout, name="Logout"),

]