import lib.parseinput

def application(environ, start_response):
    length = int(environ.get('CONTENT_LENGTH', '0'))
    body = environ['wsgi.input'].read(length)
    p = lib.parseinput.ParseInput()
    r = p.oddeye(body)
    resp = str(r)
    start_response(resp + ' OK', [('Content-Type', 'text/plain')])
    yield resp.encode('utf-8')
