function FindingCard({ title, findings }) {

  return (

    <div className="bg-white rounded-lg shadow p-5">

      <h2 className="text-xl font-bold mb-4">

        {title}

      </h2>

      {findings.length === 0 && (

        <p className="text-gray-500">

          No Findings

        </p>

      )}

      {findings.map((finding, index) => (

        <div
          key={index}
          className="border rounded-lg p-4 mb-4 bg-gray-50"
        >

          <div className="flex justify-between mb-2">

            <span className="font-bold text-blue-700">

              {finding.rule_id}

            </span>

            <span
              className={`px-3 py-1 rounded text-white text-sm ${
                finding.severity === "High"
                  ? "bg-red-600"
                  : finding.severity === "Medium"
                  ? "bg-yellow-500"
                  : "bg-green-600"
              }`}
            >
              {finding.severity}
            </span>

          </div>

          <h3 className="font-bold text-lg">

            {finding.title}

          </h3>

          <p className="mt-2">

            {finding.explanation}

          </p>

          <p className="mt-3 text-green-700">

            <strong>Recommendation:</strong>{" "}

            {finding.recommendation}

          </p>

          <div className="mt-3 text-sm text-gray-600">

            <p>

              <strong>Line:</strong> {finding.line}

            </p>

            <p>

              <strong>Column:</strong> {finding.column}

            </p>

            <p>

              <strong>Confidence:</strong>{" "}

              {finding.confidence}%

            </p>

            <p>

              <strong>Tags:</strong>{" "}

              {finding.tags?.join(", ")}

            </p>

          </div>

        </div>

      ))}

    </div>

  );

}

export default FindingCard;