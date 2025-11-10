"""Aventura interactiva por línea de comandos ambientada en Ámsterdam.

Ejecuta este script con Python 3:

    python aventura.py
"""
from __future__ import annotations

from dataclasses import dataclass, field
import sys
from textwrap import dedent


@dataclass
class GameState:
    """Estado global de la aventura."""

    energia: int = 6
    confianza: int = 0
    recuerdos: list[str] = field(default_factory=list)
    inventario: set[str] = field(default_factory=set)
    contactos: set[str] = field(default_factory=set)
    visitados: set[str] = field(default_factory=set)


def narrar(texto: str) -> None:
    """Imprime texto normalizado, sin espacios extra."""

    print(dedent(texto).strip())


def pedir_eleccion(pregunta: str, opciones: dict[str, str]) -> str:
    """Solicita una opción válida y devuelve la clave elegida."""

    while True:
        narrar(pregunta)
        for clave, descripcion in opciones.items():
            print(f"  [{clave}] {descripcion}")
        respuesta = input("> ").strip().lower()
        if respuesta in opciones:
            return respuesta
        print("\nNo entendí la respuesta. Elige una de las opciones disponibles.\n")


def registrar_recuerdo(estado: GameState, descripcion: str) -> None:
    """Guarda un recuerdo único en el cuaderno del viaje."""

    estado.recuerdos.append(descripcion)


def mostrar_estado(estado: GameState) -> None:
    """Muestra un resumen del estado actual de la persona viajera."""

    narrar(
        f"\nEnergía disponible: {estado.energia}/6\n"
        f"Confianza ganada en la ciudad: {estado.confianza}\n"
        f"Recuerdos anotados: {len(estado.recuerdos)}\n"
        f"Objetos e invitaciones guardados: {', '.join(sorted(estado.inventario)) or 'ninguno'}\n"
        f"Contactos hechos: {', '.join(sorted(estado.contactos)) or 'ninguno'}\n"
    )


def recorrer_jordaan(estado: GameState) -> None:
    narrar(
        """
        Tomas una bicicleta prestada y entras en el Jordaan al atardecer. Los canales reflejan
        las fachadas inclinadas y una brisa con olor a tostadas de centeno se cuela entre las
        casas. Un historiador fluvial y una fotógrafa urbana discuten sobre qué define el
        carácter de Ámsterdam y te invitan a tomar partido.
        """
    )

    eleccion = pedir_eleccion(
        "¿Con quién quieres recorrer el vecindario?",
        {
            "h": "Acompañar al historiador en un bote privado",
            "f": "Seguir a la fotógrafa y sus encuadres nocturnos",
        },
    )

    if eleccion == "h":
        narrar(
            """
            Abordas el bote y avanzas por un canal secundario donde casi no hay turistas.
            El historiador comparte mapas dibujados a mano y la historia de los gremios que
            financiaron los puentes. Propone que diseñes tu propia ruta de agua.
            """
        )
        registrar_recuerdo(
            estado,
            "Diseñaste una ruta de canales inspirada en los gremios artesanales del Jordaan.",
        )
        estado.confianza += 1
        invitacion = pedir_eleccion(
            "Te ofrece una llave de los archivos municipales para consultar planos originales. ¿La aceptas?",
            {"s": "Sí, guardo la llave en mi chaqueta", "n": "No, prefiero dejar el acceso reservado"},
        )
        if invitacion == "s":
            estado.inventario.add("llave de archivos históricos")
            narrar(
                """
                La llave pesa en el bolsillo con promesa de madrugadas entre planos y tinta
                azul. El historiador te anota su número para acompañarte si decides usarla.
                """
            )
            estado.contactos.add("historiador de canales")
        else:
            narrar(
                """
                Agradeces la confianza, pero decides vivir la ciudad sin credenciales
                adicionales. El bote regresa a la orilla con una serenidad casi privada.
                """
            )
    else:
        narrar(
            """
            Caminas tras la fotógrafa mientras captura reflejos fugaces en escaparates y
            ventanas altas. Te pide que elijas entre retratar a las personas o la arquitectura.
            """
        )
        subeleccion = pedir_eleccion(
            "¿Qué enfoque te interesa más?",
            {
                "p": "Retratar a quienes conversan en los escalones", 
                "a": "Buscar simetrías en los frontones y faroles",
            },
        )
        if subeleccion == "p":
            narrar(
                """
                Ella te enseña a pedir permiso con una sonrisa franca. Las historias se abren
                solas y acabas improvisando una entrevista sobre los oficios creativos de la zona.
                """
            )
            estado.contactos.add("artesanos del Jordaan")
            registrar_recuerdo(
                estado,
                "Entrevistaste a artesanos que transforman antiguas casas flotantes en estudios creativos.",
            )
        else:
            narrar(
                """
                Ajustas la cámara hacia las cornisas ornamentadas. Descubres patrones que
                parecen partituras. Ella imprime dos copias en un laboratorio cercano: una es
                para ti y otra para su exposición.
                """
            )
            estado.inventario.add("fotografía nocturna del Jordaan")
            registrar_recuerdo(
                estado,
                "Capturaste una fotografía nocturna con geometrías que recuerdan partituras barrocas.",
            )
        estado.confianza += 1

    estado.visitados.add("jordaan")


