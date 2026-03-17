from django.urls import path, include
from Admin import views

app_name = "Admin"

urlpatterns = [
    path("HomePage/", views.HomePage, name="HomePage"),
    path("Logout/", views.Logout, name="Logout"),

    path("AdminRegistration/", views.AdminRegistration, name="AdminRegistration"),
    path("deladmin/<int:id>", views.deladmin, name="deladmin"),
    path("editadmin/<int:id>", views.editadmin, name="editadmin"),

    path("EditorRegistration/", views.EditorRegistration, name="editorregistration"),
    path("deleditor/<int:id>/", views.deleditor, name="deleditor"),
    path("BlockEditor/<int:eid>/", views.BlockEditor, name="BlockEditor"),
    path("UnblockEditor/<int:eid>/", views.UnblockEditor, name="UnblockEditor"),

    path("VerifierRegistration/", views.VerifierRegistration, name="verifierregistration"),
    path("delverifier/<int:id>/", views.delverifier, name="delverifier"),
    path("BlockVerifier/<int:vid>/", views.BlockVerifier, name="BlockVerifier"),
    path("UnblockVerifier/<int:vid>/", views.UnblockVerifier, name="UnblockVerifier"),

    path("Reporterverification/", views.Reporterverification, name="reporterverification"),
    path("ReporterAccept/<int:aid>", views.ReporterAccept, name="ReporterAccept"),
    path("ReporterReject/<int:rid>", views.ReporterReject, name="ReporterReject"),
    path("Userverification/", views.Userverification, name="userverification"),
    path("BlockUser/<int:uid>/", views.BlockUser, name="BlockUser"),
    path("UnblockUser/<int:uid>/", views.UnblockUser, name="UnblockUser"),

    path("District/", views.District, name="District"),
    path("deldistrict/<int:id>", views.deldistrict, name="deldistrict"),
    path("editdistrict/<int:id>", views.editdistrict, name="editdistrict"),

    path("Place/", views.Place, name="Place"),
    path("delplace/<int:id>", views.delplace, name="delplace"),
    path("editplace/<int:id>", views.editplace, name="editplace"),

    path("Category/", views.Category, name="Category"),
    path("delcategory/<int:id>", views.delcategory, name="delcategory"),
    path("editcategory/<int:id>", views.editcategory, name="editcategory"),

    path("Subcategory/", views.Subcategory, name="Subcategory"),
    path("delsub/<int:id>", views.delsub, name="delsub"),
    path("editsub/<int:id>", views.editsub, name="editsub"),

    path("FreelancerType/", views.FreelancerType, name="freelancertype"),
    path("delfreelancer/<int:id>", views.delfreelancer, name="delfreelancer"),
    path("editfreelancer/<int:id>", views.editfreelancer, name="editfreelancer"),

    path("SkillType/", views.SkillType, name="SkillType"),
    path("delskill/<int:id>", views.delskill, name="delskill"),
    path("editskill/<int:id>", views.editskill, name="editskill"),

    path("PublishedNews/", views.PublishedNews, name="PublishedNews"),
    path("FPublishedNews/", views.FPublishedNews, name="FPublishedNews"),
    path("AddPayment/<int:id>/", views.AddPayment, name="AddPayment"),
    path("AdminPayUser/<int:id>/", views.AdminPayUser, name="AdminPayUser"),
    path("PublishNews/<int:id>/", views.PublishNews, name="PublishNews"),
    path("ViewFiles/<int:fid>", views.ViewFiles, name="ViewFiles"),
    path("ViewComplaints/", views.ViewComplaints, name="viewComplaints"),
    path("Reply/<int:id>", views.Reply, name="Reply"),

    path("Advertisement/", views.Advertisement, name="Advertisement"),
    path("PaymentAdvertisement/<int:id>/", views.PaymentAdvertisement, name="PaymentAdvertisement"),
    path("PublishAdvertisement/<int:id>/", views.PublishAdvertisement, name="PublishAdvertisement"),

    path("Plan/", views.Plan, name="Plan"),
    path("delplan/<int:id>", views.delplan, name="delplan"),


    path("AddSalary/<int:id>/<str:type>/", views.AddSalary, name="AddSalary"),

    path("chatpage/<int:id>", views.chatpage, name="chatpage"),
    path("ajaxchat/", views.ajaxchat, name="ajaxchat"),
    path("ajaxchatview/", views.ajaxchatview, name="ajaxchatview"),
    path("clearchat/", views.clearchat, name="clearchat"),  

    path('Loader/', views.Loader, name='Loader'),
    path('Payment_suc/', views.Payment_suc, name='Payment_suc'),
]