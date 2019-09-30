# Simple Instruction
### Build docker image `testcase:0.0.1` from `Dockerfile`
```bash
docker build -t localhost:5000/testcase:0.0.1 .
```
### Create registry container
```bash
docker-compose up -d registry
```
### Push `testcase:0.0.1` to registry
```bash
docker push localhost:5000/testcase:0.0.1
```
### Create application container
```bash
docker-compose up -d
```
### Browse host on 80 port
```bash
curl --verbose 'http://localhost/history?name=testcase&tag=0.0.1' 
```
