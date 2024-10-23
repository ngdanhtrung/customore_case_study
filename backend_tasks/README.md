# Explanation
Since the case study is simple, I reused a project that I had already done. The project is a simple delivery system that allows the user to create an order and track it. I had deleted mostly everything that was not necessary for the case study, only keeping the project structure.
In this case study, I just used one ModelViewSet to managing the tasks. You can check it in `develivery-server/delivery/services.task` directory. The model is in `develivery-server/delivery/models.py` file.
I recommend using the docker installation but you can use the local installation if you want. The docker installation is more straightforward and you don't need to worry about the dependencies.

# Install guide

## Local installation

### Virtual environment

Create a virtual environment and active with the following command:

```bash
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows

```

### Install dependencies

```bash
cd delivery-server
pip install -r requirements.txt
poetry install
```

### Run the server

```bash
python manage.py runserver
```

## Docker installation (Recommended)

```bash
docker-compose up
```

# Migration

```bash
python manage.py migrate
```

# API Documentation and testing
If you are using the docker installation, you can access the API documentation in the following link: [http://localhost:8000/docs/](http://localhost:8000/docs/)

# Improvements
Since the case study is simple, I think I can't add any improvements about optimize the API or database design.
For extending the project, I would add a user authentication for the API and make some relationships between users and tasks. (eg. a user can only see their tasks, or a user can assign a task to another user.). I would also add a queue system to manage the tasks and a notification system to notify the user about the task status or remind them about the deadline. This would make the project like other task management systems like Trello or Asana. 😂