def visitar_noordermarkt(estado: GameState) -> None:
    narrar(
        """
        Amanece y el Noordermarkt vibra con puestos de flores, quesos añejos y diseñadores
        que conversan sobre sostenibilidad. La curadora del mercado te ofrece dos itinerarios
        complementarios para que experimentes la ciudad a través del paladar.
        """
    )

    eleccion = pedir_eleccion(
        "¿Qué itinerario te seduce?",
        {
            "g": "Cata guiada de quesos acompañada de historias familiares",
            "c": "Laboratorio de tostado con una microtostadora de café innovadora",
        },
    )

    if eleccion == "g":
        narrar(
            """
            Descubres variedades con cristales salinos y otras bañadas en cerveza artesanal.
            La maestra quesera te comparte cómo negocian con granjeros que priorizan el bienestar animal.
            """
        )
        estado.inventario.add("queso añejo envuelto en papel de cera")
        registrar_recuerdo(
            estado,
            "Conversaste sobre comercio justo mientras degustabas quesos experimentales del Noordermarkt.",
        )
        estado.confianza += 1
    else:
        narrar(
            """
            Aprendes a identificar aromas a nuez, cacao y naranja sanguina. La microtostadora
            te invita a calibrar la máquina y a escribir notas de cata para su catálogo semanal.
            """
        )
        estado.inventario.add("tarjeta de cata firmada")
        registrar_recuerdo(
            estado,
            "Participaste en un laboratorio de tostado que mezclaba ciencia sensorial y conversaciones íntimas.",
        )
        estado.contactos.add("microtostadora experimental")

    estado.visitados.add("noordermarkt")


