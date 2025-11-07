import { motion } from "framer-motion";

export default function ResultDisplay({ result }) {
  if (!result) return null;

  // 🎨 Cores dinâmicas de acordo com o score
  const getColor = (score) => {
    if (score >= 75) return "bg-green-500 text-white";
    if (score >= 50) return "bg-yellow-400 text-gray-800";
    return "bg-red-500 text-white";
  };

  const getBadgeColor = (level) => {
    switch (level) {
      case "high":
        return "bg-blue-100 text-blue-800";
      case "medium":
        return "bg-yellow-100 text-yellow-800";
      default:
        return "bg-red-100 text-red-800";
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className="mt-8 bg-white shadow-xl rounded-xl p-6 w-full max-w-lg mx-auto text-center"
    >
      <h3 className="text-2xl font-bold text-gray-800 mb-2">Resultado da Predição</h3>

      <div
        className={`mx-auto my-6 flex items-center justify-center rounded-full w-32 h-32 text-3xl font-bold shadow-inner ${getColor(
          result.satisfaction_score
        )}`}
      >
        {result.satisfaction_score.toFixed(1)}%
      </div>

      <span
        className={`inline-block mt-2 px-4 py-1 text-sm font-semibold rounded-full ${getBadgeColor(
          result.confidence_level
        )}`}
      >
        Confiança: {result.confidence_level.toUpperCase()}
      </span>

      <p className="mt-4 text-gray-600 italic">
        {result.recommendation}
      </p>
    </motion.div>
  );
}
