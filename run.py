from flask import Flask

import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config) # 추가

    from main import main_bp 
    from main import socketio
    
    app.register_blueprint(main_bp)
    socketio.init_app(app)

    return app, socketio

app, socketio = create_app()
    
if __name__=='__main__':
    
    socketio.run(app, debug=True)