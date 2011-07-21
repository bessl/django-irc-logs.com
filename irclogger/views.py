from irclogger.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views import generic

def search(request):
    logs = []
    q = ""
    page = 0
    if request.REQUEST.has_key('q'):
        q = request.REQUEST['q']
        if len(q) > 3:
            logs_all = Log.objects.filter(channel=1).filter(msg__icontains=q).order_by("-id")
            paginator = Paginator(logs_all, 30)
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1

            try:
                logs = paginator.page(page)
            except (EmptyPage, InvalidPage):
                logs = paginator.page(paginator.num_pages)

    return render_to_response('irclogger/search.html', {'logs': logs, 'q': q},
            context_instance=RequestContext(request))

class IndexView(generic.TemplateView):
    template_name = 'start.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'archive_days': Log.objects.dates('pub_date', 'day', order='DESC'),
            'last_update': Log.objects.latest('pub_date'),
            'line_count': Log.objects.count(),
            'last_lines': Log.objects.filter(channel=1).order_by("-id")[:20],
        })
        return context
index = IndexView.as_view()
