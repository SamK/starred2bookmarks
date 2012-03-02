import web

render = web.template.render('templates/')

def listing():
    return ["a","b","c"]
