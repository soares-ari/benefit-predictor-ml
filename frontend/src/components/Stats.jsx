import { useEffect, useState } from "react";
import api from "../services/api";
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";

export default function Stats() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.get("/predictions/stats/");
        setStats(response.data);
      } catch (err) {
        console.error("Erro ao buscar estatísticas:", err);
        setError("Falha ao carregar estatísticas");
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="text-center text-gray-600 mt-6">
        Carregando estatísticas...
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center text-red-600 mt-6 font-medium">{error}</div>
    );
  }

  if (!stats) return null;

  const COLORS = ["#ef4444", "#facc15", "#22c55e"]; // vermelho, amarelo, verde
  const chartData = [
    { name: "Baixa", value: stats.distribution.low },
    { name: "Média", value: stats.distribution.medium },
    { name: "Alta", value: stats.distribution.high },
  ];

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 mt-8 w-full max-w-3xl mx-auto">
      <h2 className="text-2xl font-semibold text-gray-800 text-center mb-6">
        Estatísticas de Predições
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
        <div className="bg-blue-50 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-blue-600">
            Total de Predições
          </h3>
          <p className="text-2xl font-bold text-blue-800">
            {stats.total_predictions}
          </p>
        </div>

        <div className="bg-green-50 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-green-600">
            Média de Satisfação
          </h3>
          <p className="text-2xl font-bold text-green-800">
            {stats.average_score.toFixed(2)}%
          </p>
        </div>

        <div className="bg-purple-50 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-purple-600">
            Alta Satisfação
          </h3>
          <p className="text-2xl font-bold text-purple-800">
            {stats.distribution.high}
          </p>
        </div>
      </div>

      {/* Gráfico */}
      <div className="mt-8" style={{ height: 300 }}>
        <ResponsiveContainer>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
              label={({ name, value }) => `${name}: ${value}`}
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
