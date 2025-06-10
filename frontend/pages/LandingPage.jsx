import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import UserMenu from "../src/components/UserMenu";

export default function LandingPage() {
  const {
    loginWithRedirect,
    logout,
    isAuthenticated,
    user,
    getIdTokenClaims,
  } = useAuth0();

  const navigate = useNavigate();

  // Auto-redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      console.log("🟢 Authenticated user:", user);

      getIdTokenClaims()
        .then((claims) => {
          console.log("🟢 ID Token claims:", JSON.stringify(claims, null, 2));
        })
        .catch((e) => {
          console.error("🔴 Failed to get ID token claims:", e);
        });
      }
    }, [isAuthenticated, user, getIdTokenClaims]);

  useEffect(() => {
    if (isAuthenticated) {
      const timer = setTimeout(() => {
        navigate("/dashboard");
      }, 10); // Give logging time to finish

      return () => clearTimeout(timer);
    }
    }, [isAuthenticated, navigate]);

  const handleLogin = () => {
    loginWithRedirect({
      authorizationParams: {
        scope: "openid profile email read:summary",
        prompt: "consent",
      },
    });
  };

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">Welcome to LLM News App</h1>
      <UserMenu />
      {isAuthenticated ? (
        <>
          <p className="mb-2">Logged in as {user.name || user.email}</p>
          <button
            className="text-blue-600 underline"
            onClick={() => logout({ returnTo: window.location.origin })}
          >
            Log out
          </button>
        </>
      ) : (
        <button className="text-blue-600 underline" onClick={handleLogin}>
          Log in
        </button>
      )}
    </div>
  );
}
