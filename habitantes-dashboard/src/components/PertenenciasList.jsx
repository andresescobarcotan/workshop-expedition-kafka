import React, { useState } from "react";
import { BriefcaseIcon, PlusCircleIcon } from "@heroicons/react/24/outline";
import axios from "axios";

export default function PertenenciasList({ pertenencias, habitante }) {
  const [nueva, setNueva] = useState("");
  const [lista, setLista] = useState(pertenencias || []);
  const [cargando, setCargando] = useState(false);

  const API_BASES = {
    Lucia: "http://localhost:8000",
    Marco: "http://localhost:8001",
    Ana: "http://localhost:8002",
  };

  const agregarPertenencia = async () => {
    if (!nueva.trim()) return;
    const base = API_BASES[habitante];
    setCargando(true);
    try {
      const res = await axios.put(`${base}/pertenencias`, [nueva.trim()], {
        headers: { "Content-Type": "application/json" },
      });
      setLista(res.data.pertenencias);
      setNueva("");
    } catch (error) {
      console.error("Error al añadir pertenencia:", error);
      alert(`Error al añadir pertenencia a ${habitante}`);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="w-full">
      {/* Título */}
      <h3 className="flex items-center gap-2 text-gray-700 font-semibold mb-2">
        <BriefcaseIcon className="w-5 h-5 text-gray-600" />
        Pertenencias
      </h3>

      {/* Lista */}
      {lista.length === 0 ? (
        <p className="text-gray-400 text-sm italic pl-1 mb-2">
          Sin pertenencias registradas
        </p>
      ) : (
        <ul className="text-sm text-gray-700 bg-gray-50 rounded-lg p-2 border border-gray-100 mb-3">
          {lista.map((p, i) => (
            <li
              key={i}
              className="border-b last:border-none py-1 pl-2 hover:bg-gray-100 transition-colors rounded"
            >
              {p}
            </li>
          ))}
        </ul>
      )}

      {/* Formulario para añadir */}
      <div className="flex items-center gap-2">
        <input
          type="text"
          value={nueva}
          onChange={(e) => setNueva(e.target.value)}
          placeholder="Añadir pertenencia..."
          className="flex-grow px-3 py-1.5 text-sm border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
        <button
          onClick={agregarPertenencia}
          disabled={cargando}
          className={`flex items-center gap-1 px-3 py-1.5 text-sm rounded-lg transition-all ${
            cargando
              ? "bg-gray-300 text-gray-500 cursor-not-allowed"
              : "bg-indigo-600 hover:bg-indigo-700 text-white"
          }`}
        >
          <PlusCircleIcon className="w-5 h-5" />
          {cargando ? "..." : "Añadir"}
        </button>
      </div>
    </div>
  );
}
