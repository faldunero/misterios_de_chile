/**
 * upload_storage_76_80.js
 * Sube las imágenes y audios de las cartas 76–80 a Firebase Storage.
 *
 * INSTRUCCIONES:
 * 1. Asegúrate de tener las credenciales configuradas:
 *      export GOOGLE_APPLICATION_CREDENTIALS="ruta/a/serviceAccountKey.json"
 *    O bien, estar autenticado con: gcloud auth application-default login
 * 2. Ejecuta desde la carpeta misterios-seed/:
 *      node upload_storage_76_80.js
 */

const admin = require("firebase-admin");
const path  = require("path");

admin.initializeApp({
  credential:    admin.credential.applicationDefault(),
  projectId:     "misteriosdechile-7a538",
  storageBucket: "misteriosdechile-7a538.firebasestorage.app",
});

const bucket  = admin.storage().bucket();
const baseDir = path.resolve(__dirname, "..");

const archivos = [
  // ── Imágenes ──────────────────────────────────────────────────────────────
  { local: "imagenes/id_76_combate_naval_de_iquique.png",   dest: "imagenes/id_76_combate_naval_de_iquique.png",   type: "image/png"  },
  { local: "imagenes/id_77_cuestion_social.png",            dest: "imagenes/id_77_cuestion_social.png",            type: "image/png"  },
  { local: "imagenes/id_78_constitucion_moralista_1823.png",dest: "imagenes/id_78_constitucion_moralista_1823.png",type: "image/png"  },
  { local: "imagenes/id_79_constitucion_liberal_1828.png",  dest: "imagenes/id_79_constitucion_liberal_1828.png",  type: "image/png"  },
  { local: "imagenes/id_80_constitucion_de_1833.png",       dest: "imagenes/id_80_constitucion_de_1833.png",       type: "image/png"  },
  // ── Audios ────────────────────────────────────────────────────────────────
  { local: "audios/id_76_combate_naval_de_iquique.mp4",     dest: "audios/id_76_combate_naval_de_iquique.mp4",     type: "video/mp4"  },
  { local: "audios/id_77_cuestion_social.mp4",              dest: "audios/id_77_cuestion_social.mp4",              type: "video/mp4"  },
  { local: "audios/id_78_constitucion_moralista_1823.mp4",  dest: "audios/id_78_constitucion_moralista_1823.mp4",  type: "video/mp4"  },
  { local: "audios/id_79_constitucion_liberal_1828.mp4",    dest: "audios/id_79_constitucion_liberal_1828.mp4",    type: "video/mp4"  },
  { local: "audios/id_80_constitucion_de_1833.mp4",         dest: "audios/id_80_constitucion_de_1833.mp4",         type: "video/mp4"  },
];

async function upload() {
  console.log(`📦 Subiendo ${archivos.length} archivos a Firebase Storage…\n`);
  let ok = 0;

  for (const { local, dest, type } of archivos) {
    const localPath = path.join(baseDir, local);
    try {
      await bucket.upload(localPath, {
        destination: dest,
        metadata: {
          contentType: type,
          cacheControl: "public, max-age=31536000",
        },
      });
      console.log(`  ✅  ${dest}`);
      ok++;
    } catch (err) {
      console.error(`  ❌  ${dest} → ${err.message}`);
    }
  }

  console.log(`\n🏁 Listo: ${ok}/${archivos.length} archivos subidos.`);
  process.exit(0);
}

upload().catch((err) => {
  console.error("Error fatal:", err);
  process.exit(1);
});
