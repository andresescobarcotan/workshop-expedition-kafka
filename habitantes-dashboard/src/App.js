import React, { useEffect, useState } from "react";
import { getHabitanteInfo, ejecutarGommage } from "./api";
import HabitanteCard from "./components/HabitanteCard";

function App() {
  const [habitantes, setHabitantes] = useState([]);
  const [loading, setLoading] = useState(true);

  const nombres = ["Emma", "Marco", "Chloe", "Pintora"];

  const cargarHabitantes = async () => {
    const data = await Promise.all(nombres.map(getHabitanteInfo));
    setHabitantes(data);
    setLoading(false);
  };

  const handleGommage = async (nombre) => {
    if (window.confirm(`¿Seguro que deseas ejecutar el gommage de ${nombre}? 💀`)) {
      await ejecutarGommage(nombre);
      alert(`${nombre} ha recibido el gommage de la pintora.`);
      await cargarHabitantes();
    }
  };

  useEffect(() => {
    cargarHabitantes();
    const interval = setInterval(cargarHabitantes, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex justify-center items-center text-gray-600 text-xl">
        Cargando habitantes...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center p-8">
      <h1 className="text-4xl font-extrabold mb-8 text-indigo-700 drop-shadow-sm">
        Habitantes de Lumiere
      </h1>

      <div className="grid gap-8 sm:gßrid-cols-2 lg:grid-cols-3 w-full max-w-6xl">
        {habitantes.map((h) => (
          <HabitanteCard key={h.nombre} habitante={h} onGommage={handleGommage} />
        ))}
      </div>

      <footer className="mt-12 text-sm text-gray-500">
        © 2025 Panel de Habitantes — Desarrollado con ❤️ y FastAPI + React
      </footer>
    </div>
  );
}

export default App;
