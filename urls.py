from django.conf.urls.defaults import patterns, include, url
from django.views.generic import dates
from django.views import generic
from django.views.decorators.cache import never_cache

from irclogger.models import Log, CHANNELS
from irclogger import views

class LogBase():
    queryset = Log.objects.filter(channel=CHANNELS[0][0])
    date_field = 'pub_date'

class LogDayArchive(LogBase, generic.DayArchiveView):
    pass

class LogTodayArchive(LogBase, generic.TodayArchiveView):
    pass

urlpatterns = patterns('',
    url(r'^today/$', never_cache(LogTodayArchive.as_view())),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/$', LogDayArchive.as_view()),
    url(r'^search/$', 'irclogger.views.search'),
    url(r'^$', never_cache(views.index), name='index'),
)
