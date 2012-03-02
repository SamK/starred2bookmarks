#!/usr/bin/python -B
import web
import model
import os

#render = web.template.render('templates/', base='layout')
#render_plain = web.template.render('templates/')

urls = (
    '/', 'Index',
    #'/convert', 'Convert',
    '/about', 'About',
    #'/(.*)', 'Page'

)

template_globals = {}
render_partial = web.template.render('./templates/', globals=template_globals)
render = web.template.render('./templates/', globals=template_globals, base='layout')
template_globals.update(render=render_partial)

def notfound():
    return web.notfound(render.notfound())

def internalerror():
    return web.internalerror(render.internalerror())

class Index:
    def GET(self):
        return render.index("")

    def POST(self):
        x = web.input(myfile={})
        print "processing"
        print x.myfile
        if not x.myfile.value:
            errmsg = "The file is not!? 3"
            return render.index(errmsg)

        # download file
        web.header('Content-Type', x.myfile.type) # file type
        # force browser to show "Save as" dialog.
        web.header('Content-disposition',
                   'attachment; filename='+ x.myfile.filename + '.json') 
        return x.myfile.value # your blob 

class About:
    def GET(self):
        return render.about()

#app = web.application(urls, globals())
#app.notfound = notfound

#app.internalerror = internalerror

# dev
#web.webapi.internalerror = web.debugerror
#if __name__ == "__main__": web.run(urls, globals(), web.reloader)

#web.config.debug = False

# prod
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

