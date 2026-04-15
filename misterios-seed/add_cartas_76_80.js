/**
 * add_cartas_76_80.js
 * Agrega las cartas 76–80 a la colección "cartas" en Firestore.
 *
 * INSTRUCCIONES:
 * 1. Asegúrate de tener las credenciales configuradas:
 *      export GOOGLE_APPLICATION_CREDENTIALS="ruta/a/serviceAccountKey.json"
 *    O bien, estar autenticado con: gcloud auth application-default login
 * 2. Ejecuta desde la carpeta misterios-seed/:
 *      node add_cartas_76_80.js
 */

const admin = require("firebase-admin");

admin.initializeApp({
  credential: admin.credential.applicationDefault(),
  projectId:  "misteriosdechile-7a538",
});

const db = admin.firestore();

// ── DATOS 76–80 ──────────────────────────────────────────────────────────────

const cartas = {
  "76": {
    nombre_archivo: "id_76_combate_naval_de_iquique",
    evento:         "Combate Naval de Iquique",
    anio:           "1879",
    personajes:     "Arturo Prat, Miguel Grau",
    pistas: [
      "Dos naves se enfrentaron en aguas del norte. La más pequeña resistió hasta el último cañonazo antes de hundirse.",
      "Ocurrió durante una guerra en que Chile enfrentó a sus vecinos del norte por el control de un mineral muy valioso.",
      "El comandante de la nave menor no abandonó su puesto ni su bandera, aunque sabía que no podía ganar.",
    ],
    tiene_imagen: true,
    tiene_audio:  true,
  },
  "77": {
    nombre_archivo: "id_77_cuestion_social",
    evento:         "Cuestión Social",
    anio:           "1880",
    personajes:     "Luis Emilio Recabarren",
    pistas: [
      "Miles de familias vivían hacinadas sin agua limpia ni atención médica, mientras el país producía una riqueza enorme.",
      "Sucedió cuando el norte de Chile era el centro económico del país, entre fines del siglo XIX y comienzos del XX.",
      "Fueron hombres y mujeres trabajadores que se unieron, marcharon y pararon sus labores para exigir un trato justo.",
    ],
    tiene_imagen: true,
    tiene_audio:  true,
  },
  "78": {
    nombre_archivo: "id_78_constitucion_moralista_1823",
    evento:         "Constitución Moralista 1823",
    anio:           "1823",
    personajes:     "Juan Egaña",
    pistas: [
      "Se redactó un documento tan exigente que quería regular hasta las costumbres privadas de las personas. Nadie pudo cumplirlo.",
      "Fue en los primeros años del país como nación independiente, cuando aún se buscaba cómo organizarse.",
      "Lo redactó un político y jurista que soñaba con una república perfecta, ordenada hasta en sus más mínimos detalles.",
    ],
    tiene_imagen: true,
    tiene_audio:  true,
  },
  "79": {
    nombre_archivo: "id_79_constitucion_liberal_1828",
    evento:         "Constitución Liberal 1828",
    anio:           "1828",
    personajes:     "Francisco Antonio Pinto, Melchor de Santiago Concha",
    pistas: [
      "Un documento buscó repartir el poder entre distintas autoridades, proteger los derechos de las personas y crear un cargo para gobernar el país.",
      "Nació en una época de ideas nuevas y libertades, cuando muchos países de América recién estrenaban su independencia.",
      "Fue impulsado por pensadores que creían en la libertad, la igualdad y que el Congreso debía tener más poder que el gobernante.",
    ],
    tiene_imagen: true,
    tiene_audio:  true,
  },
  "80": {
    nombre_archivo: "id_80_constitucion_de_1833",
    evento:         "Constitución de 1833",
    anio:           "1833",
    personajes:     "Diego Portales, Mariano Egaña, Manuel José Gandarillas",
    pistas: [
      "Tras años de desorden, se creó un documento que puso al mando a un gobernante muy poderoso y que solo algunos podían votar.",
      "Se dictó poco después de que un bando derrotara a otro en una guerra civil, imponiendo su visión de cómo debía ser el país.",
      "Detrás de él estaba un ministro muy influyente que creía en el orden, la autoridad fuerte y el rol de la Iglesia en el Estado.",
    ],
    tiene_imagen: true,
    tiene_audio:  true,
  },
};

// ── SEED ─────────────────────────────────────────────────────────────────────

async function seed() {
  const colRef = db.collection("cartas");
  const batch  = db.batch();
  let count = 0;

  for (const [id, data] of Object.entries(cartas)) {
    const docRef = colRef.doc(`carta_${id}`);
    batch.set(docRef, { id, ...data });
    count++;
    console.log(`  📝  carta_${id} → ${data.evento}`);
  }

  await batch.commit();
  console.log(`\n✅ ${count} cartas escritas en Firestore (colección: cartas)`);
  process.exit(0);
}

seed().catch((err) => {
  console.error("❌ Error:", err);
  process.exit(1);
});
