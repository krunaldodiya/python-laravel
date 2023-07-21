def main(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [environ["PATH_INFO"].encode("utf-8")]
