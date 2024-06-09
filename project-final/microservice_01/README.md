# Using Protobuf

- In Dockerfile, in Linux command, add this command: 
'protobuf-compiler \'

- Create a file with '.proto' extension and write a data-model like:
'syntax = "proto3";
message Todo {
  int32 id = 1;
  string title = 2;
  string content = 3;
  bool is_completed = 4;
}'

- In project file, add the following dependency through poetry:
'protobuf'

- Run the Docker Desktop and execute the command:
'docker compose up -d' or 'docker compose up --build -d'

- Run docker in integrated enviroment:
'docker exec -it container_name /bin/bash'

- Check the version from this command:
'protoc --version'

- Enter into project directory by using 'cd' command
- Run the following command for python
'protoc --python_out=. file_name.proto'

- Now, import '.pb2' file into main.py

- Write producer code in main.py:
'todos_protobuf = todos_pb2.Todo(
        id = todo.id,
        title = todo.title,
        content = todo.content,
        is_completed = todo.is_completed
    )
    serialized_todos = todos_protbuf.SerializeToString()
    await producer.send_and_wait(str(settings.KAFKA_TODOS_TOPIC), serialized_todos)'

- Write consumer code in main.py:
'new_todos = todos_pb2.Todo()
new_todos.ParseFromString(msg.value)
print(f"Consumer's Deserialized data -> {new_todos}")'

- To run docker, to see running dockers, to see logs and clean docker desktop, use following commands:
'docker compose up -d container_name'
'docker compose ps'
'docker compose logs -f container_name'
'docker compose prune container_name'