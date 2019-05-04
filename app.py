import flask
import werkzeug.middleware.proxy_fix

from views import api
from views import customer
from views import public
from lib.security import security


# FREE FLOATING SECTION STARTS HERE

app = flask.Flask(__name__, static_folder='web/public/',
    static_url_path='/public')

app.register_blueprint(api.API_VIEWS)
app.register_blueprint(customer.CUSTOMER_VIEWS)
app.register_blueprint(public.PUBLIC_VIEWS)
app.register_blueprint(security.SECURITY)

app.wsgi_app = werkzeug.middleware.proxy_fix.ProxyFix(app.wsgi_app)
app.secret_key = None
# app.secret_key = config.get_value(config.APP_SECRET_KEY)
if app.secret_key is None:
    app.secret_key = 'e5fce5faa2e20b203c014f358f73c48f7129084ab1643c9fa6a0f87ff7a546a2'

# FREE FLOATING SECTION ENDS HERE


def main():
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
