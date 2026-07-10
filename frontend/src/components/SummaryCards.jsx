function SummaryCards({ result }) {

  const bugCount = result.bugs.findings.length;
  const securityCount = result.security.findings.length;
  const total = bugCount + securityCount;

  const severity =
    result.ai_review?.severity || "None";

  return (

    <div className="grid grid-cols-4 gap-4">

      <div className="bg-white rounded-lg shadow p-4 text-center">

        <p className="text-gray-500 text-sm">
          Bugs
        </p>

        <h2 className="text-3xl font-bold text-red-600">
          {bugCount}
        </h2>

      </div>

      <div className="bg-white rounded-lg shadow p-4 text-center">

        <p className="text-gray-500 text-sm">
          Security
        </p>

        <h2 className="text-3xl font-bold text-orange-600">
          {securityCount}
        </h2>

      </div>

      <div className="bg-white rounded-lg shadow p-4 text-center">

        <p className="text-gray-500 text-sm">
          Highest Severity
        </p>

        <h2 className="text-2xl font-bold">

          {severity}

        </h2>

      </div>

      <div className="bg-white rounded-lg shadow p-4 text-center">

        <p className="text-gray-500 text-sm">
          Total
        </p>

        <h2 className="text-3xl font-bold text-blue-600">
          {total}
        </h2>

      </div>

    </div>

  );

}

export default SummaryCards;