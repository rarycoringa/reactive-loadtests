load-saga:
    uv run locust --host http://localhost:8080 \
        --headless --users 5000 --spawn-rate 250 --run-time 2min \
        --html report-ministore-application.html \
        WebFluxAPIUser

web:
    uv run locust --host http://localhost:8080