def includeme(config):
    #config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('static', 'static', cache_max_age=0)
    config.add_static_view('uploads', 'uploads', cache_max_age=0)
    config.add_route('home', '/')

    config.add_route('login','/login')
    config.add_route('logout','/logout')

    #uploads
    config.add_route("avatarupload", "/upload/avatar")

    #Route to show Materials
    config.add_route("materials", "/materials/{moduleId}/{pageId:.*}")
    #As I CBA to make it a modal TODO: MAke this a modal
    config.add_route("newArticle", "/newMaterial/{moduleId}")   

    #Admin Page of Materials
    config.add_route("moduleAdmin", "/admin/{moduleId}")
    config.add_route("moduleRestore", "/restore/{moduleId}")
    config.add_route("studentList", "/studentList/{moduleId}")
    #Route to Show Feed
    config.add_route("feed", "/feed/{moduleId}")
    #config.add_route("feed", "/feed/{*moduleid}")

