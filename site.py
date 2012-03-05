#!/usr/bin/python -B
import web
import model
import os
import firefoxize_starred_items as reader

#render = web.template.render('templates/', base='layout')
#render_plain = web.template.render('templates/')

urls = (
    '/', 'Index',
    '/about', 'About',
    '/help', 'Help',
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
        if not x.myfile.value:
            errmsg = "The file is not!? 3"
            return render.index(errmsg)
        incrementor = model.Increment()
        incrementor.increment_users()

        # download file
        web.header('Content-Type', x.myfile.type) # file type
        # force browser to show "Save as" dialog.

        data = reader.load_data(x.myfile.value)
        bookmark = reader.convert(data, False)

        web.header('Content-disposition',
                   'attachment; filename='+ x.myfile.filename + '.html') 
        return reader.dump_data(bookmark) # your blob 

class About:
    def GET(self):
        return render.about()

# prod
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

