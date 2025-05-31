import { useAuth0 } from "@auth0/auth0-react";
import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function UserMenu() {
  const { user, isAuthenticated, logout } = useAuth0();
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();
  const menuRef = useRef();

  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  if (!isAuthenticated) return null;

  const firstName = user?.given_name || user?.name?.split(" ")[0] || "User";

  return (
    <div className="relative" ref={menuRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 focus:outline-none"
      >
        <img
          src={user.picture}
          alt="Profile"
          className="w-10 h-10 rounded-full border border-gray-300"
        />
        <span className="text-gray-800 font-medium hidden sm:inline">{firstName}</span>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10 border">
          <ul className="py-1 text-sm text-gray-700">
            <li
              className="hover:bg-gray-100 px-4 py-2 cursor-pointer"
              onClick={() => {
                navigate("/dashboard");
                setIsOpen(false);
              }}
            >
              🏠 Dashboard
            </li>
            <li
              className="hover:bg-gray-100 px-4 py-2 cursor-pointer"
              onClick={() => {
                navigate("/history");
                setIsOpen(false);
              }}
            >
              🕓 History
            </li>
            <li
              className="hover:bg-gray-100 px-4 py-2 cursor-pointer"
              onClick={() => {
                navigate("/settings");
                setIsOpen(false);
              }}
            >
              ⚙️ Settings
            </li>
            <li
              className="hover:bg-gray-100 px-4 py-2 cursor-pointer text-red-600"
              onClick={() => logout({ returnTo: window.location.origin })}
            >
              🚪 Log Out
            </li>
          </ul>
        </div>
      )}
    </div>
  );
}
