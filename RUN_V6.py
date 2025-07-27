# 📦 Imports
import chainlit as cl
from openai import OpenAI
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import json
# ESTE ES EL CÓDIGO SEGURO QUE DEBES USAR:
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ================================
# 📋 Datos básicos requeridos
# ================================
datos_basicos_requeridos = [
    "conyuge_1_nombre", "conyuge_1_cedula", "conyuge_1_ciudad_cedula", "conyuge_1_ciudad_domicilio",
    "conyuge_2_nombre", "conyuge_2_cedula", "conyuge_2_ciudad_cedula", "conyuge_2_ciudad_domicilio",
    "autoridad_matrimonio", "ciudad_matrimonio", "departamento_matrimonio",
    "registro_civil_numero", "notaria_registro_union"
]

# ================================
# ⚙️ Bloques configurados
# ================================
bloques_configurados = [
    {
        "nombre": "hijos",
        "section_name": "Hijos",
        "opcional": True,
        "introduccion": (
            "Abordemos ahora uno de los temas más importantes: el bienestar de sus hijos. "
            "En esta sección definiremos los acuerdos sobre su cuidado diario, el régimen de visitas y el soporte económico. "
            "Recuerden que la ley siempre busca proteger el interés superior de los menores, por lo que la claridad y la equidad en estos puntos son fundamentales."
        ),
        "clausulas_dict": {
            "custodia": {
                "pregunta": "¿Quién tendrá la custodia y cuidado personal de los hijos?",
                "ayuda": "Aquí se define con cuál de los dos padres vivirán los hijos de forma habitual. Normalmente, la custodia la tiene uno de los padres, estableciendo su hogar como la residencia principal de los menores.",
                "ejemplo": "Ejemplo: La custodia y cuidado personal de nuestro hijo menor, [Nombre del hijo], quedará en cabeza exclusiva de la madre, [Nombre del Cónyuge 1]."
            },
            "visitas": {
                "pregunta": "¿Cómo será el régimen de visitas para el padre que no tiene la custodia?",
                "ayuda": "Detallen los días y horarios en que el otro padre podrá compartir con sus hijos. Es recomendable ser específico para evitar malentendidos (fines de semana, vacaciones, cumpleaños, etc.).",
                "ejemplo": "Ejemplo: El padre, [Nombre del Cónyuge 2], podrá compartir con su hijo los fines de semana cada quince días, recogiéndolo el viernes en la tarde y reintegrándolo al hogar materno el domingo en la noche. Las vacaciones de mitad y fin de año se distribuirán por partes iguales."
            },
            "cuota_alimentaria": {
                "pregunta": "¿Cuál será el valor de la cuota alimentaria y cómo se gestionará?",
                "ayuda": "Fijen una suma mensual que el padre no custodio aportará para los gastos de los hijos (educación, salud, vestuario, recreación). Indiquen el monto, la fecha de pago y el método (consignación, efectivo, etc.).",
                "ejemplo": "Ejemplo: A título de cuota alimentaria, el padre se compromete a suministrar la suma de SETECIENTOS MIL PESOS ($700.000) mensuales, pagaderos dentro de los primeros cinco (5) días de cada mes mediante consignación a la cuenta de ahorros de la madre. Este valor se reajustará anualmente según el IPC."
            }
        }
    },
    {
        "nombre": "bienes",
        "section_name": "Bienes y Deudas",
        "opcional": True,
        "introduccion": (
            "Ahora organizaremos el aspecto patrimonial. Durante el matrimonio, ustedes formaron una 'sociedad conyugal', que es como una pequeña empresa con activos (bienes) y pasivos (deudas). "
            "El paso a seguir es liquidarla, es decir, repartir todo lo que se adquirió en este tiempo. La identificación de cada bien debe ser PERFECTA para su validez en notaría y en las oficinas de registro. Seamos muy detallados."
        ),
        "clausulas_dict": {
            "inmuebles": {
                "pregunta": "Describe los bienes inmuebles a repartir (casas, apartamentos, lotes, fincas).",
                "ayuda": (
                    "Para que un bien inmueble quede plenamente identificado y no haya dudas en la notaría ni en la Oficina de Registro, es **indispensable** que proporciones: \n"
                    "1. La **dirección completa** (incluyendo ciudad y departamento).\n"
                    "2. El **Número de Matrícula Inmobiliaria (NMI)**, que es como la 'cédula' de la propiedad.\n"
                    "3. La **cédula o referencia catastral**."
                ),
                "ejemplo": "Ejemplo: El apartamento 501 del Edificio 'El Roble', ubicado en la Calle 100 # 19-20 en Bogotá D.C., con Matrícula Inmobiliaria No. 50C-1234567 y Referencia Catastral No. 001122334455, será adjudicado en su totalidad a la cónyuge [Nombre del Cónyuge 1]."
            },
            "muebles": {
                "pregunta": "Describe los bienes muebles de valor a repartir (vehículos, motocicletas).",
                "ayuda": (
                    "Para vehículos, la identificación completa requiere: **placa, marca, línea, modelo, color y número de motor y/o chasis**. Para otros bienes de alto valor (maquinaria, etc.), proporciona marcas, modelos y números de serie que los hagan inconfundibles."
                ),
                "ejemplo": "Ejemplo: El vehículo de placas FBC-789, marca Renault, línea Duster, modelo 2021, color gris, con número de motor R123456789, quedará en propiedad exclusiva del cónyuge [Nombre del Cónyuge 2]."
            },
            "bienes_especiales": {
                "pregunta": "¿Existen otros activos como acciones, CDTs, derechos fiduciarios, ganado, caballos u otros títulos valores a repartir?",
                "ayuda": (
                    "Aquí se listan activos no tradicionales. La clave es identificarlos sin ambigüedad. \n"
                    "**- Para acciones o participaciones:** Nombre y NIT de la empresa, y cantidad de acciones.\n"
                    "**- Para CDTs o títulos valores:** Número del título y entidad financiera.\n"
                    "**- Para ganado/caballos:** Cantidad de animales, descripción, marcas o hierros de propiedad y ubicación.\n"
                    "**- Para derechos fiduciarios:** Número del contrato y nombre de la fiduciaria."
                ),
                "ejemplo": "Ejemplo: 1) Las 500 acciones de Ecopetrol S.A. (NIT 899.999.068-1) se repartirán en partes iguales. 2) El CDT No. 987654 del Banco Davivienda será para [Nombre del Cónyuge 1]. 3) Las 10 cabezas de ganado Brahman marcadas con el hierro 'La Herradura', se adjudicarán a [Nombre del Cónyuge 2]."
            },
            "deudas_conyugales": {
                "pregunta": "¿Cómo se repartirán las deudas adquiridas durante el matrimonio?",
                "ayuda": "Listen las deudas importantes (créditos hipotecarios, de consumo, tarjetas de crédito, etc.), indicando el acreedor (banco o entidad) y quién será responsable de pagar el saldo restante a partir de la firma del divorcio.",
                "ejemplo": "Ejemplo: La deuda del crédito hipotecario con el Banco BBVA, que pesa sobre el inmueble de matrícula 50C-1234567, será asumida en su totalidad por [Nombre del Cónyuge 1], liberando de toda responsabilidad a [Nombre del Cónyuge 2]."
            }
        }
    },
    # --- NUEVO BLOQUE DE CLÁUSULAS ADICIONALES ---
    {
        "nombre": "adicionales",
        "section_name": "Cláusulas Adicionales y Acuerdos Varios",
        "opcional": True,
        "introduccion": (
            "Esta es una sección libre para que incluyan cualquier otro acuerdo o punto específico que sea importante para ustedes y que no haya sido cubierto en las secciones anteriores. "
            "Un buen acuerdo es aquel que no deja lugar a dudas. Piensen en cualquier detalle que deseen dejar por escrito para garantizar la claridad a futuro."
        ),
        "clausulas_dict": {
            "acuerdo_adicional": {
                "pregunta": "Por favor, describe el acuerdo adicional que deseas incluir.",
                "ayuda": "Puedes añadir cualquier tipo de pacto, como acuerdos sobre mascotas, la renuncia a futuras reclamaciones, el manejo de bienes que aparecerán en el futuro, o cualquier otro punto que brinde tranquilidad a ambas partes.",
                "ejemplo": "Ejemplo: 'Ambas partes acuerdan que la mascota de la familia, un perro llamado 'Rocky', quedará bajo la custodia y cuidado de [Nombre del Cónyuge 2].' O también: 'Los cónyuges declaran que no existen más deudas o bienes por repartir y renuncian a cualquier reclamación futura sobre este asunto.'"
            }
        }
    }
]
# 
def generador_promt_engineering(contexto_datos_basicos, current, user_response, memoria=[], correccion=False):
    """
    Genera un prompt robusto y detallado para el LLM, con una regla estricta anti-placeholders.
    """
    
    if not correccion:
        # Prompt para la creación inicial de la cláusula
        prompt = f"""
## 1. ROL Y OBJETIVO ##
Actúa como un abogado colombiano experto en derecho de familia, con más de 20 años de experiencia en la redacción de acuerdos de divorcio de mutuo acuerdo. Tu objetivo es redactar una cláusula que sea legalmente sólida, precisa, clara, completa y que no deje lugar a ambigüedades, protegiendo los intereses de ambas partes de manera equitativa.

## 2. CONTEXTO DEL CASO ##
{contexto_datos_basicos}

## 3. TAREA ESPECÍFICA ##
Redacta una cláusula para la sección de "{current}". Las instrucciones proporcionadas por el usuario son las siguientes: "{user_response}".
Debes interpretar la solicitud del usuario y traducirla a un lenguaje legal formal y apropiado para un documento de esta naturaleza.

## 4. INSTRUCCIONES Y REGLAS DE ORO ##
- **Precisión Jurídica:** Utiliza terminología legal colombiana precisa.
- **Claridad Absoluta:** La redacción final tiene que ser comprensible para personas no expertas en derecho.
- **Exhaustividad:** Anticipa posibles vacíos o escenarios futuros.
- **Neutralidad y Equidad:** Redacta la cláusula desde una perspectiva neutral.
- **Tono Profesional:** El tono debe ser formal, sobrio y definitivo.
- **REGLA FUNDAMENTAL: CERO PLACEHOLDERS:** Bajo NINGUNA circunstancia la cláusula final debe contener variables, placeholders o textos entre corchetes o llaves (ej: `[Nombre del hijo]`, `{{valor del inmueble}}`, `[detallar más adelante]`). Toda la información necesaria, como nombres, cifras y detalles, debe ser extraída del contexto o de las instrucciones del usuario e integrada DIRECTAMENTE en la redacción. El texto generado debe ser completo y definitivo, listo para ser incluido en el documento final.

## 5. FORMATO DE SALIDA ##
La cláusula debe presentarse de la siguiente manera, sin incluir explicaciones adicionales ni saludos, solo el texto solicitado:
**CLÁUSULA [NÚMERO ROMANO A DETERMINAR]: [TÍTULO DESCRIPTIVO EN MAYÚSCULAS]**
[Texto completo de la cláusula aquí]

## 6. MANEJO DE ENTRADAS INVÁLIDAS ##
**REGLA CRÍTICA:** Si las instrucciones del usuario son ofensivas, absurdas, o no guardan NINGUNA relación con la tarea de redactar una cláusula de divorcio (ej: pide un chiste, una receta, un poema, etc.), NO intentes redactar la cláusula. En su lugar, tu ÚNICA respuesta debe ser, textualmente, la siguiente:
"He notado que la solicitud se desvía del objetivo de redactar el acuerdo de divorcio. Para continuar de forma productiva, por favor, proporciona instrucciones enfocadas en la cláusula que estamos trabajando. ¿Deseas volver a intentarlo?"
"""
    else:
        # Prompt para la corrección de una cláusula existente
        prompt = f"""
## 1. ROL Y OBJETIVO ##
Actúa como un abogado supervisor colombiano, experto en derecho de familia. Tu objetivo es revisar y perfeccionar una cláusula basándote en la retroalimentación del cliente. La nueva versión debe ser impecable.

## 2. CONTEXTO DEL CASO ##
{contexto_datos_basicos}

## 3. TAREA ESPECÍFICA DE CORRECCIÓN ##
A continuación se presenta una cláusula redactada previamente y las instrucciones del usuario para su modificación. Tu tarea es generar una nueva versión que incorpore estas correcciones.

**Cláusula anterior a corregir:**
"{memoria}"

**Instrucciones del usuario para la corrección:**
"{user_response}"

## 4. INSTRUCCIONES Y REGLAS DE ORO ##
- **Integración Perfecta:** Incorpora la corrección del usuario de forma natural y coherente.
- **Mantén la Calidad:** Asegúrate de que la cláusula siga cumpliendo con todas las reglas: Precisión Jurídica, Claridad Absoluta, Exhaustividad, Neutralidad y Tono Profesional.
- **Consistencia:** La nueva versión debe mantener el mismo tono y estilo legal.
- **REGLA FUNDAMENTAL: CERO PLACEHOLDERS:** La regla de no incluir placeholders (`[variables]`, `{{etc}}`) sigue aplicando. La nueva versión de la cláusula debe ser un texto final, completo y sin espacios para rellenar.

## 5. FORMATO DE SALIDA ##
La cláusula corregida debe presentarse de la siguiente manera, sin incluir explicaciones, solo el texto final:
**CLÁUSULA [NÚMERO ROMANO A DETERMINAR]: [TÍTULO DESCRIPTIVO EN MAYÚSCULAS]**
[Texto completo de la nueva versión de la cláusula aquí]

## 6. MANEJO DE ENTRADAS INVÁLIDAS ##
# ... (Sección sin cambios)
"""
        
    return prompt
        

