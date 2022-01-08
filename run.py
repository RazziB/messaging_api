from messaging_api import app, db


if __name__ == '__main__':

    @app.before_first_request
    def create_tables():
        db.create_all()


    app.run(port=5003, debug=True)

