from website import create_app

app = create_app()
#this only works if "main" is run, if you import main it wont work
if __name__ == '__main__':
    app.run(debug=True)