# ================================
# ⚖️ Clase para PDF Jurídico Profesional
# ================================
# =========================================================
# ⚖️ Clases y Funciones Auxiliares para el PDF Profesional
# =========================================================

def escribir_texto_md(pdf, texto, line_height):
    """
    Escribe texto en el PDF, interpretando los dobles asteriscos (**) como negrilla.
    """
    # Establece la fuente base para el párrafo
    pdf.set_font("Arial", "", 12)
    partes = texto.split('**')
    
    for i, parte in enumerate(partes):
        # Las partes en índices impares (1, 3, ...) son las que están entre **
        if i % 2 == 1:
            pdf.set_font("Arial", "B", 12)
        else:
            pdf.set_font("Arial", "", 12)
        
        # pdf.write() es mejor para construir una línea con múltiples formatos
        pdf.write(line_height, parte.encode('latin-1', 'replace').decode('latin-1'))
    
    # Salto de línea al final del párrafo completo
    pdf.ln(line_height)


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 10)
        self.cell(0, 10, "ACUERDO DE CESACIÓN DE EFECTOS CIVILES DE MATRIMONIO", 0, 1, "C")
        self.ln(5)

    # --- MÉTODO MODIFICADO ---
    def footer(self):
        # Posición a 1.5 cm del final
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        
        # Marquilla de la firma alineada a la izquierda
        nombre_firma = "Generado por: Vargas, Castro & Ariza - Legaltech"
        self.cell(0, 10, nombre_firma, 0, 0, "L")

        # Número de página en la misma línea, alineado a la derecha
        self.cell(0, 10, f"Página {self.page_no()} de {{nb}}", 0, 0, "R")

