import { useState } from "react";
import api from "./services/api";

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

      <h1 className="text-4xl font-bold text-center mb-8">
        AI Code Debugging Agent
      </h1>

      <div className="grid grid-cols-2 gap-6">

        {/* Left */}

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

        {/* Right */}

        <div className="space-y-5">

          <div className="bg-white rounded-lg shadow p-5">

            <h2 className="text-xl font-bold mb-2">
              Parser
            </h2>

            {result && (

              <>
                <p>
                  <b>Language:</b> {result.parser.language}
                </p>

                <p>
                  <b>Syntax:</b>{" "}
                  {result.parser.syntax_valid ? "Valid" : "Invalid"}
                </p>

              </>

            )}

          </div>

          <div className="bg-white rounded-lg shadow p-5">

            <h2 className="text-xl font-bold mb-2">
              Bug Findings
            </h2>

            {result?.bugs.findings.length === 0 && (
              <p>No Bugs Found</p>
            )}

            {result?.bugs.findings.map((bug, index) => (

              <div key={index} className="mb-5">

                <h3 className="font-bold text-red-600">
                  {bug.title}
                </h3>

                <p>{bug.explanation}</p>

                <p className="mt-2 text-green-700">
                  {bug.recommendation}
                </p>

              </div>

            ))}

          </div>

          <div className="bg-white rounded-lg shadow p-5">

            <h2 className="text-xl font-bold mb-2">
              Security Findings
            </h2>

            {result?.security.findings.length === 0 && (
              <p>No Security Issues</p>
            )}

            {result?.security.findings.map((issue, index) => (

              <div key={index} className="mb-5">

                <h3 className="font-bold text-red-600">
                  {issue.title}
                </h3>

                <p>{issue.explanation}</p>

                <p className="mt-2 text-green-700">
                  {issue.recommendation}
                </p>

              </div>

            ))}

          </div>

          <div className="bg-white rounded-lg shadow p-5">

            <h2 className="text-xl font-bold mb-2">
              AI Review
            </h2>

            {result && (

              <>
                <p><b>Summary:</b> {result.ai_review.summary}</p>

                <br />

                <p>
                  <b>Severity:</b> {result.ai_review.severity}
                </p>

                <br />

                <p>
                  <b>Explanation:</b>
                </p>

                <p>{result.ai_review.explanation}</p>

                <br />

                <p>
                  <b>Fix:</b>
                </p>

                <p>{result.ai_review.fix}</p>

                <br />

                <p>
                  <b>Best Practice:</b>
                </p>

                <p>{result.ai_review.best_practice}</p>

              </>

            )}

          </div>

        </div>

      </div>

    </div>

  );

}

export default App;