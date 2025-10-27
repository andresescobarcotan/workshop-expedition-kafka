import axios from "axios";

export const API_BASES = {
  Emma: "http://localhost:8000",
  Marco: "http://localhost:8001",
  Chloe: "http://localhost:8002",
  Pintora: "http://localhost:8003"
};

export async function getHabitanteInfo(nombre) {
  const base = API_BASES[nombre];
  try {
    const [name, edad, salud, imagen, vecinos] = await Promise.all([
      axios.get(`${base}/name`),
      axios.get(`${base}/edad`),
      axios.get(`${base}/salud`),
      axios.get(`${base}/imagen`),
      axios.get(`${base}/vecinos`),
    ]);

    // Consultar info de cada vecino (dirección + estado)
    const vecinosDetallados = await Promise.all(
      vecinos.data.vecinos.map(async (v) => {
        try {
          const info = await axios.get(`${base}/vecinos/${v}`);
          return info.data;
        } catch {
          return { nombre: v, direccion: "desconocida", vivo: false };
        }
      })
    );

    return {
      nombre: name.data.name,
      edad: edad.data.edad,
      estado: salud.data.estado,
      imagen: imagen.data.imagen_base64,
      vecinos: vecinosDetallados,
    };
  } catch (err) {
    console.error(`Error al obtener datos de ${nombre}`, err);
    return {
      nombre,
      edad: "-",
      estado: "desconocido",
      imagen: null,
      pertenencias: [],
      vecinos: [],
    };
  }
}

export async function ejecutarGommage(nombre) {
  const base = API_BASES[nombre];
  return axios.post(`${base}/gommage`);
}
