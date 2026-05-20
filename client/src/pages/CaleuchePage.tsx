import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { ArrowLeft, Ship, Sparkles, Waves } from "lucide-react";
import { Link } from "wouter";
import { useEffect } from "react";

const illustrations = [
  {
    src: "https://images.unsplash.com/photo-1500375592092-40eb2168fd21?auto=format&fit=crop&w=1200&q=80",
    alt: "Mar del sur con niebla y olas",
    title: "El mar en la noche",
  },
  {
    src: "https://images.unsplash.com/photo-1518837695005-2083093ee35b?auto=format&fit=crop&w=1200&q=80",
    alt: "Horizonte marítimo con luz dorada entre nubes",
    title: "Luces misteriosas en el horizonte",
  },
  {
    src: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80",
    alt: "Océano profundo con atmósfera fantástica",
    title: "El viaje del Caleuche",
  },
];

export default function CaleuchePage() {
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, []);

  return (
    <main className="min-h-screen bg-background text-foreground">
      <section className="relative overflow-hidden border-b border-border bg-[linear-gradient(180deg,rgba(20,60,90,0.18),rgba(255,255,255,0))]">
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
                Leyenda Chilota
              </p>
              <h1 className="mb-6 text-4xl md:text-6xl">
                El Caleuche: el barco fantasma de Chiloé
              </h1>
              <p className="mb-6 text-lg text-muted-foreground">
                En las islas y canales del sur de Chile se cuenta que, en noches
                de niebla, aparece un barco brillante que avanza sobre el mar
                como si conociera todos los secretos del archipiélago.
              </p>
              <div className="flex flex-wrap gap-3">
                <span className="inline-flex items-center gap-2 rounded-full bg-secondary px-4 py-2 text-sm text-secondary-foreground">
                  <Ship className="h-4 w-4" />
                  Barco fantasma
                </span>
                <span className="inline-flex items-center gap-2 rounded-full bg-secondary px-4 py-2 text-sm text-secondary-foreground">
                  <Waves className="h-4 w-4" />
                  Mar y niebla
                </span>
                <span className="inline-flex items-center gap-2 rounded-full bg-secondary px-4 py-2 text-sm text-secondary-foreground">
                  <Sparkles className="h-4 w-4" />
                  Misterio chilote
                </span>
              </div>
            </div>

            <div className="overflow-hidden rounded-[2rem] border border-border/70 shadow-xl">
              <img
                src="https://d2xsxph8kpxj0f.cloudfront.net/310519663575261942/9ruz5LfiTZW2kYyzstUBcW/leyenda-caleuche-FZAnrtPzpHFeucR5TpywXk.webp"
                alt="Ilustración del Caleuche navegando entre la niebla"
                className="h-full w-full object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      <section className="container mx-auto px-4 py-14">
        <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr]">
          <Card className="rounded-3xl border-border/70 p-8 shadow-sm">
            <h2 className="mb-4 text-3xl">La historia contada para jóvenes</h2>
            <div className="space-y-4 text-muted-foreground">
              <p>
                Hace mucho tiempo, los habitantes de Chiloé comenzaron a hablar
                de una embarcación extraña que aparecía de pronto en medio de la
                oscuridad. No era un barco cualquiera: decían que estaba lleno
                de luces, que desde lejos se escuchaba música y que parecía
                moverse con una rapidez imposible.
              </p>
              <p>
                Algunos pescadores aseguraban haberlo visto pasar entre bancos de
                niebla, casi flotando en silencio antes de desaparecer otra vez
                en el mar. Otros contaban que el Caleuche podía mostrarse solo a
                ciertas personas y esconderse de inmediato si alguien intentaba
                acercarse demasiado.
              </p>
              <p>
                Según la tradición oral, el Caleuche estaba relacionado con seres
                mágicos, marineros encantados y secretos que solo el océano del
                sur conoce. Por eso la leyenda se volvió una forma de explicar
                los sonidos raros de la noche, las luces en el horizonte y el
                respeto profundo que el mar inspira en quienes viven junto a él.
              </p>
              <p>
                En esta versión para niños y adolescentes, lo más importante no
                es el miedo, sino la imaginación: el Caleuche representa ese
                momento en que el paisaje, la niebla y las historias antiguas se
                mezclan para crear algo inolvidable.
              </p>
            </div>
          </Card>

          <Card className="rounded-3xl border-border/70 p-8 shadow-sm">
            <h2 className="mb-4 text-2xl">Dato curioso</h2>
            <p className="mb-4 text-muted-foreground">
              En muchas versiones, el Caleuche aparece de noche, iluminado y
              rodeado de música, como si fuera una fiesta misteriosa en medio
              del mar.
            </p>

            <h3 className="mb-3 mt-6 text-xl">¿Qué enseña esta leyenda?</h3>
            <ul className="space-y-3 text-muted-foreground">
              <li>El mar puede ser hermoso, poderoso y difícil de comprender.</li>
              <li>Las leyendas ayudan a explicar lo desconocido.</li>
              <li>La tradición oral mantiene viva la memoria de un territorio.</li>
            </ul>
          </Card>
        </div>
      </section>

      <section className="container mx-auto px-4 pb-14">
        <div className="mb-8">
          <p className="accent-text mb-3 text-sm uppercase tracking-[0.3em] text-muted-foreground">
            Ilustraciones
          </p>
          <h2 className="text-3xl md:text-4xl">Imágenes para imaginar la leyenda</h2>
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