def noche_en_rijksmuseum(estado: GameState) -> None:
    narrar(
        """
        El Rijksmuseum abre de forma excepcional después del horario habitual. Un reducido
        grupo recorre salas casi vacías iluminadas por lámparas cálidas. La comisaria a cargo
        propone dos experiencias simultáneas.
        """
    )

    opciones = {
        "r": "Charla íntima sobre claroscuro con una restauradora",
        "i": "Instalación inmersiva con proyecciones de cartas históricas",
    }
    if "llave de archivos históricos" in estado.inventario:
        opciones["a"] = "Visitar el archivo subterráneo utilizando tu credencial recién conseguida"

    eleccion = pedir_eleccion("¿Cómo quieres aprovechar la noche?", opciones)

    if eleccion == "r":
        narrar(
            """
            La restauradora desmonta el misterio de la luz en los lienzos de Rembrandt.
            Te enseña a observar las capas de barniz y comparte confidencias sobre
            presupuestos, políticas culturales y cómo conseguir apoyo sin perder independencia.
            """
        )
        registrar_recuerdo(
            estado,
            "Analizaste el claroscuro de Rembrandt desde la mirada pragmática de una restauradora.",
        )
        estado.confianza += 1
    elif eleccion == "i":
        narrar(
            """
            Entras en una sala circular donde cartas del Siglo de Oro se proyectan en las paredes.
            Al leerlas en voz alta, activas sonidos de astilleros y mercados globales.
            """
        )
        registrar_recuerdo(
            estado,
            "Activaste una instalación sonora que entrelazaba cartas mercantiles con paisajes de ultramar.",
        )
        if "fotografía nocturna del Jordaan" in estado.inventario:
            narrar(
                """
                La comisaria se fija en tu fotografía y propone incluirla en un ciclo
                contemporáneo. Te entrega su tarjeta personal.
                """
            )
            estado.contactos.add("comisaria del Rijksmuseum")
    else:
        narrar(
            """
            Desciendes por un corredor estrecho hacia los archivos. La llave abre una
            compuerta discreta. Descubres registros de barcos y cartas de navegación
            escritos con tinta ferrosa. Fotografías un plano que inspira futuros proyectos.
            """
        )
        estado.inventario.add("plano naval de 1667")
        registrar_recuerdo(
            estado,
            "Exploraste los archivos subterráneos del Rijksmuseum y obtuviste un plano naval de 1667.",
        )
        estado.confianza += 2

    estado.visitados.add("rijksmuseum")


def speakeasy_de_pijp(estado: GameState) -> None:
    narrar(
        """
        Una puerta discreta en De Pijp conduce a un speakeasy inspirado en talleres de cerámica.
        El bartender diseña tragos a partir de historias personales y una emprendedora local
        busca socios para un laboratorio de diseño circular.
        """
    )

    eleccion = pedir_eleccion(
        "¿Cómo decides pasar la noche?",
        {
            "t": "Compartir un recuerdo para recibir un cóctel creado a tu medida",
            "n": "Unirte a la conversación sobre negocios creativos",
        },
    )

    if eleccion == "t":
        narrar(
            """
            Narras un episodio de viajes y vulnerabilidad. El bartender mezcla ginebra local,
            cordial de ruibarbo y bitters de cacao. Te regala la receta y anota tu reacción
            para su archivo de emociones.
            """
        )
        estado.inventario.add("receta de cóctel personalizado")
        registrar_recuerdo(
            estado,
            "Probaste un cóctel diseñado a partir de una confidencia sobre reinicios profesionales.",
        )
    else:
        narrar(
            """
            Participas en un debate sobre cómo reutilizar materiales de demolición.
            Surgen ideas para residencias artísticas en barcazas desmanteladas. Te invitan a
            moderar una mesa redonda la próxima semana.
            """
        )
        estado.contactos.add("colectivo de diseño circular")
        registrar_recuerdo(
            estado,
            "Acordaste colaborar con un colectivo que transforma barcazas en residencias artísticas.",
        )
        estado.confianza += 1

    estado.visitados.add("speakeasy")


def festival_de_luces(estado: GameState) -> None:
    narrar(
        """
        Cruzas hacia los muelles orientales donde se celebra un festival de luz y narrativa.
        Instalaciones brillan sobre el agua mientras una cronista invita a quienes han
        tejido vínculos durante el día a compartir lo que la ciudad les susurró.
        """
    )

    narrar(
        """
        La cronista escucha tus hallazgos y te ofrece elegir cómo cerrar tu travesía nocturna.
        Puedes proyectar tus recuerdos sobre una vela flotante o escribir un compromiso para
        tu vida cotidiana al volver a casa.
        """
    )

    eleccion = pedir_eleccion(
        "¿Qué gesto final eliges?",
        {
            "v": "Encender una vela con tus recuerdos registrados",
            "c": "Escribir un compromiso inspirado en la ciudad",
        },
    )

    if eleccion == "v":
        narrar(
            """
            Tus notas se transforman en reflejos dorados que navegan lentamente.
            El público guarda silencio y alguien te pide permiso para citarte en un podcast cultural.
            """
        )
        estado.contactos.add("cronista del festival")
    else:
        narrar(
            """
            Redactas un compromiso para cultivar redes de cuidado urbano. Sellas el mensaje
            dentro de una ampolla de cristal que quedará suspendida sobre el muelle.
            """
        )
        registrar_recuerdo(
            estado,
            "Sellaste un compromiso para replicar en tu ciudad la colaboración vista en Ámsterdam.",
        )
        estado.confianza += 1

    estado.visitados.add("festival")


