from functools import wraps
from flask import request, jsonify
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError
import requests
from backend.utils.config import AUTH0_DOMAIN, AUTH0_API_AUDIENCE
from core.seed_users import seed_user

AUTH0_DOMAIN = AUTH0_DOMAIN
API_AUDIENCE = AUTH0_API_AUDIENCE
ALGORITHMS = ["RS256"]
JWKS_URL = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"


def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        return None
    parts = auth.split()
    if parts[0].lower() != "bearer" or len(parts) != 2:
        return None
    return parts[1]


def get_jwks():
    try:
        return requests.get(JWKS_URL).json()
    except Exception as e:
        print(f"🔴 Failed to fetch JWKS: {e}")
        return None


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        if not token:
            return jsonify({"message": "Authorization header is missing or malformed"}), 401

        try:
            unverified_header = jwt.get_unverified_header(token)
            print(f"🔐 JWT Header: {unverified_header}")
        except Exception as e:
            print(f"🔴 Failed to parse token header: {e}")
            return jsonify({"message": "Invalid token header"}), 401

        jwks = get_jwks()
        if not jwks:
            return jsonify({"message": "Unable to fetch JWKS"}), 500

        rsa_key = {}
        for key in jwks["keys"]:
            if key.get("kid") == unverified_header.get("kid"):
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        if not rsa_key:
            return jsonify({"message": "Appropriate key not found in JWKS"}), 401

        try:
            # Decode token with audience verification disabled
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/"
            )

        except ExpiredSignatureError:
            return jsonify({"message": "Token is expired"}), 401
        except JWTClaimsError as e:
            print(f"🔴 JWT claims error: {e}")
            try:
                decoded_unverified = jwt.get_unverified_claims(token)
            except Exception as ue:
                return jsonify({"message": "Incorrect claims"}), 401
        except Exception as e:
            print(f"🔴 Token parsing failed: {e}")
            return jsonify({"message": "Unable to parse authentication token."}), 401
        # Seed the user in DB if not exists
        
        user_info = {
                "sub": payload.get("sub"),
                "email": payload.get("email"),
                "name": payload.get("name"),
            }
        
        print("🟢 Calling seed_user with:", user_info)

        seed_user(
            user_id=user_info['sub'],
            email=user_info['email'],
            name=user_info.get('name')
        )

        # Optionally, you can add user_info to flask.g for downstream use
        from flask import g
        g.user = user_info
        return f(payload, *args, **kwargs)

    return decorated