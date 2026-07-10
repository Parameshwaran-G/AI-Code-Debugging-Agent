import { useState } from "react";
import api from "./services/api";

import SummaryCards from "./components/SummaryCards.jsx";
import ParserCard from "./components/ParserCard.jsx";
import FindingCard from "./components/FindingCard.jsx";
import AIReview from "./components/AIReview.jsx";

function App() {

  const [code, setCode] = useState(`def f():
    return f()

f()`);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  async function analyzeCode() {

    setLoading(true);

    try {

      const response = await api.post("/review", {
        code: code
      });

      setResult(response.data);

    } catch (err) {

      console.error(err);
      alert("Backend is not running.");

    } finally {

      setLoading(false);

    }

  }

  return (

    <div className="min-h-screen bg-gray-100 p-8">

      <h1 className="text-4xl font-bold text-center">
        AI Code Debugging Agent
      </h1>

      <p className="text-center text-gray-600 mb-8">
        Rule-Based Static Analysis + AI Review
      </p>

      <div className="grid grid-cols-2 gap-6">

        {/* Left Panel */}

        <div>

          <textarea
            className="w-full h-[650px] p-4 rounded-lg border bg-white font-mono text-sm"
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />

          <button
            onClick={analyzeCode}
            disabled={loading}
            className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg"
          >
            {loading ? "Analyzing..." : "Analyze Code"}
          </button>

        </div>

        {/* Right Panel */}

        <div className="space-y-5">

          {result && (

            <>
              <SummaryCards result={result} />

              <ParserCard parser={result.parser} />

              <FindingCard
                title="Bug Findings"
                findings={result.bugs.findings}
              />

              <FindingCard
                title="Security Findings"
                findings={result.security.findings}
              />

              <AIReview review={result.ai_review} />

            </>

          )}

        </div>

      </div>

    </div>

  );

}

export default App;