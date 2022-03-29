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
def test_return(client):
    response = client.delete('/todos/1')
    assert response.status_code == 200