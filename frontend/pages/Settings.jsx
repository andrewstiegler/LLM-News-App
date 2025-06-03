import Layout from "../src/components/Layout";
import { useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import axios from "axios";

export default function Settings() {
  const { user } = useAuth0();
  const [prompt, setPrompt] = useState("");
  const [status, setStatus] = useState(null);
  const {getAccessTokenSilently} = useAuth0();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus("Running...");

    try {
      const token = await getAccessTokenSilently({
          authorizationParams: {
            audience: import.meta.env.VITE_AUTH0_AUDIENCE
          }
      });
      
      const res = await axios.post("http://127.0.0.1:5000/api/run_pipeline", {
        user_id: user.sub,
        user_prompt: prompt,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`, // ⬅️ Add bearer token to request
          "Content-Type": "application/json",
        },});

      if (res.data.status === "success") {
        setStatus("✅ Pipeline ran successfully!");
      } else {
        setStatus("❌ Pipeline failed.");
      }
    } catch (err) {
      setStatus("❌ Error calling API.");
      console.error(err);
    }
  };

  return (
    <Layout>
      <div className="px-4 py-6 max-w-3xl mx-auto font-sans">
        <h2 className="text-2xl font-bold mb-4">⚙️ Settings</h2>
        <p className="mb-4">
          Enter a custom prompt to guide your news summary generation:
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g. Give me the top 3 healthcare M&A stories"
            className="w-full px-4 py-2 border rounded-md"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded-md"
          >
            Run News Pipeline
          </button>
        </form>

        {status && <p className="mt-4">{status}</p>}
      </div>
    </Layout>
  );
}
