import { useEffect, useState } from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

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

  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 3, // Show 3 articles at a time
    slidesToScroll: 1,
    responsive: [ // Adjust slidesToShow for smaller screens
      {
        breakpoint: 1024, // tablets
        settings: {
          slidesToShow: 2,
        }
      },
      {
        breakpoint: 600, // mobile
        settings: {
          slidesToShow: 1,
        }
      }
    ]
  };

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">📰 Daily Summary</h2>
      <p className="mb-6 whitespace-pre-line">{summary}</p>

      <h3 className="text-lg font-semibold mb-4">Articles</h3>
      <Slider {...settings}>
        {articles.map((a, i) => (
          <div
            key={i}
            className="p-2" // Added padding for spacing between slides
          >
            <div
              className="bg-white rounded-lg shadow-md p-5 border border-gray-200 hover:shadow-lg transition-shadow h-full" // Added h-full for consistent height
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
          </div>
        ))}
      </Slider>
    </div>
  );
}

export default SummaryViewer;
