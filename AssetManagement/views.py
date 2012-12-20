from django.http import HttpResponse
import datetime


#Write View that forces computers to be of type computer


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
