import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { ArrowLeft, Trees, Leaf, Eye } from "lucide-react";
import { Link } from "wouter";
import { useEffect } from "react";

const illustrations = [
  {
    src: "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=1200&q=80",
    alt: "Bosque húmedo y frondoso del sur",
    title: "El bosque del sur",
  },
  {
    src: "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80",
    alt: "Sendero misterioso entre árboles",
    title: "Senderos entre árboles antiguos",
  },
  {
    src: "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1200&q=80",
    alt: "Luz entrando entre árboles y helechos",
    title: "Un lugar lleno de secretos",
  },
];

export default function TraucoPage() {
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, []);

  return (
    <main className="min-h-screen bg-background text-foreground">
      <section className="relative overflow-hidden border-b border-border bg-[linear-gradient(180deg,rgba(30,90,50,0.18),rgba(255,255,255,0))]">
        <div className="container mx-auto px-4 py-16 md:py-24">
          <Link href="/">
            <Button variant="outline" className="mb-8 rounded-full">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Volver al inicio
            </Button>
          </Link>

          <div className="grid items-center gap-10 md:grid-cols-2">
            <div>
              <p className="accent-text mb-3 text-sm uppercase tracking-[0.3em] text-muted-foreground">
                Mitología Chilota
              </p>
              <h1 className="mb-6 text-4xl md:text-6xl">
                El Trauco: misterio entre los bosques de Chiloé
              </h1>
              <p className="mb-6 text-lg text-muted-foreground">
                Entre helechos, troncos húmedos y senderos ocultos, la tradición
                chilota cuenta la historia de un ser pequeño y enigmático que
                forma parte de las leyendas más conocidas del sur de Chile.
              </p>
              <div className="flex flex-wrap gap-3">
                <span className="inline-flex items-center gap-2 rounded-full bg-secondary px-4 py-2 text-sm text-secondary-foreground">
                  <Trees className="h-4 w-4" />
                  Bosque chilote
                </span>
                <span className="inline-flex items-center gap-2 rounded-full bg-secondary px-4 py-2 text-sm text-secondary-foreground">
                  <Leaf className="h-4 w-4" />
                  Naturaleza y tradición
                </span>
                <span className="inline-flex items-center gap-2 rounded-full bg-secondary px-4 py-2 text-sm text-secondary-foreground">
                  <Eye className="h-4 w-4" />
                  Personaje misterioso
                </span>
              </div>
            </div>

            <div className="overflow-hidden rounded-[2rem] border border-border/70 shadow-xl">
              <img
                src="https://d2xsxph8kpxj0f.cloudfront.net/310519663575261942/9ruz5LfiTZW2kYyzstUBcW/trauco-bosque-H58SXwkVGuRhpPauTXjS3E.webp"
                alt="Ilustración inspirada en el Trauco dentro del bosque"
                className="h-full w-full object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      <section className="container mx-auto px-4 py-14">
        <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr]">
          <Card className="rounded-3xl border-border/70 p-8 shadow-sm">
            <h2 className="mb-4 text-3xl">La leyenda adaptada para jóvenes</h2>
            <div className="space-y-4 text-muted-foreground">
              <p>
                En Chiloé se cuenta que en los bosques habita el Trauco, un ser
                pequeño pero muy poderoso, ligado al silencio del monte, a los
                árboles antiguos y a los rincones donde casi no llega la luz.
              </p>
              <p>
                Muchas personas lo describían como un personaje extraño, difícil
                de encontrar y aún más difícil de olvidar. Por eso, cuando en el
                bosque ocurría algo inesperado o misterioso, algunos decían que
                el Trauco había pasado cerca.
              </p>
              <p>
                Con el tiempo, esta leyenda se transformó en una manera de
                enseñar respeto por la naturaleza, por los lugares apartados y
                por las historias transmitidas de generación en generación. Más
                que un simple personaje fantástico, el Trauco se convirtió en un
                símbolo del bosque chilote y de su imaginación.
              </p>
              <p>
                En una versión pensada para niños y adolescentes, el Trauco puede
                entenderse como un guardián misterioso del bosque: una figura que
                recuerda que la naturaleza tiene reglas propias y que no todo
                puede explicarse fácilmente.
              </p>
            </div>
          </Card>

          <Card className="rounded-3xl border-border/70 p-8 shadow-sm">
            <h2 className="mb-4 text-2xl">¿Por qué sigue siendo famoso?</h2>
            <p className="mb-4 text-muted-foreground">
              Porque mezcla asombro, temor, naturaleza y tradición oral en una
              sola historia, y eso la vuelve inolvidable.
            </p>

            <h3 className="mb-3 mt-6 text-xl">¿Qué nos enseña?</h3>
            <ul className="space-y-3 text-muted-foreground">
              <li>Los bosques del sur forman parte esencial de la identidad chilota.</li>
              <li>Las leyendas ayudan a cuidar y respetar el entorno natural.</li>
              <li>La imaginación también es una forma de aprender cultura.</li>
            </ul>
          </Card>
        </div>
      </section>

      <section className="container mx-auto px-4 pb-14">
        <div className="mb-8">
          <p className="accent-text mb-3 text-sm uppercase tracking-[0.3em] text-muted-foreground">
            Ilustraciones
          </p>
          <h2 className="text-3xl md:text-4xl">
            Escenarios para acompañar la historia
          </h2>
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          {illustrations.map((item) => (
            <Card
              key={item.title}
              className="overflow-hidden rounded-3xl border-border/70 shadow-sm"
            >
              <img
                src={item.src}
                alt={item.alt}
                className="h-64 w-full object-cover"
                loading="lazy"
              />
              <div className="p-5">
                <h3 className="text-xl">{item.title}</h3>
              </div>
            </Card>
          ))}
        </div>
      </section>
    </main>
  );
}