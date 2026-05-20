const stories = [
  {
    id: "conquista",
    title: "La Conquista Española",
    period: "Siglo XVI",
    region: "Todo Chile",
    description: "El encuentro entre conquistadores españoles y pueblos originarios mapuches.",
    image:
      "https://d2xsxph8kpxj0f.cloudfront.net/310519663575261942/9ruz5LfiTZW2kYyzstUBcW/hero-conquista-T7DU3VeFHqKSWYpcy4oyaV.webp",
    href: "#",
  },
  {
    id: "caleuche",
    title: "El Caleuche: Barco Fantasma",
    period: "Leyenda Chilota",
    region: "Chiloé",
    description: "Un barco fantasma que navega los mares del sur entre niebla, luces y misterio.",
    image:
      "https://d2xsxph8kpxj0f.cloudfront.net/310519663575261942/9ruz5LfiTZW2kYyzstUBcW/leyenda-caleuche-FZAnrtPzpHFeucR5TpywXk.webp",
    href: "/historias/caleuche",
  },
  {
    id: "trauco",
    title: "El Trauco: Duende del Bosque",
    period: "Mitología Chilota",
    region: "Chiloé",
    description: "Una criatura legendaria del bosque, rodeada de secretos y relatos ancestrales.",
    image:
      "https://d2xsxph8kpxj0f.cloudfront.net/310519663575261942/9ruz5LfiTZW2kYyzstUBcW/trauco-bosque-H58SXwkVGuRhpPauTXjS3E.webp",
    href: "/historias/trauco",
  },
];

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <section className="px-6 py-20 md:py-28">
        <div className="mx-auto max-w-6xl">
          <p className="text-cyan-300 uppercase tracking-[0.2em] text-sm">Bienvenido a un viaje histórico</p>
          <h1 className="mt-4 text-5xl md:text-7xl font-bold leading-tight">
            Historias y Misterios de Chile
          </h1>
          <p className="mt-6 max-w-3xl text-lg text-slate-300">
            Descubre leyendas, mitos y relatos del imaginario chileno en una experiencia pensada para explorar,
            aprender y asombrarse.
          </p>
        </div>
      </section>

      <section className="px-6 pb-20">
        <div className="mx-auto grid max-w-6xl gap-8 md:grid-cols-2 xl:grid-cols-3">
          {stories.map((story) => (
            <article
              key={story.id}
              className="overflow-hidden rounded-3xl border border-white/10 bg-white/5 backdrop-blur"
            >
              <img
                src={story.image}
                alt={story.title}
                className="h-64 w-full object-cover"
              />
              <div className="p-6">
                <div className="flex gap-2 text-xs uppercase tracking-[0.16em] text-slate-400">
                  <span>{story.period}</span>
                  <span>•</span>
                  <span>{story.region}</span>
                </div>
                <h2 className="mt-3 text-2xl font-semibold">{story.title}</h2>
                <p className="mt-3 text-slate-300">{story.description}</p>

                {story.href === "#" ? (
                  <button
                    className="mt-6 rounded-full border border-white/20 px-5 py-3 text-sm font-medium text-slate-300 opacity-60 cursor-not-allowed"
                    disabled
                  >
                    Próximamente
                  </button>
                ) : (
                  <a
                    href={story.href}
                    className="mt-6 inline-flex rounded-full bg-cyan-400 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300"
                  >
                    Leer más
                  </a>
                )}
              </div>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}