def agregar_firmas(pdf, datos):
    """
    Añade los bloques de firmas con un diseño vertical robusto que evita el solapamiento.
    """
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "FIRMAS DE LAS PARTES", 0, 1, "C")
    pdf.ln(15)

    line_width = 85

    # --- Firma del Abogado Apoderado (Datos Fijos) ---
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, "El Apoderado,", 0, 1)
    pdf.ln(15)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + line_width, pdf.get_y())
    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, "SANTIAGO CASTRO", 0, 1)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, "C.C. 1.010.129.318 de Bogotá", 0, 1)
    pdf.cell(0, 7, "T.P. 108.291.7231 del C.S.J.", 0, 1)
    pdf.ln(20)

    # --- Firma Cónyuge 1 ---
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, "Cónyuge / Poderdante,", 0, 1)
    pdf.ln(15)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + line_width, pdf.get_y())
    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, datos['conyuge_1_nombre'].upper(), 0, 1)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, f"C.C. {datos['conyuge_1_cedula']} de {datos['conyuge_1_ciudad_cedula']}", 0, 1)
    pdf.ln(20)

    # --- Firma Cónyuge 2 ---
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, "Cónyuge / Poderdante,", 0, 1)
    pdf.ln(15)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + line_width, pdf.get_y())
    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, datos['conyuge_2_nombre'].upper(), 0, 1)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, f"C.C. {datos['conyuge_2_cedula']} de {datos['conyuge_2_ciudad_cedula']}", 0, 1)


