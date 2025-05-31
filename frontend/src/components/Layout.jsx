import { useAuth0 } from "@auth0/auth0-react";
import { useNavigate, useLocation } from "react-router-dom";

export default function Layout({ children }) {
  const { user, logout } = useAuth0();
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    { name: "Dashboard", path: "/dashboard" },
    { name: "History", path: "/history" },
    { name: "Settings", path: "/settings" }
  ];

  const firstName = user?.given_name || user?.name?.split(" ")[0] || "User";

  return (
    <div className="min-h-screen bg-gray-50 font-sans px-4 py-6 max-w-5xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">🧠 LLM News App</h1>

        <div className="relative group">
          <img
            src={user.picture}
            alt="Profile"
            className="w-10 h-10 rounded-full cursor-pointer border-2 border-gray-300"
          />
          <div className="absolute right-0 mt-2 w-48 bg-white shadow-lg rounded-md p-2 opacity-0 group-hover:opacity-100 transition duration-200 z-10">
            <p className="px-4 py-2 text-gray-700 font-medium">{firstName}</p>
            <hr className="my-1" />
            {menuItems
              .filter((item) => item.path !== location.pathname)
              .map((item) => (
                <button
                  key={item.path}
                  onClick={() => navigate(item.path)}
                  className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 text-gray-800"
                >
                  {item.name}
                </button>
              ))}
            <hr className="my-1" />
            <button
              onClick={() => logout({ returnTo: window.location.origin })}
              className="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
            >
              Log out
            </button>
          </div>
        </div>
      </div>

      <main>{children}</main>
    </div>
  );
}
