import web
import redis
#urls
url = (
	'/mark','showList',
	'/save','saveUrl',
        '/register','register',
        '/','index',
        '/login','login'
	)
r = redis.Redis(host='savelist-fuluchii.dotcloud.com',port=27908,password='jSexmJ421RON83OTT3nk',db=0)

render = web.template.render('templates/')

web.config.smtp_server = 'smtp.gmail.com'
web.config.smtp_port = 587
web.config.smtp_username='chainyzhao@gmail.com'
web.config.smtp_password = 'watakushi#*'
web.config.smtp_starttls = True

class showList:
  def GET(self):
        name = web.cookies().get('marks')
	shops = r.smembers(name)
        marks = ''
        array ='var markers = ['
        i = 0
        for shopurl in shops:
             marks = marks + ('var m%d =new google.maps.LatLng(%s,%s);' % (i,r.lindex(shopurl,1),r.lindex(shopurl,2)))
             array = array + ('m%d,' % i)
             i = i+1
        array = array[0:-1]+'];'
        marks = marks + array
	return render.showList(marks,shops,name)

class register:
    def GET(self):
        return  render.register()

    def POST(self):
        i = web.input()
        if(r.exists(i.name)):
            web.seeother('mark')
        r.set(i.email,i.name)
        web.setcookie('marks',i.name,3600)
        web.sendmail('chainyzhao@gmail.com',i.email,'welcome','test email')
        web.seeother('mark')
        
class saveUrl:
  def GET(self):
	i = web.input()
        name = web.cookies().get('marks')
	r.sadd(name,i.url)
	r.rpush(i.url,i.title)
        r.rpush(i.url,i.lat)
        r.rpush(i.url,i.lng)
	r.save()
	web.seeother(i.url)

class index:
    def GET(self):
        info = 'test'
        if web.cookies().get('marks') == None:
            web.seeother
        return render.index(info)

class login:
    def GET(self):
        return render.login()

    def POST(self):
        if(r.exists(web.input().name)):
            web.setcookie('marks',r.get(web.input().name),3600)
            web.seeother('mark')
        else:
            web.seeother('/login')


def auth(handler):
    if((web.ctx.path == '/login') or (web.ctx.path == '/register')):
        return handler()
    if web.cookies().get('marks') == None:
        web.seeother('login')
    result = handler()
    return result



app = web.application(url,globals())
app.add_processor(auth)
application = app.wsgifunc()
if(__name__ == "__main__"):
    app.run()

  
