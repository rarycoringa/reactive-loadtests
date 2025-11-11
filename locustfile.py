import random
import uuid

from locust import HttpUser, task, between


available_user_ids = [
    "68f7b7a0abcaab3f62083003", "68f7b841f05374f289c2cc94", "68f9b0fb5493f3c689493dc1",
    "68f9b0fc5493f3c689493dc2", "68f9b0fd5493f3c689493dc3", "68f9b0fd5493f3c689493dc4",
    "68f9b0fe5493f3c689493dc5", "68f9b0ff5493f3c689493dc6", "68f9b0ff5493f3c689493dc7",
    "68f9b1005493f3c689493dc8", "68f9b1005493f3c689493dc9", "68f9b1015493f3c689493dca", 
    "68f9b1015493f3c689493dcb", "68f9b1025493f3c689493dcc", "68f9b1025493f3c689493dcd",
    "68f9b1035493f3c689493dce", "68f9b1035493f3c689493dcf", "68f9b1045493f3c689493dd0",
    "68f9b1045493f3c689493dd1", "68f9b1055493f3c689493dd2", "68f9b1075493f3c689493dd3",
    "68f9b1075493f3c689493dd4", "68f9b2265493f3c689493dd5", "68f9b2315493f3c689493dd6",
]


class RestAPIUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def create_a_post(self):
        endpoint = "/post/restapi/posts"
        headers = {"Content-Type": "application/json"}

        user_id = random.choice(available_user_ids)

        payload = {
            "content": f"Hello, world! This is my post {uuid.uuid4()} with RestAPI",
            "user_id": user_id,
        }

        with self.client.post(
            endpoint,
            json=payload,
            headers=headers,
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status {response.status_code}")
    
    @task(2)
    def retrieve_an_user(self):
        user_id = random.choice(available_user_ids)
        endpoint = f"/user/restapi/users/{user_id}"
        headers = {"Content-Type": "application/json"}

        with self.client.get(
            endpoint,
            headers=headers,
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status {response.status_code}")

    @task(1)
    def retrieve_my_posts(self):
        endpoint = f"/post/restapi/posts"
        headers = {"Content-Type": "application/json"}

        user_id = random.choice(available_user_ids)
        params = {"user_id": user_id}

        with self.client.get(
            endpoint,
            headers=headers,
            params=params,
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status {response.status_code}")


class GraphQLUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def create_a_post(self):
        endpoint = "/post/graphql"
        headers = {"Content-Type": "application/json"}

        mutation = """
        mutation Save($input: CreatePostInput!) {
            save(createPostInput: $input) {
                id
                content
                user {
                    id
                    name
                    age
                }
                comments {
                    content
                    user {
                        name
                    }
                }
            }
        }
        """

        user_id = random.choice(available_user_ids)

        payload = {
            "query": mutation,
            "variables": {
                "input": {
                    "content": f"Hello, world! This is my post {uuid.uuid4()} with GraphQL",
                    "userId":  user_id,
                }
            },
        }

        with self.client.post(
            endpoint,
            json=payload,
            headers=headers,
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()["data"]["save"]
                    post_id = data["id"]
                    response.success()
                except Exception as e:
                    response.failure("Mutation returned unexpected data: " + str(e))
                    return

    @task(2)
    def retrieve_an_user(self):
        user_id = random.choice(available_user_ids)
        endpoint = "/user/graphql"
        headers = {"Content-Type": "application/json"}

        query = """
        query GetById($id: String!) {
            getById(id: $id) {
                id
                name
                age
                createdAt
            }
        }
        """

        payload = {
            "query": query,
            "variables": {"id": user_id},
        }

        with self.client.post(endpoint, json=payload, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                try:
                    data = response.json()["data"]["getById"]
                    response.success()
                except Exception as e:
                    response.failure("Query returned unexpected data: " + str(e))
            else:
                response.failure(f"Query failed: {response.status_code}")

    @task(1)
    def retrieve_my_posts(self):
        user_id = random.choice(available_user_ids)
        endpoint = "/post/graphql"
        headers = {"Content-Type": "application/json"}

        query = """
        query GetAllByUserId($userId: String!) {
            getAllByUserId(userId: $userId) {
                content
                user {
                    name
                }
                comments {
                    content
                }
                createdAt
            }
        }
        """

        payload = {
            "query": query,
            "variables": {"userId": user_id},
        }

        with self.client.post(endpoint, json=payload, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                try:
                    data = response.json()["data"]["getAllByUserId"]
                    response.success()
                except Exception as e:
                    response.failure("Query returned unexpected data: " + str(e))
            else:
                response.failure(f"Query failed: {response.status_code}")