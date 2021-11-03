from locust import HttpUser, task

class AppUser(HttpUser):
    host = "http://localhost:8000"  
    
    @task
    def predict(self):
        self.client.get("/predict")