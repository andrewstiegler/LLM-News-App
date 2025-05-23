import { useEffect, useState } from "react";

function SummaryViewer() {
  const [summary, setSummary] = useState("");
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/summaries")
      .then((res) => res.json())
      .then((data) => {
        setSummary(data.daily_summary);
        setArticles(data.articles);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching summaries:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">📰 Daily Summary</h2>
      <p className="mb-6 whitespace-pre-line">{summary}</p>

      <h3 className="text-lg font-semibold mb-4">Articles</h3>
      <div className="grid grid-cols-1 gap-6">
        {articles.map((a, i) => (
          <div
            key={i}
            className="bg-white rounded-lg shadow-md p-5 border border-gray-200 hover:shadow-lg transition-shadow"
          >
            <a
              href={a.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-700 text-lg font-semibold hover:underline"
            >
              {a.title || a.url}
            </a>
            {/* Optional: you could add a snippet or source here */}
          </div>
        ))}
      </div>
    </div>
  );
}

export default SummaryViewer;
