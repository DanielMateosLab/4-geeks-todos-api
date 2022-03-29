import toml, pytest, os, sys, tempfile, mock, json
from flask import Flask

@pytest.fixture
def client():
    with mock.patch('flask.Flask', lambda x: Flask(x)):
        from src.app import app
        db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True

        with app.test_client() as client:
            # with app.app_context():
            #     app.init_db()
            yield client

        os.close(db_fd)
        os.unlink(app.config['DATABASE'])


"""
Testing DELETE
"""

@pytest.mark.it("The function delete_todo should be declared")
def test_delete():
    from src import app
    try:
        app.delete_todo
        assert callable(app.delete_todo)
    except AttributeError:
        raise AttributeError("The function 'delete_todo' should exist on app.py")

@pytest.mark.it("The endpoint 'DELETE /todos' should exist")
def test_delete_code(client):
    response = client.delete('/todos/0')
    assert response.status_code == 200

@pytest.mark.it("DELETE /todos should return json list of todos")
def test_simple_delete(client):
    response = client.delete('/todos/0')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

@pytest.mark.it("The json that returns from the DELETE /todos should have one less item")
def test_delete_and_get(client):
    client.post('todos', json={"mock": "todo"})
    response = client.get('/todos')
    todos = json.loads(response.data)
    
    response2 = client.delete('/todos/0')
    data = json.loads(response2.data)

    assert (len(todos) - 1) == len(data)