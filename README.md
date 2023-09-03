###

1. docker build -t api:v1 . 

2. docker run -dit --rm -p 8000:8000 --name api api:v1 

3. ===> http://127.0.0.1:8000/