import { useState } from "react";
import PredictionForm from "./components/PredictionForm";
import ResultDisplay from "./components/ResultDisplay";
import Stats from "./components/Stats";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-600 to-purple-600 flex flex-col items-center justify-start p-6">
      <h1 className="text-white text-3xl font-bold mb-8 drop-shadow-lg">
        Benefit Predictor
      </h1>

      <PredictionForm onResult={setResult} />

      <ResultDisplay result={result} />

      <Stats />
    </div>
  );
}

export default App;
