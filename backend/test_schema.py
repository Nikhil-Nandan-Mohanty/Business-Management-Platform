from app.auth.schemas import UserRegistration

user = UserRegistration(
    full_name="Raghu Ram",
    email="raghu@example.com",
    password="Raghu@1234",
)

print(user.model_dump())