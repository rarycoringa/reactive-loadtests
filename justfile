load-graphql:
    uv run locust --host http://localhost:8080 \
        --headless --users 3000 --spawn-rate 25 --run-time 2min \
        --html report-graphql-webmvc-pt-v2.html \
        GraphQLUser

load-restapi:
    uv run locust --host http://localhost:8080 \
        --headless --users 3000 --spawn-rate 25 --run-time 2min \
        --html report-restapi-webmvc-pt-v2.html \
        RestAPIUser

web:
    uv run locust --host http://localhost:8080