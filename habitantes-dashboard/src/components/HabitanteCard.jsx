import React from "react";
import { HeartIcon, XCircleIcon, Cog8ToothIcon } from "@heroicons/react/24/solid";
import PertenenciasList from "./PertenenciasList";
import VecinosList from "./VecinosList";

export default function HabitanteCard({ habitante, onGommage }) {
  const { nombre, edad, estado, imagen, pertenencias, vecinos } = habitante;
  const vivo = estado === "vivo";

  
  return (
    <div className="relative bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-shadow p-6 flex flex-col items-center border border-gray-100">
      <img
        src={
          imagen
            ? `data:image/jpeg;base64,${imagen}`
            : "https://placehold.co/150x150?text=Sin+Imagen"
        }
        alt={nombre}
        className="w-32 h-32 rounded-full object-cover border-4 border-gray-200 mb-4"
      />

      <h2 className="text-2xl font-semibold text-gray-800">{nombre}</h2>
      <p className="text-gray-500 mb-2">Edad: {edad}</p>

      <div className="flex items-center gap-2 mb-4">
        {vivo ? (
          <>
            <HeartIcon className="w-6 h-6 text-green-500 animate-pulse" />
            <span className="text-green-600 font-semibold">Vivo</span>
          </>
        ) : (
          <>
            <XCircleIcon className="w-6 h-6 text-gray-500" />
            <span className="text-gray-600 font-semibold">Muerto</span>
          </>
        )}
      </div>

      <button
        disabled={!vivo}
        onClick={() => onGommage(nombre)}
        className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all mb-4 ${
          vivo
            ? "bg-red-500 hover:bg-red-600 text-white shadow"
            : "bg-gray-300 text-gray-500 cursor-not-allowed"
        }`}
      >
        <Cog8ToothIcon className="w-5 h-5" />
        Ejecutar Gommage
      </button>

      {/* Secciones adicionales */}
      <div className="w-full space-y-3">
        <PertenenciasList pertenencias={pertenencias} habitante={nombre} />
        <VecinosList vecinos={vecinos} />
      </div>
    </div>
  );
}
