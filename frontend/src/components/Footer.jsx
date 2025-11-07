export default function Footer() {
  return (
    <footer className="mt-10 py-4 text-center text-sm text-gray-200 bg-transparent">
      <p>
        © {new Date().getFullYear()} <span className="font-semibold">Benefit Predictor</span>.{" "}
        Desenvolvido por{" "}
        <a
          href="https://github.com/soares-ari"
          target="_blank"
          rel="noopener noreferrer"
          className="underline hover:text-white transition"
        >
          Ari Soares
        </a>
        .
      </p>

      <p className="text-gray-400 mt-1">
        API v1.0.0 — Django + React + ML
      </p>
    </footer>
  );
}