async def manejar_bloque_clausulas(message: cl.Message = None, section_name=None, clausulas_dict=None, session_key_prefix=None, introduccion=None):
    step = cl.user_session.get("step", "start")
    # ... (el resto de las inicializaciones se mantienen igual)
    clausulas_pendientes = cl.user_session.get(f"{session_key_prefix}_pendientes")
    if clausulas_pendientes is None:
        clausulas_pendientes = list(clausulas_dict.keys())
        cl.user_session.set(f"{session_key_prefix}_pendientes", clausulas_pendientes)
        if introduccion:
            await cl.Message(content=f"## ⚖️ Sección: {section_name}\n\n*{introduccion}*").send()

    aprobadas = cl.user_session.get(f"{session_key_prefix}_aprobadas", {})
    cl.user_session.set(f"{session_key_prefix}_aprobadas", aprobadas)
    current = cl.user_session.get(f"{session_key_prefix}_actual", clausulas_pendientes[0])
    memoria = cl.user_session.get(f"{session_key_prefix}_memoria")
    if current not in aprobadas:
        aprobadas[current] = []
    datos_basicos = cl.user_session.get("datos_basicos", {})
    contexto_datos_basicos = "### CONTEXTO DEL CASO ###\nEstos son los datos de las partes involucradas:\n"
    for key, value in datos_basicos.items():
        etiqueta = key.replace("_", " ").capitalize()
        contexto_datos_basicos += f"- {etiqueta}: {value}\n"
    contexto_datos_basicos += "########################\n\n"

    # STEP: Iniciar cláusula
    if step == "start":
        cl.user_session.set(f"{session_key_prefix}_actual", current)
        cl.user_session.set("step", "input")
        clausula_info = clausulas_dict[current]
        pregunta = clausula_info["pregunta"]
        ayuda = clausula_info["ayuda"]
        ejemplo = clausula_info["ejemplo"]

        # LÍNEA MODIFICADA: Instrucción más clara y visual
        mensaje_completo = (
            f"**Cláusula sobre: {current.replace('_', ' ').capitalize()}**\n\n"
            f"**Pregunta:** {pregunta}\n\n"
            f"💡 **Ayuda:** *{ayuda}*\n\n"
            f"✍️ **{ejemplo}**\n\n"
            "> Por favor, describe tu acuerdo a continuación. También puedes escribir **omitir** para saltar esta cláusula."
        )
        await cl.Message(content=mensaje_completo).send()
        return False

    # STEP: Entrada del usuario
    elif step == "input":
        # ... (la lógica interna de este bloque se mantiene)
        if not message:
            return False
        user_response = message.content.strip()

        if user_response.lower() == "omitir":
            aprobadas[current].append(None)
            clausulas_pendientes.remove(current)
            if clausulas_pendientes:
                siguiente = clausulas_pendientes[0]
                cl.user_session.set(f"{session_key_prefix}_actual", siguiente)
                cl.user_session.set("step", "start")
                return await manejar_bloque_clausulas(None, section_name, clausulas_dict, session_key_prefix, introduccion)
            else:
                cl.user_session.set("step", None)
                await cl.Message(content=f"✅ Sección *{section_name}* completada.").send()
                return True
        else:
            await cl.Message(content="✍️ Redactando cláusula legal...").send()
            try:
                prompt = generador_promt_engineering(contexto_datos_basicos, current, user_response, memoria=[], correccion=False)
                response = client.chat.completions.create(
                    model="gpt-4o", messages=[{"role": "user", "content": prompt}]
                )
                output = response.choices[0].message.content
                cl.user_session.set(f"{session_key_prefix}_memoria", output)
                cl.user_session.set("step", "validate")
                await cl.Message(content="📄 **Propuesta de cláusula:**").send()
                await cl.Message(content=output).send()

                # LÍNEA MODIFICADA: Opciones de validación más claras
                mensaje_opciones = (
                    "¿Estás de acuerdo con esta propuesta?\n\n"
                    "**Tus opciones:**\n"
                    "- ✅ Escribe **sí** para aceptarla.\n"
                    "- ✍️ **Explica los cambios** que quieres hacer (ej: 'cámbialo a cada 20 días').\n"
                    "- ⏭️ Escribe **omitir** para descartarla."
                )
                await cl.Message(content=mensaje_opciones).send()

                return False
            except Exception as e:
                await cl.Message(content=f"❌ Error: {str(e)}").send()
                return False

    # STEP: Validación
    elif step == "validate":
        if not message:
            return False
        user_response = message.content.strip().lower()
        memoria = cl.user_session.get(f"{session_key_prefix}_memoria")

        # LÍNEA MODIFICADA: Opciones para agregar más cláusulas
        mensaje_agregar_mas = (
            "¿Deseas agregar otra cláusula sobre este mismo tema?\n\n"
            "**Tus opciones:**\n"
            "- ✅ Escribe **sí** para añadir otra.\n"
            "- ❌ Escribe **no** para continuar con la siguiente sección."
        )

        if user_response in ["sí", "si", "ok", "acepto", "de acuerdo"]:
            aprobadas[current].append(memoria)
            cl.user_session.set("step", "agregar")
            await cl.Message(content=mensaje_agregar_mas).send()
            return False

        elif user_response == "omitir":
            aprobadas[current].append(None)
            cl.user_session.set("step", "agregar")
            await cl.Message(content=mensaje_agregar_mas).send()
            return False

        else:
            await cl.Message(content="✍️ Reformulando cláusula...").send()
            try:
                prompt = generador_promt_engineering(contexto_datos_basicos, current, message.content.strip(), memoria, correccion=True)
                response = client.chat.completions.create(
                    model="gpt-4o", messages=[{"role": "user", "content": prompt}]
                )
                output = response.choices[0].message.content
                cl.user_session.set(f"{session_key_prefix}_memoria", output)
                await cl.Message(content="📄 **Nueva propuesta:**").send()
                await cl.Message(content=output).send()

                # LÍNEA MODIFICADA: Se reutiliza el mensaje de opciones claras
                mensaje_opciones_reformulado = (
                    "¿Estás de acuerdo con esta nueva versión?\n\n"
                    "**Tus opciones:**\n"
                    "- ✅ Escribe **sí** para aceptarla.\n"
                    "- ✍️ **Sigue explicando los cambios** que necesites.\n"
                    "- ⏭️ Escribe **omitir** para descartarla."
                )
                await cl.Message(content=mensaje_opciones_reformulado).send()

                return False
            except Exception as e:
                await cl.Message(content=f"❌ Error: {str(e)}").send()
                return False

    # STEP: ¿Agregar otra?
    elif step == "agregar":
        # ... (la lógica interna de este bloque se mantiene igual)
        if not message:
            return False
        user_response = message.content.strip().lower()

        if user_response in ["sí", "si"]:
            cl.user_session.set("step", "input")
            await cl.Message(content=f"✳️ Ingresa otra cláusula sobre *{current}*. Puedes escribir 'omitir' para saltar.").send()
            return False
        elif user_response == "no":
            clausulas_pendientes.remove(current)
            if clausulas_pendientes:
                siguiente = clausulas_pendientes[0]
                cl.user_session.set(f"{session_key_prefix}_actual", siguiente)
                cl.user_session.set("step", "start")
                return await manejar_bloque_clausulas(None, section_name, clausulas_dict, session_key_prefix, introduccion)
            else:
                cl.user_session.set("step", None)
                await cl.Message(content=f"✅ Sección *{section_name}* completada.").send()
                return True
        else:
            # LÍNEA MODIFICADA: Se reutiliza el mensaje de opciones claras
            mensaje_agregar_mas_error = (
                "Respuesta no válida. Por favor, indica si deseas agregar otra cláusula sobre este tema.\n\n"
                "**Tus opciones:**\n"
                "- ✅ Escribe **sí** para añadir otra.\n"
                "- ❌ Escribe **no** para continuar."
            )
            await cl.Message(content=mensaje_agregar_mas_error).send()
            return False



