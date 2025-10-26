import React from "react";
import { UserCircleIcon, HeartIcon, XCircleIcon } from "@heroicons/react/24/solid";

export default function VecinosList({ vecinos }) {
  if (!vecinos?.length) {
    return (
      <p className="text-gray-400 text-sm italic">Sin vecinos conocidos</p>
    );
  }

  return (
    <div className="w-full mt-3">
      <h3 className="flex items-center gap-2 text-gray-700 font-semibold mb-1">
        <UserCircleIcon className="w-5 h-5 text-gray-600" />
        Vecinos
      </h3>
      <ul className="text-sm text-gray-600 bg-gray-50 rounded-lg p-2 border border-gray-100">
        {vecinos.map((v) => (
          <li
            key={v.nombre}
            className="flex justify-between items-center border-b last:border-none py-1 px-2"
          >
            <span className="font-medium">{v.nombre}</span>
            {v.vivo ? (
              <HeartIcon className="w-5 h-5 text-green-500" />
            ) : (
              <XCircleIcon className="w-5 h-5 text-gray-500" />
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