def opciones_disponibles(estado: GameState) -> dict[str, str]:
    opciones: dict[str, str] = {}
    if "jordaan" not in estado.visitados:
        opciones["j"] = "Recorrer el Jordaan al atardecer"
    if "noordermarkt" not in estado.visitados:
        opciones["n"] = "Sumergirte en el Noordermarkt matutino"
    if "rijksmuseum" not in estado.visitados:
        opciones["r"] = "Vivir una noche excepcional en el Rijksmuseum"
    if "speakeasy" not in estado.visitados:
        opciones["p"] = "Buscar un speakeasy creativo en De Pijp"

    requisitos_festival = estado.confianza >= 2 or len(estado.inventario) >= 3 or len(estado.recuerdos) >= 4
    if requisitos_festival and "festival" not in estado.visitados:
        opciones["f"] = "Culminar en el festival de luces de los muelles orientales"

    opciones["i"] = "Revisar tu cuaderno y estado actual"
    opciones["s"] = "Dar por concluida la travesía"
    return opciones


def finalizar_aventura(estado: GameState) -> None:
    narrar(
        """
        Con la noche bien entrada, cruzas un último puente iluminado. Las notas, sabores y
        conversaciones del día laten en tu cuaderno. Respiras hondo el aire húmedo y decides
        qué fragmentos llevarás de regreso a tu vida cotidiana.
        """
    )

    if estado.recuerdos:
        narrar("Recuerdos destacados:")
        for recuerdo in estado.recuerdos:
            print(f"  • {recuerdo}")
    if estado.inventario:
        narrar("\nObjetos e invitaciones que guardas:")
        for objeto in sorted(estado.inventario):
            print(f"  • {objeto}")
    if estado.contactos:
        narrar("\nContactos con quienes podrías reencontrarte:")
        for contacto in sorted(estado.contactos):
            print(f"  • {contacto}")

    narrar(
        """
        Cuando el tranvía nocturno llega, sabes que Ámsterdam queda inscrita en tu forma de
        mirar ciudades y te prometes volver con más tiempo para explorar cada historia emergente.
        """
    )


def main() -> None:
    estado = GameState()
    narrar(
        """
        Llegas a Ámsterdam con la agenda libre y una invitación abierta a dejarte sorprender.
        La ciudad combina elegancia histórica con innovación cotidiana. Te propones explorar
        durante unas horas, equilibrando la curiosidad profesional con el placer de estar de viaje.
        Cada decisión que tomes dejará huellas en tu cuaderno.
        """
    )

    while estado.energia > 0:
        print()
        opciones = opciones_disponibles(estado)
        eleccion = pedir_eleccion("¿Cuál será tu próximo paso?", opciones)

        if eleccion == "s":
            break
        if eleccion == "i":
            mostrar_estado(estado)
            continue

        if eleccion == "j":
            recorrer_jordaan(estado)
        elif eleccion == "n":
            visitar_noordermarkt(estado)
        elif eleccion == "r":
            noche_en_rijksmuseum(estado)
        elif eleccion == "p":
            speakeasy_de_pijp(estado)
        elif eleccion == "f":
            festival_de_luces(estado)
        else:
            print("Opción no reconocida. Intenta de nuevo.")
            continue

        estado.energia -= 1
        if estado.energia == 0:
            narrar(
                """
                El cansancio se instala con suavidad. Reconoces que es momento de cerrar la noche
                antes de que el amanecer te sorprenda sin fuerzas.
                """
            )
            break

        continuar = pedir_eleccion(
            "¿Quieres seguir explorando?",
            {"s": "Sí, aún me queda energía", "n": "No, prefiero retirarme"},
        )
        if continuar == "n":
            break

    finalizar_aventura(estado)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nHas cerrado la aventura. ¡Hasta pronto!")
