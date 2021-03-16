from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return view_func(request, *args, **kwargs)
	return wrapper_func


def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'Admins':
			return view_func(request, *args, **kwargs)
		else:
			return redirect('login')

	return wrapper_function