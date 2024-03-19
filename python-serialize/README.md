# Serialize Your Data With Python

This folder contains the sample code for the tutorial [Serialize Your Data With Python](https://realpython.com/python-serialize-data/) published on Real Python.

## Table of Contents

- [Setup](#setup)
- [Usage](#usage)
    - [Python Objects](##python-objects)
        - [Standard Python](#standard-python)
        - [Customize Pickle](#customize-pickle)
        - [JSON Encode](#json-encode)
        - [Foreign Formats](#foreign-formats)
    - [Executable Code](#executable-code)
        - [Pickle-Importable Code](#pickle-importable-code)
        - [Code Objects](#code-objects)
        - [Digital Signature](#digital-signature)
    - [HTTP Payload](#http-payload)
        - [Flask](#flask)
        - [Django REST Framework](#django-rest-framework)
        - [FastAPI](#fastapi)
        - [Pydantic](#pydantic)
    - [Hierarchical Data](#hierarchical-data)
        - [XML, YAML, JSON, BSON](#xml-yaml-json-bson)
    - [Tabular Data](#tabular-data)
        - [CSV](#csv)
        - [Apache Parquet](#apache-parquet)
    - [Schema-Based Formats](#schema-based-formats)
        - [Apache Avro](#apache-avro)
        - [Protocol Buffers (Protobuf)](#protocol-buffers-protobuf)

## Setup

Create and activate a new virtual environment:

```shell
$ python3 -m venv venv/
$ source venv/bin/activate
```

Install the required third-party dependencies:

```shell
(venv) $ python -m pip install -r requirements.txt
```

## Usage

### Python Objects

#### Standard Python

```shell
(venv) $ cd python-objects/standard-python/
(venv) $ python pickle_demo.py
(venv) $ python marshal_demo.py
(venv) $ python shelve_demo.py
(venv) $ python dbm_demo.py
```

#### Customize Pickle

```shell
(venv) $ cd python-objects/customize-pickle/
(venv) $ python main.py
```

#### JSON Encode

```shell
(venv) $ cd python-objects/json-encode/
(venv) $ python main.py
```

#### Foreign Formats

jsonpickle and PyYAML:

```shell
(venv) $ cd python-objects/foreign-formats/
(venv) $ python jsonpickle_demo.py
(venv) $ python pyyaml_demo.py
```

### Executable Code

#### Pickle-Importable Code

```shell
(venv) $ cd executable-code/pickle-importable/
(venv) $ python main.py
```

#### Code Objects

```shell
(venv) $ cd executable-code/code-objects/
(venv) $ python dill_demo.py
```

#### Digital Signature

```shell
(venv) $ cd executable-code/digital-signature/
(venv) $ python main.py
```

### HTTP Payload

#### Flask

Start the web server:

```shell
(venv) $ cd http-payload/flask-rest-api/
(venv) $ flask --app main --debug run
```

Navigate to the "users" resource in your web browser:
<http://127.0.0.1:5000/users>

Send an HTTP GET request to retrieve all users:

```shell
$ curl -s http://127.0.0.1:5000/users | jq
[
  {
    "name": "Alice",
    "id": "512a956f-165a-429f-9ec8-83d859843072",
    "created_at": "2023-11-13T12:29:18.664574"
  },
  {
    "name": "Bob",
    "id": "fb52a80f-8982-46be-bcdd-605932d8ef03",
    "created_at": "2023-11-13T12:29:18.664593"
  }
]
```

Send an HTTP POST request to add a new user:

```shell
$ curl -s -X POST http://127.0.0.1:5000/users \
       -H 'Content-Type: application/json' \
       --data '{"name": "Frank"}' | jq
{
  "name": "Frank",
  "id": "f6d3cae7-f86a-4bc8-8d05-2fb65e8c6f3b",
  "created_at": "2023-11-13T12:31:21.602389"
}
```

#### Django REST Framework

Navigate to the folder:

```shell
(venv) $ cd http-payload/django-rest-api/
```

Apply the migrations if necessary:

```shell
(venv) $ python manage.py migrate
```

Start the Django development web server:

```shell
(venv) $ python manage.py runserver
```

Navigate to the "users" resource in your web browser:
<http://127.0.0.1:8000/users/>

You can use the web interface generated by Django REST Framework to send a POST request to add a new user, for example:

```json
{"name": "Frank"}
```

#### FastAPI

Start the web server:

```shell
(venv) $ cd http-payload/fastapi-rest-api/
(venv) $ uvicorn main:app --reload
```

Navigate to the "users" resource in your web browser:
<http://127.0.0.1:8000/users>

Send an HTTP GET request to retrieve all users:

```shell
$ curl -s http://127.0.0.1:8000/users | jq
[
  {
    "name": "Alice",
    "id": "512a956f-165a-429f-9ec8-83d859843072",
    "created_at": "2023-11-13T12:29:18.664574"
  },
  {
    "name": "Bob",
    "id": "fb52a80f-8982-46be-bcdd-605932d8ef03",
    "created_at": "2023-11-13T12:29:18.664593"
  }
]
```

Send an HTTP POST request to add a new user:

```shell
$ curl -s -X POST http://127.0.0.1:8000/users \
       -H 'Content-Type: application/json' \
       --data '{"name": "Frank"}' | jq
{
  "name": "Frank",
  "id": "f6d3cae7-f86a-4bc8-8d05-2fb65e8c6f3b",
  "created_at": "2023-11-13T12:31:21.602389"
}
```

#### Pydantic

Start the FastAPI server:

```shell
(venv) $ cd http-payload/fastapi-rest-api/
(venv) $ uvicorn main:app --reload
```

Run the REST API consumer:

```shell
(venv) $ cd http-payload/pydantic-demo/
(venv) $ python main.py
```

### Hierarchical Data

#### XML, YAML, JSON, BSON

```shell
(venv) $ cd hierarchical-data/
(venv) $ python bson_demo.py
(venv) $ python yaml_demo.py
```

### Tabular Data

#### CSV

```shell
(venv) $ cd tabular-data/csv-demo/
(venv) $ python main.py
```

#### Apache Parquet

```shell
(venv) $ cd tabular-data/parquet-demo/
(venv) $ python main.py
```

### Schema-Based Formats

#### Apache Avro

```shell
(venv) $ cd schema-based/avro-demo/
(venv) $ python main.py
```

#### Protocol Buffers (Protobuf)

Install the `protoc` compiler:

```shell
$ sudo apt install protobuf-compiler
```

Generate Python code from IDL:

```shell
(venv) $ cd schema-based/protocol-buffers-demo/
(venv) $ protoc --python_out=. --pyi_out=. users.proto
```

Run the demo:

```shell
(venv) $ python main.py
```