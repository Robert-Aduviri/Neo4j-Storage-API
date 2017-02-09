from neo4j.v1 import GraphDatabase, basic_auth
from flask import Flask, request
from flask_restful import Resource, Api

driver = GraphDatabase.driver("bolt://localhost:7687",
                    auth=basic_auth("neo4j", "admin"))

app = Flask(__name__)
api = Api(app)

class Person(Resource):
    def get(self, name):
        print("GET")
        session = driver.session()
        result = session.run(("MATCH (a:Person) "
                    "WHERE a.name = '{}'"
                    "RETURN a.name AS name, "
                    "a.age AS age".format(name)))
        res = []
        for record in result:
            res += {'name': record['name'],
                    'age': record['age']}
        print(res)
        session.close()
        return dict(res)

    def post(self, name):
        print("POST")
        data = request.get_json()
        session = driver.session()
        session.run(("CREATE (a:Person {{name: '{0}', "
                 "age: '{1}' }})".format(data['name'],
                                       data['age'])))
        print(data)
        session.close()
        return {'message': 'Person added'}

class Neo4jDatabase(Resource):
    def get(self):
        print("GET ALL")
        session = driver.session()
        result = session.run("MATCH (a:Person) "
                "RETURN a.name AS name, a.age AS age")
        res = []
        for record in result:
            print(record)
            res.append({'name': record["name"],
                    'age': record["age"]})
        print(res)
        session.close()
        return {'objects': res}

    def delete(self):
        print("DELETE1")
        session = driver.session()
        session.run("MATCH (n) DETACH DELETE n")
        print("deleting")
        session.close()
        return {'message': 'Database cleared'}

api.add_resource(Person, '/person/<string:name>')
api.add_resource(Neo4jDatabase, '/objects')
print("LAUNCHING")
app.run(port=5000, debug=True)