# ================================
# 🧱 Plantilla para documento legal
# ================================
def generar_documento_final(datos, clausulas_aprobadas):
    clausulas_texto = []
    for bloque in clausulas_aprobadas.values():
        for lista in bloque.values():
            for clausula in lista:
                if clausula:
                    clausulas_texto.append(clausula)

    cuerpo = "\n\n".join(clausulas_texto)

    return f"""
Señor NOTARIO 44 DEL CIRCULO DE BOGOTA, D.C.  

Santiago Castro, mayor de edad, domiciliado y residente en Bogota , identificado con la cédula de ciudadanía número 1010129318 expedida en Bogota, abogado titulada portadora de la tarjeta profesional número 1082917231 expedida por el Consejo Superior de la Judicatura, obrando en mi calidad de Apoderado de los señores {datos['conyuge_1_nombre']}, mujer, colombiana, mayor de edad, identificada con cédula de ciudadanía {datos['conyuge_1_cedula']} de {datos['conyuge_1_ciudad_cedula']}, domiciliada y residente en {datos['conyuge_1_ciudad_domicilio']}, de estado civil Casada con sociedad conyugal vigente y {datos['conyuge_2_nombre']}, varón, colombiano, mayor de edad, identificado con cédula de ciudadanía {datos['conyuge_2_cedula']} de {datos['conyuge_2_ciudad_cedula']}, domiciliado y residente en {datos['conyuge_2_ciudad_domicilio']}, de estado civil Casado con sociedad conyugal vigente, solicito respetuosamente a usted se sirva AUTORIZAR ESCRITURA PÚBLICA DE Cesación de efectos civiles de matrimonio católico Y LIQUIDACIÓN DE SOCIEDAD CONYUGAL formada entre el suscrito y mi apoderada de conformidad con el artículo 34 de la ley 962 de la 2005, reglamentado por el decreto número 4436 del 28 de noviembre de 2005 del Ministerio del Interior y de Justicia, de acuerdo a lo siguiente:

HECHOS

PRIMERO - MATRIMONIO:  
Autoridad ante quien se celebró: {datos['autoridad_matrimonio']}  
Ciudad: {datos['ciudad_matrimonio']}    Departamento: {datos['departamento_matrimonio']}  
País: Colombia.  
Registro Civil de Matrimonio No. {datos['registro_civil_numero']}  
Autoridad de registro: {datos['notaria_registro_union']}

SEGUNDO - ACUERDOS ENTRE LAS PARTES:

{cuerpo}

TERCERO - El estado de la sociedad conyugal es el siguiente: Casados entre sí, con sociedad conyugal vigente, la cual será disuelta y liquidada de mutuo acuerdo mediante este mismo trámite notarial.

PETICIONES

PRIMERA: Darle trámite a la presente solicitud de Cesación de efectos civiles de matrimonio católico y liquidación de sociedad conyugal, la cual se liquidará de conformidad con el acuerdo suscrito entre las partes, teniendo en cuenta la renuncia a gananciales.

SEGUNDA: Permitir el otorgamiento de la mencionada escritura con la comparecencia del suscrito apoderado y autorizarla de conformidad a la ley, protocolizando esta solicitud y todos sus anexos.

TERCERA: Comunicar a las autoridades que guardan los originales de los Registros Civiles de Matrimonio y Nacimiento la declaración de la Cesación de efectos civiles de matrimonio católico y Liquidación de la sociedad conyugal.

CUARTA: Expedir copias para cada uno de los Poderdantes.

FUNDAMENTOS DE DERECHO  
Ley 962 de 2005 Artículo 34; Decreto ley 960 de 1970 Artículos 4 y 5; Decreto Ley 1260 de 1970, y Artículo 42 de la Constitución Política y Decreto 4436 del 28 de noviembre de 2005 expedido por el Ministerio del Interior y de Justicia.
"""

