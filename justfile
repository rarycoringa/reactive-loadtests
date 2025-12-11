load-saga:
    uv run locust --host http://localhost:8080 \
        --headless --users 20000 --spawn-rate 500 --run-time 2min \
        --html report-orchestration-rabbitmq.html \
        WebFluxAPIUser

web:
    uv run locust --host http://localhost:8080