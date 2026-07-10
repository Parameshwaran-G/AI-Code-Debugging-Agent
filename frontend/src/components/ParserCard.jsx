function ParserCard({ parser }) {

  return (

    <div className="bg-white rounded-lg shadow p-5">

      <h2 className="text-xl font-bold mb-4">

        Parser Information

      </h2>

      <div className="space-y-2">

        <p>

          <strong>Language:</strong> {parser.language}

        </p>

        <p>

          <strong>Syntax:</strong>{" "}

          <span
            className={
              parser.syntax_valid
                ? "text-green-600 font-semibold"
                : "text-red-600 font-semibold"
            }
          >
            {parser.syntax_valid ? "Valid" : "Invalid"}
          </span>

        </p>

      </div>

    </div>

  );

}

export default ParserCard;