def enviar_pdf_por_correo(destinatario, ruta_pdf, texto_documento):
    """
    Analiza el documento para generar un checklist de anexos y envía el correo con el PDF.
    """
    email_remitente = "danielcamilovs4@gmail.com"
    password_remitente = "arpb pogt ckny rwxm"

    if not email_remitente or not password_remitente:
        print("❌ Error: Las variables de entorno EMAIL_SENDER y EMAIL_PASSWORD no están configuradas.")
        return False
    
    try:
        # 1. Generar la lista de documentos necesarios
        print("🤖 Analizando el documento para generar checklist de anexos...")
        checklist_anexos = generar_checklist_documentos(texto_documento)
        print("✅ Checklist generado.")

        # 2. Construir el mensaje del correo
        msg = MIMEMultipart()
        msg["From"] = email_remitente
        msg["To"] = destinatario
        msg["Subject"] = "Entrega de su Documento Legal y Anexos Requeridos | Vargas, Castro & Ariza"

        cuerpo = f"""
Estimado(a) usuario(a),

Adjunto a este correo encontrará el borrador del Acuerdo de Divorcio que ha elaborado utilizando nuestro asistente legal inteligente.

En Vargas, Castro & Ariza - Soluciones Legaltech, integramos la precisión del derecho de familia tradicional con la eficiencia de la tecnología de vanguardia.

**Próximos Pasos: Documentos Requeridos**
Para la protocolización de este acuerdo ante notaría, deberá adjuntar la siguiente documentación:

{checklist_anexos}

Le recomendamos revisar el documento y reunir los anexos mencionados. Si requiere asesoría adicional, no dude en contactarnos.

Cordialmente,

--
**El Equipo de Vargas, Castro & Ariza**
Soluciones Legaltech
Bogotá, Colombia
www.vcalegaltech.com 

***
AVISO LEGAL: Este documento es un borrador generado automáticamente basado en la información que usted ha proporcionado. No constituye asesoría legal ni establece una relación abogado-cliente. Su validez final debe ser confirmada y protocolizada por un notario público. La confidencialidad de la información enviada por correo electrónico no puede ser garantizada.
"""
        msg.attach(MIMEText(cuerpo, "plain"))

        # 3. Adjuntar el archivo PDF
        with open(ruta_pdf, "rb") as f:
            adjunto = MIMEApplication(f.read(), _subtype="pdf")
            adjunto.add_header("Content-Disposition", "attachment", filename=os.path.basename(ruta_pdf))
            msg.attach(adjunto)

        # 4. Enviar el correo
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_remitente, password_remitente)
            server.send_message(msg)
        
        return True

    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")
        return False

