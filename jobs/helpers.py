import secrets

def make_token() -> str:
    """
    Creates a cryptographically-secure, URL-safe string
    """
    return secrets.token_urlsafe(16)  

if __name__ == "__main__":
    print(make_token())