import { useEffect, useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import ReactMarkdown from "react-markdown";

function SummaryViewer() {
  const { getAccessTokenSilently } = useAuth0();
  const [summary, setSummary] = useState("");
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expanded, setExpanded] = useState(false);

  const apiUrl = import.meta.env.VITE_API_URL;

  useEffect(() => {
    async function fetchSummaries() {
      try {
        const token = await getAccessTokenSilently({
          authorizationParams: {
            audience: import.meta.env.VITE_AUTH0_AUDIENCE
          }
      });

        const res = await fetch(`${apiUrl}/api/summaries`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }

        const data = await res.json();
        setSummary(data.daily_summary);
        setArticles(data.articles);
      } catch (err) {
        console.error("Error fetching summaries:", err);
        setError(err.message || "Error fetching summaries");
      } finally {
        setLoading(false);
      }
    }

    fetchSummaries();
  }, [getAccessTokenSilently]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  const settings = {
    dots: true,
    arrows: true,
    infinite: true,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 1,
    responsive: [
      { breakpoint: 1024, settings: { slidesToShow: 2 } },
      { breakpoint: 600, settings: { slidesToShow: 1 } },
    ],
  };

  const toggleExpanded = () => setExpanded(!expanded);

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4 text-primary">📰 Daily Summary</h2>

      <div className="text-gray-800 text-base leading-relaxed transition-all duration-300 ease-in-out mb-4">
        <p className={expanded ? "" : "line-clamp-3 whitespace-pre-line"}>
          <ReactMarkdown>{summary}</ReactMarkdown>
        </p>
        <button
          onClick={toggleExpanded}
          className="mt-2 text-blue-600 font-medium hover:underline"
        >
          {expanded ? "Show less ▲" : "Read more ▼"}
        </button>
      </div>

      <h3 className="text-lg font-semibold mb-4">Articles</h3>
      <Slider {...settings}>
        {articles.map((a, i) => (
          <div key={i} className="p-2">
            <div className="bg-gray-100 rounded-lg shadow-md p-5 border border-gray-200 hover:shadow-lg transition-shadow h-64 flex flex-col gap-y-2">
              <a
                href={a.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-700 text-lg font-semibold hover:underline line-clamp-3"
              >
                {a.title || a.url}
              </a>
              <p className="text-sm text-gray-600 line-clamp-6">{a.summary}</p>
            </div>
          </div>
        ))}
      </Slider>
    </div>
  );
}

export default SummaryViewer;
