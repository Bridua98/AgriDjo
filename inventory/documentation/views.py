import mimetypes
import os

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.static import serve

from . import app_settings

DOCUMENTATION_ROOT = 'index.html'


@login_required
def documentation(request, path):
    if path == '':
        path = DOCUMENTATION_ROOT
    if not app_settings.DOCUMENTATION_ACCESS_FUNCTION(request.user):
        return HttpResponseRedirect(app_settings.LOGIN_REDIRECT_URL)
    if not app_settings.DOCUMENTATION_XSENDFILE:
        use_chache = True
        if os.path.isdir(os.path.join(app_settings.DOCUMENTATION_HTML_ROOT, path)):
            path = path + "/index.html"
        if 'assets/' in path:
            use_cache = False
        response = serve(
            request,
            path,
            app_settings.DOCUMENTATION_HTML_ROOT)
        if not use_chache:
            response["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
            response["Pragma"] = "no-cache" # HTTP 1.0.
            response["Expires"] = "0" # Proxies.
        return response
    mimetype, encoding = mimetypes.guess_type(path)
    response = HttpResponse(content_type=mimetype)

    response['Content-Encoding'] = encoding
    response['Content-Disposition'] = ''
    response['X-Sendfile'] = "".join([app_settings.DOCUMENTATION_HTML_ROOT,
                                      path])
    return response
