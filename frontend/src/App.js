import { useEffect } from "react";
import api from "./services/api";

function App() {
  useEffect(() => {
    api.get("health/")
      .then((res) => console.log("✅ API conectada:", res.data))
      .catch((err) => console.error("❌ Erro na conexão:", err.message));
  }, []);

  return (
    <div className="h-screen flex flex-col items-center justify-center bg-gradient-to-r from-blue-600 to-purple-600 text-white">
      <h1 className="text-5xl font-bold mb-4">Benefit Predictor</h1>
      <p className="text-lg opacity-90">Conectando ao backend...</p>
    </div>
  );
}

export default App;