def generar_checklist_documentos(texto_completo):
    """
    Usa un LLM para analizar CUALQUIER tipo de contrato y generar una lista de anexos necesarios,
    basándose en principios generales y distinguiendo entre las partes y su apoderado.
    """
    try:
        prompt = f"""
        ## ROL Y OBJETIVO ##
        Actúa como un asistente legal senior en una notaría colombiana, experto en la formalización y protocolización de toda clase de contratos y acuerdos. Tu objetivo es revisar CUALQUIER tipo de documento legal y generar una lista precisa de los documentos de soporte (anexos) que las partes deben presentar para que el acto tenga plena validez legal y registral. Tu reputación depende de tu exhaustividad y precisión.

        ## DOCUMENTO A ANALIZAR ##
        ```
        {texto_completo}
        ```

        ## PROCESO DE ANÁLISIS Y TAREA ##
        Sigue estos pasos rigurosamente:
        1.  **Análisis Conceptual:** Lee el "DOCUMENTO A ANALIZAR" e identifica los siguientes componentes clave:
            - **Las Partes Principales:** Quiénes son los clientes, poderdantes o implicados directos en el negocio.
            - **El Representante Legal:** Identifica si un abogado actúa como apoderado.
            - **El Hecho Principal:** Qué se está haciendo (vendiendo, arrendando, disolviendo un matrimonio, etc.).
            - **Los Activos Involucrados:** Qué objetos materiales o inmateriales son parte del acuerdo.

        2.  **Generación de Checklist:** Basado en tu análisis, crea una lista de documentos requeridos aplicando las siguientes reglas de oro.

        ## REGLAS DE ORO PARA LA LISTA ##
        1.  **Documentos de las Partes Principales:** Siempre solicita los documentos que acrediten la identidad y capacidad legal de los implicados directos.
            - Para **Personas Naturales**: Fotocopia de la cédula de ciudadanía. Si su estado civil es relevante, solicita el Registro Civil correspondiente (Nacimiento o Matrimonio).
            - Para **Personas Jurídicas**: Certificado de Existencia y Representación Legal reciente.

        2.  **Documentos de los Activos:** Por cada activo específico mencionado en el texto, solicita el documento estándar en Colombia que prueba su propiedad y estado legal.
            - Si se menciona un **Bien Inmueble**: Solicita el Certificado de Tradición y Libertad y paz y salvo de impuestos.
            - Si se menciona un **Vehículo**: Solicita la Tarjeta de Propiedad y paz y salvo de impuestos.
            - Si se mencionan **Acciones o Títulos Valores**: Solicita los certificados correspondientes.

        3.  **REGLA DE EXCLUSIVIDAD:** Tu análisis debe basarse **estrictamente** en el contenido del documento. Si un tipo de activo no se menciona, está **prohibido** solicitar documentos para ello.

        4.  **REGLA DE ORO (NUEVA Y MUY IMPORTANTE): Exclusión del Apoderado. Santiago Castro**
            La lista de documentos debe ser **exclusivamente para las partes principales del contrato (los clientes)**. Está **estrictamente prohibido** solicitar documentos personales del abogado que actúa como apoderado (ej: no pedir la cédula de ciudadanía ni la tarjeta profesional del abogado). El checklist es para los implicados, no para su representante legal.

        ## FORMATO DE SALIDA ##
        Genera únicamente una lista con viñetas (usando '-'), sin encabezados, saludos, resúmenes ni explicaciones adicionales.
        """
        response = client.chat.completions.create(
            # Se recomienda 'gpt-4o' para seguir mejor las reglas complejas
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ Error al generar el checklist de documentos: {e}")
        # Devuelve una lista genérica en caso de error
        return (
            "- Fotocopias de las cédulas de ciudadanía de las partes.\n"
            "- Documentos que acrediten la propiedad de los bienes mencionados."
        )



# ================================
# 🚀 Inicio del chat: pide datos
# ================================
@cl.on_chat_start
async def inicio():
    cl.user_session.set("bloque_idx", -1)
    cl.user_session.set("step", "recoger_datos")
    cl.user_session.set("datos_basicos", {})
    await cl.Message(content="👋 Bienvenido. Empecemos por ingresar los datos básicos para redactar el documento legal.").send()
    await solicitar_dato_basico()

def corregir_datos_basicos_con_llm(datos_usuario):
    """
    Usa un LLM para corregir errores ortográficos en los datos básicos del usuario,
    excepto en nombres y cédulas.
    """
    # Convierte el diccionario de Python a un string en formato JSON para el prompt
    datos_json_str = json.dumps(datos_usuario, indent=2, ensure_ascii=False)

    prompt = f"""
    ## ROL Y OBJETIVO ##
    Actúa como un asistente de data entry experto en la normalización y corrección de información para documentos legales en Colombia. Tu única tarea es corregir errores ortográficos y tipográficos en los valores del siguiente objeto JSON.

    ## DATOS A CORREGIR ##
    ```json
    {datos_json_str}
    ```

    ## REGLAS ESTRICTAS DE CORRECCIÓN ##
    1.  **NO MODIFICAR NOMBRES NI CÉDULAS:** Los valores de los campos que terminan en `_nombre` o `_cedula` son intocables. Debes devolverlos EXACTAMENTE como están en la entrada. Esta es tu regla más importante.
    2.  **CORREGIR CIUDADES Y OTROS DATOS:** Corrige errores tipográficos obvios en ciudades, departamentos o cualquier otro campo que no sea un nombre o cédula (ej: "BOGOTÁ D.C" -> "Bogotá D.C.", "notariaa" -> "Notaría"). Asegúrate de que los nombres de lugares correspondan a la nomenclatura oficial de Colombia.
    3.  **NO INVENTAR INFORMACIÓN:** Si un campo está vacío o no puedes determinar una corrección con certeza, déjalo como está.
    4.  **MANTENER LA ESTRUCTURA:** Tu respuesta debe ser ÚNICAMENTE el objeto JSON corregido, con la misma estructura y claves que el original. No añadas comentarios, explicaciones ni texto adicional.

    ## SALIDA ESPERADA (SOLO JSON) ##
    """

    try:
        print("🤖 Solicitando corrección de datos al LLM...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"} # Fuerza la salida en formato JSON
        )
        
        # El LLM devuelve el JSON como un string, lo convertimos a diccionario
        datos_corregidos = json.loads(response.choices[0].message.content)
        print("✅ Datos corregidos recibidos.")
        return datos_corregidos

    except Exception as e:
        print(f"❌ Error durante la corrección de datos: {e}. Se usarán los datos originales.")
        # En caso de cualquier error, devuelve los datos originales para no detener el flujo
        return datos_usuario

async def solicitar_dato_basico():
    datos = cl.user_session.get("datos_basicos", {})
    
    # Bucle para pedir los datos que faltan
    for campo in datos_basicos_requeridos:
        if campo not in datos or not datos[campo]:
            etiqueta = campo.replace("_", " ").capitalize()
            await cl.Message(content=f"✍️ Por favor, ingresa: **{etiqueta}**").send()
            cl.user_session.set("campo_actual", campo)
            return

    # --- BLOQUE AÑADIDO ---
    # Una vez que todos los datos están recopilados, los corregimos
    await cl.Message(content="Gracias. Verificando y corrigiendo la información ingresada...").send()
    
    # Llama a la nueva función de corrección
    datos_corregidos = corregir_datos_basicos_con_llm(datos)
    
    # Guarda los datos corregidos en la sesión del usuario
    cl.user_session.set("datos_basicos", datos_corregidos)
    
    await cl.Message(content="✅ ¡Información verificada!").send()
    # --- FIN DEL BLOQUE AÑADIDO ---

    # Avanza al primer bloque de cláusulas
    cl.user_session.set("step", "start")
    cl.user_session.set("bloque_idx", 0)
    await continuar(message=None)

