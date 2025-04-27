# MongoChef

A fast and friendly desktop recipe manager built with MongoDB, FastAPI, and Tkinter.

## 🚀 Getting Started

### Folder structure diagram

        └── 📁MongoChef
        └── 📁app
                └── database.py
                └── main.py
                └── 📁models
                └── 📁routers
                └── 📁schemas
                └── 📁utils
        └── 📁gui
        └── .gitignore
        └── README.md
        └── requirements.txt

### Prerequisites

Make sure you have the following installed:

- [Python 3.12.10](https://www.python.org/downloads/release/python-31210/)
- [MongoDB](https://www.mongodb.com/docs/manual/installation/)

### Installing

Follow these steps to set up a development environment:

1. Clone de repository.

        git clone https://github.com/alemr214/MongoChef.git
        cd MongoChef

2. Create and activate a virtual environment (optional but recommended):

        python -m venv .env
        source .env/bin/activate  # Linux/macOS
        .env\Scripts\activate     # Windows

3. Install the dependencies:

        pip install -r requirements.txt

4. Ensure MongoDB is running locally on your machine.

5. Run the application.

        python main.py

## Example Usage

Once running, MongoChef allows you to add, edit, and organize recipes through a simple graphical interface.

## 🌐 Deployment

For production deployment:

- Set up MongoDB on a production server.
- Configure the FastAPI server with a WSGI/ASGI server like Gunicorn or Uvicorn.
- Package the Tkinter application into an executable using tools like PyInstaller.

## Built With

- [FastAPI](https://fastapi.tiangolo.com)
- [MongoDB](https://www.mongodb.com)
- [Tkinter](https://docs.python.org/es/3.13/library/tkinter.html)

## 👨‍💻 Authors

- **Alejandro Martinez Rivera** - *Project creator* -
    [alemr214](https://github.com/alemr214)

See also the list of
[contributors](https://github.com/alemr214/MongoChef/contributors)
who participated in this project.

## Acknowledgments

- To Mr. "Mike", professor of the subject NoSQL at ITVer, who gives me the task to develop this project.
- To my friends who they are in the Discord app at midnight talking about everything buy still yet to hear me.
- My girlfriend, 'cause she doesn't understand anything about programming, despite that she supports me in everything.
