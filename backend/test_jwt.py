from app.auth.security import create_access_token, decode_access_token

token = create_access_token(
    subject="12345",
    role="admin",
)

print(token)

print(decode_access_token(token))