import SummaryViewer from "./components/SummaryViewer";
import ChatBox from './components/ChatBox';

function App() {
  return (
    <div className="px-4 sm:px-6 lg:px-8 py-6 max-w-full sm:max-w-2xl lg:max-w-5xl mx-auto font-sans bg-gray-50 rounded-2xl shadow-md mt-10">
      <h1 className="text-3xl font-bold mb-4">🧠 LLM News App</h1>
      <SummaryViewer />
      <div className="mt-8"></div>
        <ChatBox />
    </div>
  );
}

export default App;