@cl.on_message
async def continuar(message: cl.Message):
    step = cl.user_session.get("step")

    # === MANEJO DE PASOS DE LA CONVERSACIÓN ===

    if step == "recoger_datos":
        campo = cl.user_session.get("campo_actual")
        if campo:
            datos = cl.user_session.get("datos_basicos", {})
            datos[campo] = message.content.strip()
            cl.user_session.set("datos_basicos", datos)
            cl.user_session.set("campo_actual", None)
            await solicitar_dato_basico()
        return

    # NUEVO PASO: Confirma si el usuario quiere llenar el bloque opcional
    elif step == "confirmar_bloque":
        user_response = message.content.strip().lower()
        bloque_idx = cl.user_session.get("bloque_idx")

        if user_response in ["sí", "si", "ok", "continuar"]:
            # Si el usuario confirma, entra al bloque de cláusulas
            cl.user_session.set("step", "start")
            await continuar(message=None)
        
        elif user_response in ["no", "omitir", "saltar"]:
            # Si el usuario omite, salta al siguiente bloque
            cl.user_session.set("bloque_idx", bloque_idx + 1)
            cl.user_session.set("step", "start") # Reinicia el paso para el próximo bloque
            await continuar(message=None)
        
        else:
            # Pide una respuesta válida
            await cl.Message(content="Respuesta no válida. Por favor, responde **sí** para configurar esta sección o **no** para saltarla.").send()
        return
    elif step == "solicitar_correo":
        email_usuario = message.content.strip()
        nombre_archivo = cl.user_session.get("nombre_archivo_final")
        texto_final = cl.user_session.get("texto_final_documento") # <-- AÑADE ESTA LÍNEA

        await cl.Message(content=f"Gracias. Analizando el documento y enviándolo a **{email_usuario}**...").send()
        
        # LÍNEA MODIFICADA: Pasa el texto del documento
        enviado_con_exito = enviar_pdf_por_correo(email_usuario, nombre_archivo, texto_final)

        if enviado_con_exito:
            await cl.Message(content="✅ ¡Correo enviado! Por favor, revisa tu bandeja de entrada (y la carpeta de spam).").send()
        else:
            await cl.Message(content="Lo sentimos, ha ocurrido un error al intentar enviar el correo. Por favor, verifica que las credenciales del servidor estén bien configuradas.").send()
        
        # Opcional: reiniciar la conversación
        cl.user_session.set("step", "fin") # Marca el fin para no hacer nada más
        return    

    # === LÓGICA PRINCIPAL DE NAVEGACIÓN ===

    bloque_idx = cl.user_session.get("bloque_idx", 0)

# Si ya se completaron todos los bloques, genera el documento final
    if bloque_idx >= len(bloques_configurados):
        # 1. Recopila toda la información de la sesión
        datos = cl.user_session.get("datos_basicos", {})
        aprobadas = {
            b["nombre"]: cl.user_session.get(f"{b['nombre']}_aprobadas", {})
            for b in bloques_configurados
        }

        # 2. Genera el texto final del documento a partir de la plantilla
        texto_final = generar_documento_final(datos, aprobadas)
        cl.user_session.set("texto_final_documento", texto_final) # 

        await cl.Message(content="📄 Documento final generado. Creando PDF profesional...").send()

        # 3. Crea el objeto PDF y configura sus propiedades
        pdf = PDF('P', 'mm', 'Letter')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_margins(25, 20, 25)
        pdf.set_auto_page_break(auto=True, margin=20)
        line_height = 7
        
        # 4. Escribe el contenido del documento en el PDF, aplicando formato
        titulos_seccion = ["HECHOS", "PETICIONES", "FUNDAMENTOS DE DERECHO", "ACUERDOS ENTRE LAS PARTES"]
        for linea in texto_final.split("\n"):
            linea_limpia = linea.strip()
            if not linea_limpia:
                continue

            # Aplica formato a los títulos de sección
            if any(titulo in linea_limpia.upper() for titulo in titulos_seccion):
                pdf.ln(line_height)
                pdf.set_font("Arial", "B", 12)
                pdf.multi_cell(0, line_height, linea_limpia, 0, "C")
                pdf.set_font("Arial", "", 12)
                pdf.ln(line_height / 2)
            # Aplica formato de negrilla si detecta **
            elif "**" in linea_limpia:
                escribir_texto_md(pdf, linea_limpia, line_height)
            # Escribe el texto normal justificado
            else:
                pdf.set_font("Arial", "", 12)
                pdf.multi_cell(0, line_height, linea_limpia.encode('latin-1', 'replace').decode('latin-1'), 0, "J")

        # 5. Añade la página de firmas al final
        agregar_firmas(pdf, datos)

        # 6. Guarda el archivo PDF en el servidor
        nombre_archivo = "acuerdo_divorcio_profesional.pdf"
        pdf.output(nombre_archivo)
        print(f"✅ PDF generado y guardado localmente: {nombre_archivo}")

        # 7. Inicia el proceso para enviar el PDF por correo
        cl.user_session.set("nombre_archivo_final", nombre_archivo)
        cl.user_session.set("step", "solicitar_correo")
        await cl.Message(content="El documento está listo. Por favor, ingresa tu dirección de correo electrónico para enviártelo.").send()
        
        return

    # --- Flujo normal de bloques ---
    bloque_actual = bloques_configurados[bloque_idx]

    # Lógica para manejar bloques opcionales
    if bloque_actual.get("opcional") and step == "start":
        cl.user_session.set("step", "confirmar_bloque")
        mensaje_confirmacion = (
            f"Vamos a entrar a la sección sobre **{bloque_actual['section_name']}**.\n\n"
            f"*{bloque_actual['introduccion']}*\n\n"
            "**¿Deseas incluir y configurar esta sección en tu acuerdo?**"
        )
        await cl.Message(content=mensaje_confirmacion).send()
        return

    # Si el bloque es obligatorio o ya fue confirmado, se manejan las cláusulas
    terminado = await manejar_bloque_clausulas(
        message=message,
        section_name=bloque_actual["section_name"],
        clausulas_dict=bloque_actual["clausulas_dict"],
        session_key_prefix=bloque_actual["nombre"],
        introduccion=bloque_actual.get("introduccion")
    )

    # Si el bloque de cláusulas terminó, avanza al siguiente
    if terminado:
        cl.user_session.set("bloque_idx", bloque_idx + 1)
        cl.user_session.set("step", "start")
        await continuar(message=None)

