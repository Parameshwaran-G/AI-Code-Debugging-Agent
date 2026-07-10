function AIReview({ review }) {

  return (

    <div className="bg-white rounded-lg shadow p-5">

      <h2 className="text-xl font-bold mb-4">

        AI Review

      </h2>

      <div className="space-y-5">

        <div>

          <h3 className="font-semibold">

            Summary

          </h3>

          <p>{review.summary}</p>

        </div>

        <div>

          <h3 className="font-semibold">

            Severity

          </h3>

          <p>{review.severity}</p>

        </div>

        <div>

          <h3 className="font-semibold">

            Explanation

          </h3>

          <p>{review.explanation}</p>

        </div>

        <div>

          <h3 className="font-semibold">

            Fix

          </h3>

          <p>{review.fix}</p>

        </div>

        <div>

          <h3 className="font-semibold">

            Best Practice

          </h3>

          <p>{review.best_practice}</p>

        </div>

      </div>

    </div>

  );

}

export default AIReview;