import { useState } from "react";
import PredictionForm from "./components/PredictionForm";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-600 to-purple-600 flex flex-col items-center justify-center p-6">
      <PredictionForm onResult={setResult} />

      {result && (
        <div className="mt-6 bg-white shadow-lg rounded-xl p-6 w-full max-w-lg text-center">
          <h3 className="text-2xl font-bold text-gray-800 mb-2">
            Satisfação: {result.satisfaction_score.toFixed(2)}%
          </h3>
          <p className="text-gray-600 italic">{result.recommendation}</p>
          <span className="inline-block mt-3 px-4 py-1 text-sm font-semibold rounded-full bg-blue-100 text-blue-700">
            Confiança: {result.confidence_level.toUpperCase()}
          </span>
        </div>
      )}
    </div>
  );
}

export default App;
