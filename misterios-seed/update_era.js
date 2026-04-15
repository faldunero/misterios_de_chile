/**
 * update_era.js
 * Agrega el campo "era" a los 80 documentos existentes en Firestore.
 *
 * INSTRUCCIONES:
 * 1. Asegúrate de tener credenciales configuradas
 * 2. Ejecuta desde la carpeta misterios-seed/:
 *      node update_era.js
 */

const admin = require("firebase-admin");

admin.initializeApp({
  credential: admin.credential.applicationDefault(),
  projectId:  "misteriosdechile-7a538",
});

const db = admin.firestore();

const eraData = {
  "01": "Conquista",
  "02": "Conquista",
  "03": "Conquista",
  "04": "Conquista",
  "05": "Conquista",
  "06": "Conquista",
  "07": "Conquista",
  "08": "La Colonia",
  "09": "La Colonia",
  "10": "La Colonia",
  "11": "La Colonia",
  "12": "La Colonia",
  "13": "La Colonia",
  "14": "La Colonia",
  "15": "La Colonia",
  "16": "Independencia",
  "17": "Independencia",
  "18": "Independencia",
  "19": "Independencia",
  "20": "Independencia",
  "21": "Independencia",
  "22": "Independencia",
  "23": "Reconquista",
  "24": "Reconquista",
  "25": "Independencia",
  "26": "Independencia",
  "27": "Independencia",
  "28": "Independencia",
  "29": "Independencia",
  "30": "Independencia",
  "31": "Organización",
  "32": "Organización",
  "33": "Organización",
  "34": "Organización",
  "35": "Organización",
  "36": "Rep. Conservadora",
  "37": "Rep. Conservadora",
  "38": "Rep. Conservadora",
  "39": "Rep. Conservadora",
  "40": "Rep. Conservadora",
  "41": "Rep. Conservadora",
  "42": "Rep. Conservadora",
  "43": "Rep. Conservadora",
  "44": "Rep. Conservadora",
  "45": "Rep. Conservadora",
  "46": "Rep. Conservadora",
  "47": "Rep. Conservadora",
  "48": "Rep. Conservadora",
  "49": "Rep. Conservadora",
  "50": "Rep. Conservadora",
  "51": "Rep. Liberal",
  "52": "Rep. Liberal",
  "53": "Rep. Liberal",
  "54": "Rep. Liberal",
  "55": "Rep. Liberal",
  "56": "Rep. Liberal",
  "57": "Rep. Liberal",
  "58": "Rep. Liberal",
  "59": "Rep. Liberal",
  "60": "Rep. Liberal",
  "61": "Rep. Liberal",
  "62": "Rep. Liberal",
  "63": "Rep. Liberal",
  "64": "Rep. Liberal",
  "65": "Rep. Liberal",
  "66": "Rep. Liberal",
  "67": "Rep. Liberal",
  "68": "Rep. Liberal",
  "69": "Rep. Liberal",
  "70": "Parlamentarismo",
  "71": "Parlamentarismo",
  "72": "Parlamentarismo",
  "73": "Parlamentarismo",
  "74": "Parlamentarismo",
  "75": "Parlamentarismo",
  "76": "Rep. Liberal",
  "77": "Rep. Liberal",
  "78": "Organización",
  "79": "Organización",
  "80": "Organización",
};

async function update() {
  const colRef = db.collection("cartas");
  const batch  = db.batch();
  let count = 0;

  for (const [id, era] of Object.entries(eraData)) {
    const docRef = colRef.doc(`carta_${id}`);
    batch.update(docRef, { era });
    count++;
  }

  await batch.commit();
  console.log(`✅ Era actualizada en ${count} cartas.`);
  process.exit(0);
}

update().catch(err => {
  console.error("❌ Error:", err);
  process.exit(1);
});
