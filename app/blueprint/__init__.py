from .user import user_bp
# from .manage import manage_bp

'''
蓝图这一块 还用到了flask-restful,接口是用restful写的
可以照着接口文档看,容易理解些
'''


def register(app):
    app.register_blueprint(user_bp, url_prefix='/user')
