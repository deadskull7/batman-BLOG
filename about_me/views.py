from django.shortcuts import render

def aboutme(request):
	return render(request, 'about_me/abme.html')