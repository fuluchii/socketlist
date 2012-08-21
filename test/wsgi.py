from redis import Redis
import web

urls = (
        '/','index',
        '/mark','showList'
        )
class index:
    def GET(self):
        return 'hello'
class showList:
    def GET(self):
        return 'redis'

app = web.application(urls,globals())
application = app.wsgifunc()
if(__name__=="__main__"):
    app.run()
