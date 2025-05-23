import SummaryViewer from "./components/SummaryViewer";
import ChatBox from './components/ChatBox';

function App() {
  return (
    <div className="p-6 max-w-3xl mx-auto font-sans bg-white rounded-2xl shadow-md mt-10">
      <h1 className="text-3xl font-bold mb-4">🧠 LLM News App</h1>
      <SummaryViewer />
      <div className="mt-8"></div>
        <ChatBox />
    </div>
  );
}

export default App;
