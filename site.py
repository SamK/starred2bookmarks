#!/usr/bin/python
import sys, os

# import files in modules
sys.path.insert(0, "/home/samk/modules")

# Import files in current dir
abspath = os.path.dirname(__file__)
sys.path.insert(0, abspath)
if len(abspath) > 0:
    os.chdir(abspath)

import webpy as web
import model
import firefoxize_starred_items as reader

#render = web.template.render('templates/', base='layout')
#render_plain = web.template.render('templates/')

urls = (
    '/', 'Index',
    '/about', 'About',
    '/help', 'Help',
    #'/(.*)', 'Page'
)

render = web.template.render('templates/', base='layout')

def notfound():
    return web.notfound(render.notfound())

def internalerror():
    return web.internalerror(render.internalerror())

class Index:
    def GET(self):
        return render.index("")

    def POST(self):
        x = web.input(myfile={})
        if not x.myfile.value:
            errmsg = "For some reason I can't read your file"
            return render.index(errmsg)

        try:
            data = reader.load_data(x.myfile.value)
        except ValueError:
            print >> sys.stderr, "Wrong file format from user"
            return render.index("Your file does not look like a JSON file.")

        # do the magic
        bookmark = reader.convert(data, False)

        # force browser to show "Save as" dialog.
        web.header('Content-Type', x.myfile.type) # file type
        web.header('Content-disposition',
                   'attachment; filename='+ x.myfile.filename + '.html') 
        model.Increment().increment_users()
        return reader.dump_data(bookmark) # your blob 

class About:
    def GET(self):
        return render.about()

# prod
if __name__ == "__main__":
    print >> sys.stderr, "__name__ == __main__"
    app = web.application(urls, globals())
    app.notfound = notfound
    app.internalerror = internalerror
    app.run()
elif "wsgi" in __name__:
    print >> sys.stderr, "wsgi in__name__"
    application = web.application(urls, globals()).wsgifunc()
    # FIXME
    application.notfound = notfound
    application.internalerror = internalerror
else:
    print >> sys.stderr, "Je ne sais pas quoi faire avec %s" % __name__

