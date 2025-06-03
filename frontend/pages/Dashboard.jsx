import SummaryViewer from "../src/components/SummaryViewer";
import ChatBox from "../src/components/ChatBox";
import Layout from "../src/components/Layout";

export default function Dashboard() {
  return (
    <Layout>
    <div className="px-4 sm:px-6 lg:px-8 py-6 max-w-full sm:max-w-2xl lg:max-w-5xl mx-auto font-sans bg-gray-50 rounded-2xl shadow-md mt-10">
      <SummaryViewer />
      <div className="mt-8" />
      <ChatBox />
    </div>
    </Layout>
  );
}