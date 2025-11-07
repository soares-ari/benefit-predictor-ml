import axios from "axios";

// Instância base para o backend Django
const api = axios.create({
    baseURL: "http://localhost:8000/api/",
    headers: {
        "Content-Type": "application/json"
    },
});

export default api;