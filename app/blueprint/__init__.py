from .api import api_bp
from .manage import manage_bp
# from .manage import manage_bp

'''
蓝图这一块 还用到了flask-restful,接口是用restful写的
可以照着接口文档看,容易理解些
'''


def register(app):
    app.register_blueprint(api_bp, url_prefix='/api')  # 这个是小程序调用的
    app.register_blueprint(manage_bp, url_prefix='/manage')  # 这个是管理后台页面调用的
