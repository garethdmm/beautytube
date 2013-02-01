
from settings import settings

import httplib
import traceback 
import logging
logger = logging.getLogger(__name__)

def error_handler(self, status_code, **kwargs):
    """Override to implement custom error pages.
    """
    debug = settings['debug']
    if 'exc_info' in kwargs:
        exc_info = kwargs["exc_info"]
        trace_info = ''.join(["%s<br/>" % line for line in traceback.format_exception(*exc_info)])
        request_info = ''.join(["<strong>%s</strong>: %s<br/>" % (k, self.request.__dict__[k] ) for k in self.request.__dict__.keys()])
        error = exc_info[1]
        private_error_report =  """<html>
                         <title>%s</title>
                         <body>
                            <h2>Error</h2>
                            <p>%s</p>
                            <h2>Traceback</h2>
                            <p>%s</p>
                            <h2>Request Info</h2>
                            <p>%s</p>
                         </body>
                       </html>""" % (error, error, 
                                    trace_info, request_info)
        public_error_report = (
            ("<html><title>%(code)d: %(message)s</title>"
            "<body>%(code)d: %(message)s</body></html>") % 
            {"code": status_code,
            "message": httplib.responses[status_code]})
    else:
        public_error_report, private_error_report = (
            ("<html><title>%(code)d: %(message)s</title>"
            "<body>%(code)d: %(message)s</body></html>") % 
            {"code": status_code,
            "message": httplib.responses[status_code]})
            
    if status_code == 404:
        self.render('404.html')
    else:
        self.set_header('Content-Type', 'text/html')
        if debug:
            self.finish(private_error_report)
        else:
            #email_error_report(private_error_report)
            self.finish(public_error_report)
       
