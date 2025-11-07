import { useState } from "react";
import api from "../services/api";

export default function PredictionForm({ onResult }) {
  // 🧠 Estados dos campos do formulário
  const [formData, setFormData] = useState({
    age: "",
    salary: "",
    commute_time: "",
    gym_usage: "",
    meal_voucher: "",
    health_plan_tier: "1",
  });

  // 🎡 Estados de controle
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // 🧩 Atualiza os campos dinamicamente
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  // 🚀 Submissão do formulário
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await api.post("/predict/", formData);
      onResult(response.data); // envia o resultado para o componente pai
    } catch (err) {
      console.error("Erro na previsão:", err);
      setError("Falha ao processar predição. Verifique os dados.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-xl shadow-lg p-6 space-y-4 max-w-lg mx-auto"
    >
      <h2 className="text-2xl font-semibold text-center text-blue-600 mb-4">
        Predict Employee Satisfaction
      </h2>

      {/* Campos */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Idade
          </label>
          <input
            type="number"
            name="age"
            value={formData.age}
            onChange={handleChange}
            min="18"
            max="100"
            required
            className="w-full border-2 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Salário (EUR)
          </label>
          <input
            type="number"
            name="salary"
            value={formData.salary}
            onChange={handleChange}
            min="1320"
            required
            className="w-full border-2 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Tempo de Deslocamento (min)
          </label>
          <input
            type="number"
            name="commute_time"
            value={formData.commute_time}
            onChange={handleChange}
            min="0"
            max="300"
            required
            className="w-full border-2 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Uso da Academia (dias/mês)
          </label>
          <input
            type="number"
            name="gym_usage"
            value={formData.gym_usage}
            onChange={handleChange}
            min="0"
            max="30"
            required
            className="w-full border-2 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Vale-Refeição (EUR)
          </label>
          <input
            type="number"
            name="meal_voucher"
            value={formData.meal_voucher}
            onChange={handleChange}
            min="0"
            required
            className="w-full border-2 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Plano de Saúde
          </label>
          <select
            name="health_plan_tier"
            value={formData.health_plan_tier}
            onChange={handleChange}
            className="w-full border-2 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="1">Básico</option>
            <option value="2">Padrão</option>
            <option value="3">Premium</option>
          </select>
        </div>
      </div>

      {/* Botão e status */}
      <div className="text-center mt-6">
        <button
          type="submit"
          disabled={loading}
          className={`${
            loading
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700"
          } text-white font-semibold py-3 px-6 rounded-lg transition`}
        >
          {loading ? "Processando..." : "Fazer Predição"}
        </button>

        {error && (
          <p className="text-red-600 font-medium mt-3 text-sm">{error}</p>
        )}
      </div>
    </form>
  );
}
