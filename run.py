from messaging_api import app, db


if __name__ == '__main__':
    Test = None
    @app.before_first_request
    def create_tables():
        Test = 'created the tables. Yes.'
        db.create_all()


    app.run(port=5003, debug=True)

