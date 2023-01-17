import dbm
from student import app

if __name__ == "__main__":
    with app.app_context(): 
        dbm.create_all()
    app.run(debug = True)