import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/NotFound";
import Home from "@/pages/Home";
import { Route, Switch } from "wouter";

function CaleuchePage() {
  return (
    <main className="min-h-screen bg-slate-950 text-white px-6 py-16">
      <div className="mx-auto max-w-4xl">
        <a href="/" className="text-cyan-300 hover:text-cyan-200">← Volver</a>
        <h1 className="mt-6 text-4xl md:text-6xl font-bold">El Caleuche</h1>
        <p className="mt-6 text-lg text-slate-200">
          En los canales de Chiloé se cuenta que aparece un barco misterioso cubierto de neblina,
          con luces brillantes, música lejana y marineros que jamás envejecen.
        </p>
        <img
          src="https://d2xsxph8kpxj0f.cloudfront.net/310519663575261942/9ruz5LfiTZW2kYyzstUBcW/leyenda-caleuche-FZAnrtPzpHFeucR5TpywXk.webp"
          alt="Ilustración del Caleuche navegando entre niebla y luces"
          className="mt-8 w-full rounded-2xl object-cover"
        />
        <section className="mt-10 space-y-6 text-slate-100 leading-8">
          <p>
            Algunas personas decían que el Caleuche aparecía solo de noche y que avanzaba silencioso
            entre la bruma, como si conociera todos los secretos del mar del sur.
          </p>
          <p>
            Otras historias cuentan que desde lejos se escuchaban risas, cantos y música, como si dentro
            del barco hubiera una fiesta eterna. Pero cuando alguien intentaba acercarse demasiado, el barco
            desaparecía en segundos.
          </p>
          <p>
            Para niños y adolescentes, esta leyenda puede entenderse como una historia sobre el respeto al mar,
            la imaginación y los misterios de Chiloé, donde la naturaleza siempre parece guardar algo oculto.
          </p>
        </section>
      </div>
    </main>
  );
}

function TraucoPage() {
  return (
    <main className="min-h-screen bg-emerald-950 text-white px-6 py-16">
      <div className="mx-auto max-w-4xl">
        <a href="/" className="text-emerald-300 hover:text-emerald-200">← Volver</a>
        <h1 className="mt-6 text-4xl md:text-6xl font-bold">El Trauco</h1>
        <p className="mt-6 text-lg text-emerald-50">
          En los bosques húmedos de Chiloé se habla de un ser pequeño, extraño y muy poderoso, capaz de aparecer
          entre árboles antiguos y senderos cubiertos de musgo.
        </p>
        <img
          src="https://d2xsxph8kpxj0f.cloudfront.net/310519663575261942/9ruz5LfiTZW2kYyzstUBcW/trauco-bosque-H58SXwkVGuRhpPauTXjS3E.webp"
          alt="Ilustración del Trauco en un bosque chilote"
          className="mt-8 w-full rounded-2xl object-cover"
        />
        <section className="mt-10 space-y-6 text-emerald-50 leading-8">
          <p>
            El Trauco forma parte de las leyendas más conocidas del archipiélago y suele describirse como un habitante
            misterioso del bosque, relacionado con lo desconocido y con el respeto por la naturaleza.
          </p>
          <p>
            Muchas familias han contado esta historia durante generaciones para enseñar a los más jóvenes que no todo
            en el bosque es juego: también hay zonas que deben recorrerse con cuidado, atención y respeto.
          </p>
          <p>
            En una versión adaptada para público infantil y juvenil, el Trauco puede presentarse como un guardián inquietante
            del bosque chilote, una figura legendaria que recuerda que la naturaleza tiene reglas propias.
          </p>
        </section>
      </div>
    </main>
  );
}

function App() {
  return (
    <TooltipProvider>
      <Toaster />
      <Switch>
        <Route path="/" component={Home} />
        <Route path="/historias/caleuche" component={CaleuchePage} />
        <Route path="/historias/trauco" component={TraucoPage} />
        <Route component={NotFound} />
      </Switch>
    </TooltipProvider>
  );
}

export default App;