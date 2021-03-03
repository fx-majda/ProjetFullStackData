from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        print(modulename)
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "enqueteur.HodViews":
                    pass
                elif modulename == "enqueteur.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename =="django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse("indexAdmin"))
            elif user.user_type == "2":
                if modulename == "enqueteur.StaffViews" or modulename == "enqueteur.EditResultVIewClass":
                    pass
                elif modulename == "enqueteur.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("indexEnqueteur"))

            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if request.path == reverse("index") or modulename == "enqueteur.views" or request.path == reverse("service") or request.path == reverse("auth_re_password") or request.path == reverse("actualite") or request.path == reverse("actualite_detail") or request.path == reverse("faq") or request.path == reverse("signup") or request.path == reverse("contact") or request.path == reverse("login") or modulename == "django.contrib.auth.views" or modulename =="django.contrib.admin.sites" :
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))