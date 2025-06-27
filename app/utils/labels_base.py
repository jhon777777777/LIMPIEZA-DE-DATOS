"""
Módulo Profesional de Etiquetas y Metadatos para la Encuesta Nacional de Hogares (ENAHO) - INEI 2023

Este módulo centraliza el conocimiento completo de la encuesta ENAHO 2023, replicando la funcionalidad
de los archivos de sintaxis de paquetes estadísticos como Stata o SPSS, con todas las variables documentadas.

Características:
- Diccionarios completos de descripciones de variables y etiquetas de valores para todos los módulos
- Funciones avanzadas de consulta para metadatos y generación de tablas de frecuencia
- Organizado por módulos temáticos según la estructura oficial del INEI
- Incluye variables de identificación, vivienda, educación, salud, empleo, gastos y programas sociales

Autor: [Tu Nombre]
Versión: 3.0.0 (Versión Completa ENAHO 2023)
Última actualización: [Fecha Actual]
"""
import pandas as pd
import streamlit as st
from typing import Dict, List, Optional, Union


# ==============================================================================
# SECCIÓN 1: DICCIONARIO COMPLETO DE DESCRIPCIONES DE VARIABLES (VARIABLE_DESCRIPTIONS)
# Fuente: Diccionario de Datos ENAHO 2023, INEI - Documento completo
# Nota: Todas las claves están en minúsculas para un manejo consistente.
# ==============================================================================
VARIABLE_DESCRIPTIONS = {
    # === Identificación y Ubicación Geográfica ===
    'año': 'Año de la encuesta',
    'mes': 'Mes de ejecución de la encuesta',
    'nconglome': 'Número de conglomerado (proveniente del marco)',
    'sub_conglome': 'Número de subconglomerado (proveniente del marco)',
    'conglome': 'Número de conglomerado',
    'vivienda': 'Número de selección de vivienda',
    'hogar': 'Número secuencial del hogar',
    'ubigeo': 'Código de ubicación geográfica (6 dígitos)',
    'dominio': 'Dominio geográfico (8 regiones naturales)',
    'estrato': 'Estrato geográfico (tamaño de población)',
    'periodo': 'Periodo de ejecución de la encuesta (1-5)',
    'tipenc': 'Tipo de selección del conglomerado',
    'fecent': 'Fecha de resultado final de la encuesta',
    'result': 'Resultado final de la encuesta (1-7)',
    'panel': '¿El hogar fue entrevistado el año pasado?',
    'factor07': 'Factor de expansión anual (proyecciones CPV-2007)',
    'codccpp': 'Código del centro poblado',
    'nomccpp': 'Nombre del centro poblado',
    'longitud': 'Longitud geográfica',
    'latitud': 'Latitud geográfica',

    # === Módulo 100: Características de la Vivienda y del Hogar ===
    'p101': 'Tipo de vivienda',
    'p102': 'Material predominante en las paredes exteriores',
    'p103a': 'Material predominante en los pisos',
    'p103': 'Material predominante en los techos',
    'p104': 'Número total de habitaciones en la vivienda',
    'p104a': 'Habitaciones usadas exclusivamente para dormir',
    'p104b1': '¿La vivienda cuenta con licencia de construcción?',
    'p104b2': '¿La vivienda fue construida con asistencia técnica profesional?',
    'p105a': 'Régimen de tenencia de la vivienda',
    'p105b': 'Monto mensual por alquiler o compra de la vivienda (S/.)',
    'p106': 'Valor estimado de alquiler mensual (S/.)',
    'p106a': '¿Esta vivienda tiene título de propiedad?',
    'p106b': '¿El título está registrado en SUNARP?',
    'p107b1': 'Crédito para comprar casa/departamento (últimos 12 meses)',
    'p107d1': 'Monto total del crédito para vivienda',
    'p110': 'Fuente principal de agua en el hogar',
    'p110a': '¿El agua es potable?',
    'p110a_modificada': 'Nivel de cloro residual del agua',
    'p110c': '¿Tiene acceso al servicio de agua todos los días?',
    'p110c1': 'Horas de servicio de agua al día',
    'p110c2': 'Días de servicio de agua a la semana',
    'p110f': '¿Pagan por el servicio de agua?',
    'p110g': 'Entidad a la que se paga por el agua',
    'p111a': 'Tipo de conexión del servicio higiénico',
    'p1121': 'Tipo de alumbrado: Electricidad',
    'p1123': 'Tipo de alumbrado: Petróleo/Gas',
    'p1124': 'Tipo de alumbrado: Vela',
    'p1125': 'Tipo de alumbrado: Generador',
    'p1126': 'Tipo de alumbrado: Otro',
    'p1127': 'No utiliza alumbrado en el hogar',
    'p112a': 'Tipo de servicio eléctrico',
    'p1131': 'Combustible para cocinar: Electricidad',
    'p1132': 'Combustible para cocinar: Gas (balón GLP)',
    'p1133': 'Combustible para cocinar: Gas natural',
    'p1135': 'Combustible para cocinar: Carbón',
    'p1136': 'Combustible para cocinar: Leña',
    'p1139': 'Combustible para cocinar: Bosta/estiércol',
    'p1137': 'Combustible para cocinar: Otro',
    'p1138': 'No cocinan',
    'p113a': 'Combustible más usado para cocinar',
    'p1141': 'El hogar tiene: Teléfono fijo',
    'p1142': 'El hogar tiene: Teléfono celular',
    'p1143': 'El hogar tiene: TV por cable/satelital',
    'p1144': 'El hogar tiene: Conexión a Internet',
    'p1148b1': 'Conexión a internet: Fija',
    'p1148b2': 'Conexión a internet: Móvil postpago',
    'p1148b3': 'Conexión a internet: Móvil prepago',
    'p1145': 'No tiene servicios de comunicación',
    'p1171$01': 'Gasto mensual en agua',
    'p1171$02': 'Gasto mensual en electricidad',
    'p1171$04': 'Gasto mensual en gas (balón GLP)',
    'p1171$05': 'Gasto mensual en gas natural',
    'p1171$06': 'Gasto mensual en velas',
    'p1171$07': 'Gasto mensual en carbón',
    'p1171$08': 'Gasto mensual en leña',
    'p1171$09': 'Gasto mensual en petróleo',
    'p1171$10': 'Gasto mensual en gasolina',
    'p1171$11': 'Gasto mensual en teléfono fijo',
    'p1171$12': 'Gasto mensual en celular',
    'p1171$13': 'Gasto mensual en TV cable/satelital',
    'p1171$14': 'Gasto mensual en internet',
    'p1171$15': 'Gasto mensual en otros servicios',
    'p1171$16': 'Gasto mensual en bosta/estiércol',
    'p1171$17': 'Gasto mensual en internet portátil',
    'p1172$01': 'Monto pagado por agua',
    'p1172$02': 'Monto pagado por electricidad',
    'p1172$04': 'Monto pagado por gas (balón GLP)',
    'p1172$05': 'Monto pagado por gas natural',
    'p1172$06': 'Monto pagado por velas',
    'p1172$07': 'Monto pagado por carbón',
    'p1172$08': 'Monto pagado por leña',
    'p1172$09': 'Monto pagado por petróleo',
    'p1172$10': 'Monto pagado por gasolina',
    'p1172$11': 'Monto pagado por teléfono fijo',
    'p1172$12': 'Monto pagado por celular',
    'p1172$13': 'Monto pagado por TV cable/satelital',
    'p1172$14': 'Monto pagado por internet',
    'p1172$15': 'Monto pagado por otros servicios',
    'p1172$16': 'Monto pagado por bosta/estiércol',
    'p1172$17': 'Monto pagado por internet portátil',
    'p1173$01': 'Agua donada/regalada',
    'p1173$02': 'Electricidad donada/regalada',
    'p1173$04': 'Gas (balón GLP) donado/regalado',
    'p1173$05': 'Gas natural donado/regalado',
    'p1173$06': 'Velas donadas/regaladas',
    'p1173$07': 'Carbón donado/regalado',
    'p1173$08': 'Leña donada/regalada',
    'p1173$09': 'Petróleo donado/regalado',
    'p1173$10': 'Gasolina donada/regalada',
    'p1173$11': 'Teléfono fijo donado/regalado',
    'p1173$12': 'Celular donado/regalado',
    'p1173$13': 'TV cable/satelital donado/regalado',
    'p1173$14': 'Internet donado/regalado',
    'p1173$15': 'Otros servicios donados/regalados',
    'p1173$16': 'Bosta/estiércol donado/regalado',
    'p1173$17': 'Internet portátil donado/regalado',
    'p1174$04': 'Gas (balón GLP) por autoconsumo',
    'p1174$05': 'Gas natural por autoconsumo',
    'p1174$06': 'Velas por autoconsumo',
    'p1174$07': 'Carbón por autoconsumo',
    'p1174$08': 'Leña por autoconsumo',
    'p1174$09': 'Petróleo por autoconsumo',
    'p1174$10': 'Gasolina por autoconsumo',
    'p1174$15': 'Otros por autoconsumo',
    'p1174$16': 'Bosta/estiércol por autoconsumo',
    'p1175$01': 'Agua incluida en alquiler',
    'p1175$02': 'Electricidad incluida en alquiler',
    'p1175$04': 'Gas (balón GLP) incluido en alquiler',
    'p1175$05': 'Gas natural incluido en alquiler',
    'p1175$06': 'Velas incluidas en alquiler',
    'p1175$07': 'Carbón incluido en alquiler',
    'p1175$08': 'Leña incluida en alquiler',
    'p1175$09': 'Petróleo incluido en alquiler',
    'p1175$10': 'Gasolina incluida en alquiler',
    'p1175$11': 'Teléfono fijo incluido en alquiler',
    'p1175$12': 'Celular incluido en alquiler',
    'p1175$13': 'TV cable/satelital incluido en alquiler',
    'p1175$14': 'Internet incluido en alquiler/celular',
    'p1175$15': 'Otros incluidos en alquiler',
    'p1175$16': 'Bosta/estiércol incluido en alquiler',
    'p1175$17': 'Internet portátil incluido en alquiler/celular',
    'p11772': 'Total gasto mensual pagado por el hogar',
    'p11773': 'Total gasto mensual donado por otros',
    'p11774': 'Total gasto mensual por autoconsumo',
    'nb11': 'NBI: Vivienda inadecuada',
    'nb12': 'NBI: Hacinamiento',
    'nb13': 'NBI: Sin servicios higiénicos',
    'nb14': 'NBI: Niños que no asisten a la escuela',
    'nb15': 'NBI: Alta dependencia económica',

    # === Módulo 200: Características de los Miembros del Hogar ===
    'p201p': 'Código panel de la persona',
    'p203': 'Relación de parentesco con el jefe del hogar',
    'p203a': 'Número del núcleo familiar',
    'p203b': 'Relación con el jefe del núcleo familiar',
    'p204': '¿Es miembro del hogar?',
    'p205': '¿Se encuentra ausente del hogar 30 días o más?',
    'p206': '¿Está presente en el hogar 30 días o más?',
    'p207': 'Sexo',
    'p208a': 'Edad en años cumplidos',
    'p208b': 'Edad en meses (para menores de 1 año)',
    'p209': 'Estado civil o conyugal',
    'p210': 'Actividad laboral la semana pasada',
    'p211a': 'Tipo de actividad realizada',
    'p211d': 'Horas totales dedicadas a la actividad',
    'p212': 'Persona para módulo de Educación (3+ años)',
    'p213': 'Persona para módulo de Salud (todas)',
    'p214': 'Persona para módulo de Empleo/Ingresos (14+ años)',
    'p215': 'Número de orden de la persona en el año anterior (panel)',
    'p216': 'Persona nueva (panel)',
    'p217': 'Motivo por el que ya no vive en el hogar (panel)',
    't211': 'Actividad recodificada de la semana pasada',
    'ocupac_r3': 'Código de ocupación (CIUO-88)',
    'ocupac_r4': 'Código de ocupación (CNO-2015)',
    'rama_r3': 'Código de actividad (CIIU-R3)',
    'rama_r4': 'Código de actividad (CIIU-R4)',
    'codtarea': 'Código de tarea peligrosa o no',
    'facpob07': 'Factor de expansión de población (CPV-2007)',

    # === Módulo 300: Educación (Personas de 3+ años) ===
    'p300a': '¿Asiste actualmente a un centro de enseñanza?',
    'p300b': '¿Por qué no asiste actualmente?',
    'p301a': '¿Sabe leer y escribir?',
    'p301b': 'Nivel educativo más alto alcanzado',
    'p301c': 'Último año/grado aprobado',
    'p302': '¿En qué nivel está matriculado actualmente?',
    'p303': 'Grado/año de estudio actual',
    'p304': 'Tipo de centro educativo',
    'p305': '¿El centro educativo es público o privado?',
    'p306': '¿Recibe enseñanza en lengua nativa?',
    'p307': 'Idioma o lengua materna',
    'p308': '¿Cuánto tiempo demora en llegar al centro educativo?',
    'p309': 'Medio de transporte utilizado',
    'p310': '¿Recibe desayuno/almuerzo escolar?',
    'p311': '¿Cuánto gasta mensualmente en educación?',
    'p312': '¿Algún miembro del hogar recibe beca?',
    'p313': 'Monto mensual de la beca',

    # === Módulo 400: Salud (Todas las personas) ===
    'p401': 'Tipo de seguro de salud al que está afiliado',
    'p401h': '¿Tiene algún problema de salud crónico?',
    'p402': 'Problema de salud crónico específico',
    'p403': '¿En los últimos 3 meses buscó atención médica?',
    'p404': 'Motivo por el que no buscó atención médica',
    'p405': 'Tipo de establecimiento donde buscó atención',
    'p406': '¿Fue atendido?',
    'p407': 'Motivo por el que no fue atendido',
    'p408': '¿Pagó por la atención médica?',
    'p409': 'Monto pagado por la atención médica',
    'p410': '¿Recibió medicamentos?',
    'p411': '¿Pagó por los medicamentos?',
    'p412': 'Monto pagado por medicamentos',
    'p413': '¿En los últimos 3 meses estuvo hospitalizado?',
    'p414': 'Días de hospitalización',
    'p415': '¿Pagó por la hospitalización?',
    'p416': 'Monto pagado por hospitalización',
    'p417': '¿En los últimos 3 meses tuvo emergencia médica?',
    'p418': '¿Pagó por la emergencia médica?',
    'p419': 'Monto pagado por emergencia médica',
    'p420': '¿En las últimas 4 semanas tuvo malestar/enfermedad?',
    'p421': 'Tipo de malestar/enfermedad',
    'p422': '¿Buscó atención médica por este malestar?',
    'p423': 'Tipo de establecimiento donde buscó atención',
    'p424': '¿Fue atendido?',
    'p425': '¿Pagó por esta atención médica?',
    'p426': 'Monto pagado por esta atención médica',
    'p427': '¿Recibió medicamentos para este malestar?',
    'p428': '¿Pagó por estos medicamentos?',
    'p429': 'Monto pagado por estos medicamentos',
    'p430': '¿En los últimos 12 meses tuvo accidente?',
    'p431': 'Tipo de accidente',
    'p432': '¿Buscó atención médica por el accidente?',
    'p433': 'Tipo de establecimiento donde buscó atención',
    'p434': '¿Fue atendido?',
    'p435': '¿Pagó por esta atención médica?',
    'p436': 'Monto pagado por esta atención médica',
    'p437': '¿Recibió medicamentos por el accidente?',
    'p438': '¿Pagó por estos medicamentos?',
    'p439': 'Monto pagado por estos medicamentos',
    'p440': '¿En los últimos 12 meses tuvo discapacidad?',
    'p441': 'Tipo de discapacidad',
    'p442': '¿Recibe pensión por discapacidad?',
    'p443': 'Monto de la pensión por discapacidad',
    'p444': '¿Usa algún aparato ortopédico?',
    'p445': '¿Pagó por el aparato ortopédico?',
    'p446': 'Monto pagado por el aparato ortopédico',

    # === Módulo 500: Empleo e Ingresos (Personas de 14+ años) ===
    'p501': '¿Trabajó la semana pasada?',
    'p502': 'Razón principal por la que no trabajó',
    'p503': '¿Buscó trabajo la semana pasada?',
    'p504': 'Razón por la que no buscó trabajo',
    'p505': 'Disponibilidad para trabajar',
    'p506': 'Tiempo sin trabajar/buscando trabajo',
    'p507': 'Ocupación principal (CIUO-08)',
    'p508': 'Actividad principal (CIIU Rev.4)',
    'p509': 'Tamaño de la empresa/negocio',
    'p510': '¿Dónde realiza su trabajo principal?',
    'p511a': 'Horas trabajadas en la ocupación principal',
    'p511b': 'Horas trabajadas en otras ocupaciones',
    'p512a': '¿Desea trabajar más horas?',
    'p512b': 'Razón por la que no desea trabajar más horas',
    'p513': 'Rama de actividad principal (CIIU Rev.4)',
    'p514': 'Categoría de ocupación en trabajo principal',
    'p515': '¿Tiene contrato de trabajo?',
    'p516': 'Tipo de contrato de trabajo',
    'p517': '¿Está afiliado a algún sistema de pensiones?',
    'p518': 'Sistema de pensiones al que está afiliado',
    'p519': '¿Recibe beneficios laborales?',
    'p520': 'Tipo de beneficios laborales que recibe',
    'p521': 'Categoría de ocupación en el trabajo principal',
    'p522': 'Ingreso bruto mensual en la ocupación principal',
    'p523': 'Ingreso neto mensual en la ocupación principal',
    'p524': 'Ingreso por horas extras en la ocupación principal',
    'p525': 'Ingreso por bonificaciones en la ocupación principal',
    'p526': 'Ingreso por gratificaciones en la ocupación principal',
    'p527': 'Ingreso por CTS en la ocupación principal',
    'p528': 'Ingreso por utilidades en la ocupación principal',
    'p529': 'Ingreso por otros conceptos en la ocupación principal',
    'p530': 'Ingreso total mensual en la ocupación principal',
    'p531': 'Ingreso mensual en otras ocupaciones',
    'p532': 'Ingreso mensual por trabajos independientes',
    'p533': 'Ingreso mensual por rentas',
    'p534': 'Ingreso mensual por intereses/dividendos',
    'p535': 'Ingreso mensual por pensiones/jubilaciones',
    'p536': 'Ingreso mensual por remesas',
    'p537': 'Ingreso mensual por otros conceptos',
    'p538': 'Ingreso total mensual del hogar',
    'i524': 'Ingreso mensual principal (imputado)',
    'inghog1d': 'Ingreso total del hogar (anualizado)',
    'gashog1d': 'Gasto total del hogar (anualizado)',

    # === Módulo 600: Gastos del Hogar ===
    # Submódulo 601: Gastos en alimentos y bebidas
    'p601x': 'Nombre del producto alimenticio',
    'p601b': '¿Obtuvo este producto en los últimos 15 días?',
    'p601a1': 'Forma de obtención: Comprado',
    'p601a2': 'Forma de obtención: Autoconsumo',
    'p601a3': 'Forma de obtención: Autosuministro',
    'p601a4': 'Forma de obtención: Parte de pago',
    'p601a5': 'Forma de obtención: Regalado por otro hogar',
    'p601a6': 'Forma de obtención: Donado por programa social',
    'p601a7': 'Forma de obtención: Otro',
    'p601b1': 'Frecuencia de compra',
    'p601b2': 'Cantidad comprada',
    'p601b3': 'Unidad de medida de compra',
    'p601c': 'Lugar de compra',
    'p601d1': 'Frecuencia de obtención',
    'p601d2': 'Cantidad obtenida',
    'p601d3': 'Unidad de medida de obtención',
    'p601e': 'Monto total de la compra',
    'i601b2': 'Cantidad comprada en kilos (imputado)',
    'i601c': 'Monto de compra (imputado)',
    'i601d2': 'Cantidad obtenida en kilos (imputado)',
    'i601e': 'Monto estimado (imputado)',
    
    # Submódulo 602: Alimentos de instituciones benéficas
    'p602': '¿Recibió alimentos de instituciones benéficas?',
    'p602a1': 'Veces por semana que recibe alimentos',
    'p602b1': 'Raciones recibidas cada vez',
    'p602c1': 'Miembros del hogar que consumen',
    'p602d1a': '¿Pagó por el alimento?',
    'p602d1b': '¿Pagó por otros conceptos asociados?',
    'p602e3': 'Monto pagado por el alimento',
    'p602e4': 'Monto pagado por otros conceptos',
    'd602e3': 'Monto pagado por alimento (deflactado)',
    'd602e4': 'Monto pagado por otros conceptos (deflactado)',
    'i602e3': 'Monto pagado por alimento (imputado)',
    'i602e4': 'Monto pagado por otros conceptos (imputado)',
    
    # Submódulo 603: Mantenimiento de la vivienda
    'p603n': 'Producto/servicio de mantenimiento',
    'p603': '¿Obtuvo este producto/servicio en el mes anterior?',
    'p603a1': 'Forma de obtención: Comprado',
    'p603a2': 'Forma de obtención: Autoconsumo',
    'p603a3': 'Forma de obtención: Autosuministro',
    'p603a4': 'Forma de obtención: Parte de pago',
    'p603a5': 'Forma de obtención: Regalado por otro hogar',
    'p603a6': 'Forma de obtención: Donado por programa',
    'p603a7': 'Forma de obtención: Otro',
    'p603aa': 'Lugar de compra',
    'p603b': 'Monto total por la compra',
    'p603c2': 'Valor estimado si fue autoconsumo',
    'p603c3': 'Valor estimado si fue autosuministro',
    'p603c4': 'Valor estimado si fue parte de pago',
    'p603c5': 'Valor estimado si fue regalado',
    'p603c6': 'Valor estimado si fue donado',
    'p603c7': 'Valor estimado si fue otro',
    'p603c': 'Valor estimado total',
    'd603b': 'Monto de compra (deflactado)',
    'd603c2': 'Valor autoconsumo (deflactado)',
    'd603c3': 'Valor autosuministro (deflactado)',
    'd603c4': 'Valor parte de pago (deflactado)',
    'd603c5': 'Valor regalado (deflactado)',
    'd603c6': 'Valor donado (deflactado)',
    'd603c7': 'Valor otro (deflactado)',
    'd603c': 'Valor total estimado (deflactado)',
    'i603b': 'Monto de compra (imputado)',
    'i603c2': 'Valor autoconsumo (imputado)',
    'i603c3': 'Valor autosuministro (imputado)',
    'i603c4': 'Valor parte de pago (imputado)',
    'i603c5': 'Valor regalado (imputado)',
    'i603c6': 'Valor donado (imputado)',
    'i603c7': 'Valor otro (imputado)',
    'i603c': 'Valor total estimado (imputado)',
    
    # Submódulo 604: Transportes y comunicaciones
    'p604n': 'Producto/servicio de transporte/comunicación',
    'p604': '¿Obtuvo este producto/servicio en el mes anterior?',
    'p604a1': 'Forma de obtención: Comprado',
    'p604a2': 'Forma de obtención: Autoconsumo',
    'p604a3': 'Forma de obtención: Autosuministro',
    'p604a4': 'Forma de obtención: Parte de pago',
    'p604a5': 'Forma de obtención: Regalado por otro hogar',
    'p604a6': 'Forma de obtención: Donado por programa',
    'p604a7': 'Forma de obtención: Otro',
    'p604aa': 'Lugar de compra',
    'p604b': 'Monto total por la compra',
    'p604c2': 'Valor estimado si fue autoconsumo',
    'p604c3': 'Valor estimado si fue autosuministro',
    'p604c4': 'Valor estimado si fue parte de pago',
    'p604c5': 'Valor estimado si fue regalado',
    'p604c6': 'Valor estimado si fue donado',
    'p604c7': 'Valor estimado si fue otro',
    'p604c': 'Valor estimado total',
    'd604b': 'Monto de compra (deflactado)',
    'd604c2': 'Valor autoconsumo (deflactado)',
    'd604c3': 'Valor autosuministro (deflactado)',
    'd604c4': 'Valor parte de pago (deflactado)',
    'd604c5': 'Valor regalado (deflactado)',
    'd604c6': 'Valor donado (deflactado)',
    'd604c7': 'Valor otro (deflactado)',
    'd604c': 'Valor total estimado (deflactado)',
    'i604b': 'Monto de compra (imputado)',
    'i604c2': 'Valor autoconsumo (imputado)',
    'i604c3': 'Valor autosuministro (imputado)',
    'i604c4': 'Valor parte de pago (imputado)',
    'i604c5': 'Valor regalado (imputado)',
    'i604c6': 'Valor donado (imputado)',
    'i604c7': 'Valor otro (imputado)',
    'i604c': 'Valor total estimado (imputado)',
    
    # Submódulo 605: Servicios a la vivienda
    'p605n': 'Servicio a la vivienda',
    'p605': '¿Utilizó este servicio en el mes anterior?',
    'p605a1': 'Forma de pago: Pagado por el hogar',
    'p605a2': 'Forma de pago: Regalado por otro hogar',
    'p605a3': 'No gastó',
    'p605a4': 'Incluido en el alquiler',
    'p605a5': 'Otro',
    'p605b': 'Monto mensual por el servicio',
    'p605c2': 'Valor estimado si fue regalado',
    'p605c3': 'Valor estimado si no gastó',
    'p605c4': 'Valor estimado si incluido en alquiler',
    'p605c5': 'Valor estimado si fue otro',
    'p605c': 'Valor estimado total',
    'd605b': 'Monto del servicio (deflactado)',
    'd605c2': 'Valor regalado (deflactado)',
    'd605c3': 'Valor no gastó (deflactado)',
    'd605c4': 'Valor incluido en alquiler (deflactado)',
    'd605c5': 'Valor otro (deflactado)',
    'd605c': 'Valor total estimado (deflactado)',
    'i605b': 'Monto del servicio (imputado)',
    'i605c2': 'Valor regalado (imputado)',
    'i605c3': 'Valor no gastó (imputado)',
    'i605c4': 'Valor incluido en alquiler (imputado)',
    'i605c5': 'Valor otro (imputado)',
    'i605c': 'Valor total estimado (imputado)',
    
    # Submódulo 606: Esparcimiento, diversión y cultura
    'p606n': 'Producto/servicio de esparcimiento/cultura',
    'p606': '¿Obtuvo este producto/servicio en el mes anterior?',
    'p606a1': 'Forma de obtención: Comprado',
    'p606a2': 'Forma de obtención: Autoconsumo',
    'p606a3': 'Forma de obtención: Autosuministro',
    'p606a4': 'Forma de obtención: Parte de pago',
    'p606a5': 'Forma de obtención: Regalado por otro hogar',
    'p606a6': 'Forma de obtención: Donado por programa',
    'p606a7': 'Forma de obtención: Otro',
    'p606aa': 'Lugar de compra',
    'p606b': 'Monto total por la compra',
    'p606c2': 'Valor estimado si fue autoconsumo',
    'p606c3': 'Valor estimado si fue autosuministro',
    'p606c4': 'Valor estimado si fue parte de pago',
    'p606c5': 'Valor estimado si fue regalado',
    'p606c6': 'Valor estimado si fue donado',
    'p606c7': 'Valor estimado si fue otro',
        'p606c': 'Valor estimado total',
    'd606b': 'Monto de compra (deflactado)',
    'd606c2': 'Valor autoconsumo (deflactado)',
    'd606c3': 'Valor autosuministro (deflactado)',
    'd606c4': 'Valor parte de pago (deflactado)',
    'd606c5': 'Valor regalado (deflactado)',
    'd606c6': 'Valor donado (deflactado)',
    'd606c7': 'Valor otro (deflactado)',
    'd606c': 'Valor total estimado (deflactado)',
    'i606b': 'Monto de compra (imputado)',
    'i606c2': 'Valor autoconsumo (imputado)',
    'i606c3': 'Valor autosuministro (imputado)',
    'i606c4': 'Valor parte de pago (imputado)',
    'i606c5': 'Valor regalado (imputado)',
    'i606c6': 'Valor donado (imputado)',
    'i606c7': 'Valor otro (imputado)',
    'i606c': 'Valor total estimado (imputado)',
    
    # Submódulo 606D: Bienes y servicios de cuidados personales
    'p606dn': 'Producto/servicio de cuidado personal',
    'p606d': '¿Obtuvo este producto/servicio en el mes anterior?',
    'p606da1': 'Forma de obtención: Comprado',
    'p606da2': 'Forma de obtención: Autoconsumo',
    'p606da3': 'Forma de obtención: Autosuministro',
    'p606da4': 'Forma de obtención: Parte de pago',
    'p606da5': 'Forma de obtención: Regalado por otro hogar',
    'p606da6': 'Forma de obtención: Donado por programa',
    'p606da7': 'Forma de obtención: Otro',
    'p606daa': 'Lugar de compra',
    'p606db': 'Monto total por la compra',
    'p606dc2': 'Valor estimado si fue autoconsumo',
    'p606dc3': 'Valor estimado si fue autosuministro',
    'p606dc4': 'Valor estimado si fue parte de pago',
    'p606dc5': 'Valor estimado si fue regalado',
    'p606dc6': 'Valor estimado si fue donado',
    'p606dc7': 'Valor estimado si fue otro',
    'p606dc': 'Valor estimado total',
    'd606db': 'Monto de compra (deflactado)',
    'd606dc2': 'Valor autoconsumo (deflactado)',
    'd606dc3': 'Valor autosuministro (deflactado)',
    'd606dc4': 'Valor parte de pago (deflactado)',
    'd606dc5': 'Valor regalado (deflactado)',
    'd606dc6': 'Valor donado (deflactado)',
    'd606dc7': 'Valor otro (deflactado)',
    'd606dc': 'Valor total estimado (deflactado)',
    'i606db': 'Monto de compra (imputado)',
    'i606dc2': 'Valor autoconsumo (imputado)',
    'i606dc3': 'Valor autosuministro (imputado)',
    'i606dc4': 'Valor parte de pago (imputado)',
    'i606dc5': 'Valor regalado (imputado)',
    'i606dc6': 'Valor donado (imputado)',
    'i606dc7': 'Valor otro (imputado)',
    'i606dc': 'Valor total estimado (imputado)',
    
    # Submódulo 607: Vestido y calzado
    'p607n': 'Prenda de vestir o calzado',
    'p607': '¿Obtuvo este producto en los últimos 3 meses?',
    'p607a1': 'Forma de obtención: Comprado',
    'p607a2': 'Forma de obtención: Autoconsumo',
    'p607a3': 'Forma de obtención: Autosuministro',
    'p607a4': 'Forma de obtención: Parte de pago',
    'p607a5': 'Forma de obtención: Regalado por otro hogar',
    'p607a6': 'Forma de obtención: Donado por programa',
    'p607a7': 'Forma de obtención: Otro',
    'p607aa': 'Lugar de compra',
    'p607b': 'Monto total por la compra',
    'p607c2': 'Valor estimado si fue autoconsumo',
    'p607c3': 'Valor estimado si fue autosuministro',
    'p607c4': 'Valor estimado si fue parte de pago',
    'p607c5': 'Valor estimado si fue regalado',
    'p607c6': 'Valor estimado si fue donado',
    'p607c7': 'Valor estimado si fue otro',
    'p607c': 'Valor estimado total',
    'd607b': 'Monto de compra (deflactado)',
    'd607c2': 'Valor autoconsumo (deflactado)',
    'd607c3': 'Valor autosuministro (deflactado)',
    'd607c4': 'Valor parte de pago (deflactado)',
    'd607c5': 'Valor regalado (deflactado)',
    'd607c6': 'Valor donado (deflactado)',
    'd607c7': 'Valor otro (deflactado)',
    'd607c': 'Valor total estimado (deflactado)',
    'i607b': 'Monto de compra (imputado)',
    'i607c2': 'Valor autoconsumo (imputado)',
    'i607c3': 'Valor autosuministro (imputado)',
    'i607c4': 'Valor parte de pago (imputado)',
    'i607c5': 'Valor regalado (imputado)',
    'i607c6': 'Valor donado (imputado)',
    'i607c7': 'Valor otro (imputado)',
    'i607c': 'Valor total estimado (imputado)',
    
    # Submódulo 609: Gastos de transferencias
    'p609n': 'Tipo de transferencia',
    'p609': '¿Realizó este gasto en los últimos 3 meses?',
    'p609a1': 'Forma de pago: Efectivo',
    'p609a2': 'Forma de pago: Especies',
    'p609a3': 'Forma de pago: Otro',
    'p609b': 'Monto total de la transferencia',
    'p609c': 'Frecuencia de la transferencia',
    'd609b': 'Monto de transferencia (deflactado)',
    'i609b': 'Monto de transferencia (imputado)',
    
    # Submódulo 610: Muebles y enseres
    'p610n': 'Mueble o enser',
    'p610': '¿Adquirió este artículo en los últimos 12 meses?',
    'p610a1': 'Forma de obtención: Comprado',
    'p610a2': 'Forma de obtención: Autoconsumo',
    'p610a3': 'Forma de obtención: Autosuministro',
    'p610a4': 'Forma de obtención: Parte de pago',
    'p610a5': 'Forma de obtención: Regalado por otro hogar',
    'p610a6': 'Forma de obtención: Donado por programa',
    'p610a7': 'Forma de obtención: Otro',
    'p610aa': 'Lugar de compra',
    'p610b': 'Monto total por la compra',
    'p610c2': 'Valor estimado si fue autoconsumo',
    'p610c3': 'Valor estimado si fue autosuministro',
    'p610c4': 'Valor estimado si fue parte de pago',
    'p610c5': 'Valor estimado si fue regalado',
    'p610c6': 'Valor estimado si fue donado',
    'p610c7': 'Valor estimado si fue otro',
    'p610c': 'Valor estimado total',
    'd610b': 'Monto de compra (deflactado)',
    'd610c2': 'Valor autoconsumo (deflactado)',
    'd610c3': 'Valor autosuministro (deflactado)',
    'd610c4': 'Valor parte de pago (deflactado)',
    'd610c5': 'Valor regalado (deflactado)',
    'd610c6': 'Valor donado (deflactado)',
    'd610c7': 'Valor otro (deflactado)',
    'd610c': 'Valor total estimado (deflactado)',
    'i610b': 'Monto de compra (imputado)',
    'i610c2': 'Valor autoconsumo (imputado)',
    'i610c3': 'Valor autosuministro (imputado)',
    'i610c4': 'Valor parte de pago (imputado)',
    'i610c5': 'Valor regalado (imputado)',
    'i610c6': 'Valor donado (imputado)',
    'i610c7': 'Valor otro (imputado)',
    'i610c': 'Valor total estimado (imputado)',
    
    # Submódulo 611: Otros bienes y servicios
    'p611n': 'Otro bien o servicio',
    'p611': '¿Adquirió este bien/servicio en los últimos 3 meses?',
    'p611a1': 'Forma de obtención: Comprado',
    'p611a2': 'Forma de obtención: Autoconsumo',
    'p611a3': 'Forma de obtención: Autosuministro',
    'p611a4': 'Forma de obtención: Parte de pago',
    'p611a5': 'Forma de obtención: Regalado por otro hogar',
    'p611a6': 'Forma de obtención: Donado por programa',
    'p611a7': 'Forma de obtención: Otro',
    'p611aa': 'Lugar de compra',
    'p611b': 'Monto total por la compra',
    'p611c2': 'Valor estimado si fue autoconsumo',
    'p611c3': 'Valor estimado si fue autosuministro',
    'p611c4': 'Valor estimado si fue parte de pago',
    'p611c5': 'Valor estimado si fue regalado',
    'p611c6': 'Valor estimado si fue donado',
    'p611c7': 'Valor estimado si fue otro',
    'p611c': 'Valor estimado total',
    'd611b': 'Monto de compra (deflactado)',
    'd611c2': 'Valor autoconsumo (deflactado)',
    'd611c3': 'Valor autosuministro (deflactado)',
    'd611c4': 'Valor parte de pago (deflactado)',
    'd611c5': 'Valor regalado (deflactado)',
    'd611c6': 'Valor donado (deflactado)',
    'd611c7': 'Valor otro (deflactado)',
    'd611c': 'Valor total estimado (deflactado)',
    'i611b': 'Monto de compra (imputado)',
    'i611c2': 'Valor autoconsumo (imputado)',
    'i611c3': 'Valor autosuministro (imputado)',
    'i611c4': 'Valor parte de pago (imputado)',
    'i611c5': 'Valor regalado (imputado)',
    'i611c6': 'Valor donado (imputado)',
    'i611c7': 'Valor otro (imputado)',
    'i611c': 'Valor total estimado (imputado)',
    
    # Submódulo 612: Equipamiento del hogar
    'p612n': 'Equipo del hogar',
    'p612': '¿Adquirió este equipo en los últimos 12 meses?',
    'p612a1': 'Forma de obtención: Comprado',
    'p612a2': 'Forma de obtención: Autoconsumo',
    'p612a3': 'Forma de obtención: Autosuministro',
    'p612a4': 'Forma de obtención: Parte de pago',
    'p612a5': 'Forma de obtención: Regalado por otro hogar',
    'p612a6': 'Forma de obtención: Donado por programa',
    'p612a7': 'Forma de obtención: Otro',
    'p612aa': 'Lugar de compra',
    'p612b': 'Monto total por la compra',
    'p612c2': 'Valor estimado si fue autoconsumo',
    'p612c3': 'Valor estimado si fue autosuministro',
    'p612c4': 'Valor estimado si fue parte de pago',
    'p612c5': 'Valor estimado si fue regalado',
    'p612c6': 'Valor estimado si fue donado',
    'p612c7': 'Valor estimado si fue otro',
    'p612c': 'Valor estimado total',
    'd612b': 'Monto de compra (deflactado)',
    'd612c2': 'Valor autoconsumo (deflactado)',
    'd612c3': 'Valor autosuministro (deflactado)',
    'd612c4': 'Valor parte de pago (deflactado)',
    'd612c5': 'Valor regalado (deflactado)',
    'd612c6': 'Valor donado (deflactado)',
    'd612c7': 'Valor otro (deflactado)',
    'd612c': 'Valor total estimado (deflactado)',
    'i612b': 'Monto de compra (imputado)',
    'i612c2': 'Valor autoconsumo (imputado)',
    'i612c3': 'Valor autosuministro (imputado)',
    'i612c4': 'Valor parte de pago (imputado)',
    'i612c5': 'Valor regalado (imputado)',
    'i612c6': 'Valor donado (imputado)',
    'i612c7': 'Valor otro (imputado)',
    'i612c': 'Valor total estimado (imputado)',
    
    # Submódulo 613: Beneficiarios de instituciones sin fines de lucro
    'p613n': 'Tipo de institución sin fines de lucro',
    'p613': '¿Recibió ayuda de esta institución en los últimos 3 meses?',
    'p613a1': 'Forma de ayuda: Alimentos',
    'p613a2': 'Forma de ayuda: Vestido',
    'p613a3': 'Forma de ayuda: Medicinas',
    'p613a4': 'Forma de ayuda: Dinero',
    'p613a5': 'Forma de ayuda: Otros',
    'p613b': 'Frecuencia con que recibe la ayuda',
    'p613c': 'Valor estimado de la ayuda recibida',
    'd613c': 'Valor de ayuda (deflactado)',
    'i613c': 'Valor de ayuda (imputado)',
    
    # Submódulo 613H: Alimentos preparados de olla común
    'p613h': '¿Recibió alimentos de olla común en los últimos 15 días?',
    'p613ha1': 'Veces por semana que recibe alimentos',
    'p613hb1': 'Raciones recibidas cada vez',
    'p613hc1': 'Miembros del hogar que consumen',
    'p613hd1a': '¿Pagó por el alimento?',
    'p613hd1b': '¿Pagó por otros conceptos asociados?',
    'p613he3': 'Monto pagado por el alimento',
    'p613he4': 'Monto pagado por otros conceptos',
    'p613hoc': 'Nombre de la olla común',
    'p613he91': 'Razón para recibir ayuda: No tiene trabajo',
    'p613he92': 'Razón para recibir ayuda: Ingresos insuficientes',
    'p613he93': 'Razón para recibir ayuda: Precio económico',
    'p613he94': 'Razón para recibir ayuda: Falta tiempo para cocinar',
    'p613he95': 'Razón para recibir ayuda: Otra razón',
    'd613he3': 'Monto pagado por alimento (deflactado)',
    'd613he4': 'Monto pagado por otros conceptos (deflactado)',
    'i613he3': 'Monto pagado por alimento (imputado)',
    'i613he4': 'Monto pagado por otros conceptos (imputado)',
    
    # === Módulo 700: Programas Sociales ===
    'p700': '¿Algún miembro del hogar es beneficiario de programas sociales?',
    'p701': 'Programa de alimentación (Vaso de Leche)',
    'p702': 'Programa de alimentación (Comedores Populares)',
    'p703': 'Programa de alimentación (Desayunos Escolares)',
    'p704': 'Programa Juntos',
    'p705': 'Programa Pensión 65',
    'p706': 'Programa Contigo',
    'p707': 'Programa Cuna Más',
    'p708': 'Programa Qali Warma',
    'p709': 'Programa Foncodes',
    'p710': 'Otros programas sociales',
    'p711': '¿Recibe transferencias monetarias del gobierno?',
    'p712': 'Monto recibido por transferencias monetarias',
    'p713': 'Frecuencia de las transferencias monetarias',
    'd712': 'Monto de transferencias (deflactado)',
    'i712': 'Monto de transferencias (imputado)',
    
    # === Módulo 800: Participación Ciudadana ===
    'p801': '¿Participó en organizaciones sociales el último año?',
    'p802': 'Tipo de organización en la que participó',
    'p803': 'Frecuencia de participación en reuniones',
    'p804': '¿Ha ocupado algún cargo directivo?',
    'p805': 'Tipo de cargo directivo ocupado',
    'p806a': '¿Participó en actividades comunales el último año?',
    'p806b': 'Tipo de actividad comunal en la que participó',
    
    # === Módulo 2000: Actividad Agropecuaria ===
    'p2000': '¿El hogar realizó actividades agropecuarias?',
    'p2001': 'Superficie agrícola total (hectáreas)',
    'p2002': 'Principales cultivos sembrados',
    'p2003': 'Superficie por tipo de cultivo (hectáreas)',
    'p2004': 'Producción obtenida por cultivo (kg)',
    'p2005': 'Destino de la producción agrícola',
    'p2006': 'Valor de la producción agrícola vendida',
    'p2007': 'Número de cabezas de ganado',
    'p2008': 'Producción pecuaria (litros, kg, docenas)',
    'p2009': 'Destino de la producción pecuaria',
    'p2010': 'Valor de la producción pecuaria vendida',
    'p2011': 'Gastos en insumos agrícolas',
    'p2012': 'Gastos en insumos pecuarios',
    'p2013': 'Mano de obra contratada',
    'p2014': 'Ingreso neto agropecuario',
    'd2006': 'Valor producción agrícola vendida (deflactado)',
    'd2010': 'Valor producción pecuaria vendida (deflactado)',
    'd2011': 'Gastos agrícolas (deflactado)',
    'd2012': 'Gastos pecuarios (deflactado)',
    'd2013': 'Mano de obra (deflactado)',
    'd2014': 'Ingreso neto agropecuario (deflactado)',
    'i2006': 'Valor producción agrícola vendida (imputado)',
    'i2010': 'Valor producción pecuaria vendida (imputado)',
    'i2011': 'Gastos agrícolas (imputado)',
    'i2012': 'Gastos pecuarios (imputado)',
    'i2013': 'Mano de obra (imputado)',
    'i2014': 'Ingreso neto agropecuario (imputado)',
    
    # === Variables de Sumaria ===
    'sumaria_8g': 'Sumaria por 8 grupos de gastos',
    'sumaria_12g': 'Sumaria por 12 grupos de gastos',
    'linea_pobreza': 'Línea de pobreza (S/.)',
    'pobreza': 'Situación de pobreza (1=Pobre, 0=No pobre)',
    'extrema_pobreza': 'Situación de pobreza extrema (1=Extremo, 0=No extremo)',
    'quintil': 'Quintil de ingreso per cápita',
    'deciles': 'Decil de ingreso per cápita',
    'gasto_pc': 'Gasto per cápita mensual (S/.)',
    'ingreso_pc': 'Ingreso per cápita mensual (S/.)',
    'dominio_region': 'Dominio regional ampliado',
    'area': 'Área de residencia (1=Urbano, 2=Rural)',
    'factor07': 'Factor de expansión anual (proyecciones CPV-2007)',
    'facpob07': 'Factor de expansión de población (CPV-2007)',
    'fac500a': 'Factor de expansión para módulo 500A',
    'fac500b': 'Factor de expansión para módulo 500B',
}

# ==============================================================================
# SECCIÓN 2: DICCIONARIO COMPLETO DE ETIQUETAS DE VALORES (VALUE_LABELS)
# Fuente: Diccionario de Datos ENAHO 2023, INEI - Documento completo
# Nota: Todas las claves están en minúsculas para un manejo consistente.
# ==============================================================================
VALUE_LABELS = {
    # === Identificación y Ubicación Geográfica ===
    'dominio': {
        1: 'Costa Norte',
        2: 'Costa Centro',
        3: 'Costa Sur',
        4: 'Sierra Norte',
        5: 'Sierra Centro',
        6: 'Sierra Sur',
        7: 'Selva',
        8: 'Lima Metropolitana'
    },
    'estrato': {
        1: '500,000+ habitantes',
        2: '100,000-499,999 habitantes',
        3: '50,000-99,999 habitantes',
        4: '20,000-49,999 habitantes',
        5: '2,000-19,999 habitantes',
        6: '500-1,999 habitantes',
        7: 'Área Rural Compuesta',
        8: 'Área Rural Simple'
    },
    'periodo': {
        1: 'Primer Periodo',
        2: 'Segundo Periodo',
        3: 'Tercer Periodo',
        4: 'Cuarto Periodo',
        5: 'Quinto Periodo'
    },
    'tipenc': {
        1: 'Selección Automática Urbana',
        3: 'Muestra Panel',
        4: 'Selección Automática Rural',
        5: 'Conteo en Área Rural'
    },
    'result': {
        1: 'Completa',
        2: 'Incompleta',
        3: 'Rechazo',
        4: 'Ausente',
        5: 'Vivienda Desocupada',
        6: 'No se inició Entrevista',
        7: 'Otro'
    },
    'panel': {
        1: 'Sí',
        2: 'No'
    },
    
    # === Módulo 100: Características de la Vivienda y del Hogar ===
    'p101': {
        1: 'Casa independiente',
        2: 'Departamento en edificio',
        3: 'Vivienda en quinta',
        4: 'Vivienda en casa de vecindad',
        5: 'Choza o cabaña',
        6: 'Vivienda improvisada',
        7: 'Local no destinado para habitación',
        8: 'Otro'
    },
    'p102': {
        1: 'Ladrillo o bloque de cemento',
        2: 'Piedra o sillar con cal/cemento',
        3: 'Adobe',
        4: 'Tapia',
        5: 'Quincha (caña con barro)',
        6: 'Piedra con barro',
        7: 'Madera',
        8: 'Triplay/calamina/estera',
        9: 'Otro material'
    },
    'p103a': {
        1: 'Parquet o madera pulida',
        2: 'Láminas asfálticas/vinílicos',
        3: 'Losetas, terrazos o similares',
        4: 'Madera',
        5: 'Cemento',
        6: 'Tierra',
        7: 'Otro material'
    },
    'p103': {
        1: 'Concreto armado',
        2: 'Madera',
        3: 'Tejas',
        4: 'Planchas de calamina/fibra de cemento',
        5: 'Caña o estera con torta de barro/cemento',
        6: 'Triplay/estera/carrizo',
        7: 'Paja, hojas de palmera',
        8: 'Otro material'
    },
    'p104b1': {
        1: 'Sí',
        2: 'No',
        3: 'No sabe'
    },
    'p104b2': {
        1: 'Sí',
        2: 'No',
        3: 'No sabe'
    },
    'p105a': {
        1: 'Alquilada',
        2: 'Propia, totalmente pagada',
        3: 'Propia, por invasión',
        4: 'Propia, comprándola a plazos',
        5: 'Cedida por centro de trabajo',
        6: 'Cedida por otro hogar o institución',
        7: 'Otra forma',
        9: 'Missing value'
    },
    'p106a': {
        1: 'Sí',
        2: 'No',
        3: 'En trámite de titulación',
        9: 'Missing value'
    },
    'p106b': {
        1: 'Sí',
        2: 'No',
        9: 'Missing value'
    },
    'p107b1': {
        1: 'Sí',
        2: 'No'
    },
    'p107c11': {
        0: 'No',
        1: 'Sí'
    },
    'p107c12': {
        0: 'No',
        2: 'Sí'
    },
    'p107c13': {
        0: 'No',
        3: 'Sí'
    },
    'p107c14': {
        0: 'No',
        4: 'Sí'
    },
    'p107c16': {
        0: 'No',
        6: 'Sí'
    },
    'p107c17': {
        0: 'No',
        7: 'Sí'
    },
    'p107c18': {
        0: 'No',
        8: 'Sí'
    },
    'p107c19': {
        0: 'No',
        9: 'Sí'
    },
    'p107c110': {
        0: 'No',
        10: 'Sí'
    },
    'p110': {
        1: 'Red pública dentro de la vivienda',
        2: 'Red pública fuera de la vivienda',
        3: 'Pilón o pileta pública',
        4: 'Camión cisterna',
        5: 'Pozo (agua subterránea)',
        6: 'Manantial o puquio',
        7: 'Otra',
        8: 'Río, acequia, lago, laguna'
    },
    'p110a': {
        1: 'Sí',
        2: 'No'
    },
    'p110a_modificada': {
        1: 'Seguro (≥0.5 mg/Lt)',
        2: 'Inadecuada dosificación (0.1-<0.5 mg/Lt)',
        3: 'Sin cloro (0.0 mg/Lt)',
        9: 'Missing value'
    },
    'p110c': {
        1: 'Sí',
        2: 'No',
        9: 'Missing value'
    },
    'p110f': {
        1: 'Sí',
        2: 'No'
    },
    'p110g': {
        1: 'Empresa prestadora de servicios',
        2: 'Municipalidad',
        3: 'Organización comunal',
        4: 'Camión cisterna',
        5: 'Otro'
    },
    'p111a': {
        1: 'Red pública dentro de la vivienda',
        2: 'Red pública fuera de la vivienda',
        3: 'Letrina con tratamiento',
        4: 'Pozo séptico/tanque séptico/biodigestor',
        5: 'Pozo ciego o negro',
        6: 'Río, acequia, canal o similar',
        7: 'Otra',
        9: 'Campo abierto o al aire libre'
    },
    't111a': {
        1: 'Red pública dentro de la vivienda',
        2: 'Red pública fuera de la vivienda',
        3: 'Letrina con tratamiento',
        4: 'Pozo séptico/tanque séptico/biodigestor',
        5: 'Pozo ciego o negro',
        6: 'Río, acequia, canal o similar',
        7: 'Otra',
        9: 'Campo abierto o al aire libre',
        10: 'Letrina sin tratamiento',
        11: 'Letrina tipo compostera'
    },
    'p112a': {
        1: 'Medidor de uso exclusivo',
        2: 'Medidor de uso colectivo',
        3: 'Otro'
    },
    'p113a': {
        1: 'Electricidad',
        2: 'Gas (balón GLP)',
        3: 'Gas natural (tuberías)',
        5: 'Carbón',
        6: 'Leña',
        7: 'Otro',
        8: 'No cocinan'
    },
    'nb11': {
        0: 'Vivienda adecuada',
        1: 'Vivienda inadecuada'
    },
    'nb12': {
        0: 'Sin hacinamiento',
        1: 'Con hacinamiento'
    },
    'nb13': {
        0: 'Con servicios higiénicos',
        1: 'Sin servicios higiénicos'
    },
    'nb14': {
        0: 'Niños asisten a la escuela',
        1: 'Niños no asisten a la escuela'
    },
    'nb15': {
        0: 'Sin alta dependencia económica',
        1: 'Con alta dependencia económica'
    },
    
    # === Módulo 200: Características de los Miembros del Hogar ===
    'p203': {
        0: 'Panel',
        1: 'Jefe/Jefa',
        2: 'Esposo(a)/compañero(a)',
        3: 'Hijo(a)/Hijastro(a)',
        4: 'Yerno/Nuera',
        5: 'Nieto(a)',
        6: 'Padres/Suegros',
        7: 'Otros parientes',
        8: 'Trabajador del hogar',
        9: 'Pensionista',
        10: 'Otros no parientes',
        11: 'Hermano(a)'
    },
    'p204': {
        1: 'Sí',
        2: 'No'
    },
    'p205': {
        1: 'Sí',
        2: 'No'
    },
    'p206': {
        1: 'Sí',
        2: 'No'
    },
    'p207': {
        1: 'Hombre',
        2: 'Mujer'
    },
    'p209': {
        1: 'Conviviente',
        2: 'Casado(a)',
        3: 'Viudo(a)',
        4: 'Divorciado(a)',
        5: 'Separado(a)',
        6: 'Soltero(a)'
    },
    'p210': {
        1: 'Sí',
        2: 'No'
    },
    'p211a': {
        1: 'Ayudó en negocio familiar',
        2: 'Labores domésticas en otra vivienda',
        3: 'Elaboró productos para venta',
        4: 'Ayudó en chacra/pastoreo',
        5: 'Vendió productos (caramelos, etc.)',
        6: 'Prestó servicios (lavar carros, etc.)',
        7: 'Elaboró productos (chompas, etc.)',
        8: 'Solo quehaceres del hogar',
        9: 'Solo estudiando',
        10: 'Otro'
    },
        't211': {
        1: 'Ayudó en negocio familiar',
        2: 'Labores domésticas en otra vivienda',
        3: 'Elaboró productos para venta',
        4: 'Ayudó en chacra/pastoreo',
        5: 'Vendió productos (caramelos, etc.)',
        6: 'Prestó servicios (lavar carros, etc.)',
        7: 'Elaboró productos (chompas, etc.)',
        8: 'Solo quehaceres del hogar',
        9: 'Solo estudiando',
        10: 'Otro',
        11: 'Vacaciones por estudio',
        12: 'Trabajando'
    },
    
    # === Módulo 300: Educación ===
    'p300a': {
        1: 'Sí',
        2: 'No'
    },
    'p301a': {
        1: 'Público',
        2: 'Privado',
        3: 'Otro'
    },
    'p302': {
        1: 'Inicial',
        2: 'Primaria',
        3: 'Secundaria',
        4: 'Superior no universitaria',
        5: 'Superior universitaria',
        6: 'Básica especial',
        7: 'Básica alternativa',
        8: 'Avanzado (CEBA)',
        9: 'Técnico productivo'
    },
    'p303': {
        1: 'Sí',
        2: 'No'
    },
    'p304': {
        1: 'Sí',
        2: 'No'
    },
    'p305': {
        1: 'Sí',
        2: 'No'
    },
    'p306': {
        1: 'Sí',
        2: 'No'
    },
    'p307': {
        1: 'Sí',
        2: 'No'
    },
    'p308': {
        1: 'Sí',
        2: 'No'
    },
    
    # === Módulo 400: Salud ===
    'p401': {
        1: 'Sí',
        2: 'No'
    },
    'p402': {
        1: 'Sí',
        2: 'No'
    },
    'p403': {
        1: 'SIS',
        2: 'EsSalud',
        3: 'FFAA/PNP',
        4: 'Seguro privado',
        5: 'Otro',
        6: 'Ninguno'
    },
    'p404': {
        1: 'Sí',
        2: 'No'
    },
    'p405': {
        1: 'Sí',
        2: 'No'
    },
    'p406': {
        1: 'Sí',
        2: 'No'
    },
    
    # === Módulo 500: Empleo e Ingresos ===
    'p501': {
        1: 'Sí',
        2: 'No'
    },
    'p502': {
        1: 'Empleado',
        2: 'Independiente',
        3: 'Patrono',
        4: 'Trabajador familiar no remunerado',
        5: 'Otro'
    },
    'p503': {
        1: 'Sí',
        2: 'No'
    },
    'p504': {
        1: 'Sí',
        2: 'No'
    },
    'p505': {
        1: 'Sí',
        2: 'No'
    },
    'p506': {
        1: 'Sí',
        2: 'No'
    },
    'p507': {
        1: 'Sí',
        2: 'No'
    },
    
    # === Módulo 600: Gastos del Hogar ===
    'p601b': {
        1: 'Sí',
        2: 'No',
        9: 'Missing value'
    },
    'p601a1': {
        0: 'Pase',
        1: 'Comprado'
    },
    'p601a2': {
        0: 'Pase',
        1: 'Autoconsumo'
    },
    'p601a3': {
        0: 'Pase',
        1: 'Autosuministro'
    },
    'p601a4': {
        0: 'Pase',
        1: 'Parte de pago'
    },
    'p601a5': {
        0: 'Pase',
        1: 'Regalado por otro hogar'
    },
    'p601a6': {
        0: 'Pase',
        1: 'Donado por programa'
    },
    'p601a7': {
        0: 'Pase',
        1: 'Otro'
    },
    'p601f': {
        1: 'Diario',
        2: 'Interdiario',
        3: 'Semanal',
        4: 'Quincenal',
        5: 'Mensual',
        6: 'Bimestral',
        7: 'Trimestral',
        8: 'Semestral',
        9: 'Dos veces por semana',
        10: 'Tres veces por semana',
        11: 'Cuatro veces por semana',
        12: 'Anual'
    },
    
    # === Módulo 700: Programas Sociales ===
    'p700': {
        1: 'Sí',
        2: 'No'
    },
    'p701': {
        1: 'Sí',
        2: 'No'
    },
    'p702': {
        1: 'Sí',
        2: 'No'
    },
    'p703': {
        1: 'Sí',
        2: 'No'
    },
    'p704': {
        1: 'Sí',
        2: 'No'
    },
    'p705': {
        1: 'Sí',
        2: 'No'
    },
    'p706': {
        1: 'Sí',
        2: 'No'
    },
    'p707': {
        1: 'Sí',
        2: 'No'
    },
    'p708': {
        1: 'Sí',
        2: 'No'
    },
    'p709': {
        1: 'Sí',
        2: 'No'
    },
    'p710': {
        1: 'Sí',
        2: 'No'
    },
    'p711': {
        1: 'Sí',
        2: 'No'
    },
    
    # === Módulo 800: Participación Ciudadana ===
    'p801': {
        1: 'Sí',
        2: 'No'
    },
    'p802': {
        1: 'Organización vecinal',
        2: 'Club de madres',
        3: 'Comité de vaso de leche',
        4: 'Comité de comedor popular',
        5: 'Asociación de productores',
        6: 'Sindicato',
        7: 'Otra'
    },
    'p804': {
        1: 'Sí',
        2: 'No'
    },
    'p806a': {
        1: 'Sí',
        2: 'No'
    },
    
    # === Módulo 2000: Actividad Agropecuaria ===
    'p2000': {
        1: 'Sí',
        2: 'No'
    },
    'p2005': {
        1: 'Venta',
        2: 'Autoconsumo',
        3: 'Trueque',
        4: 'Pago en especie',
        5: 'Otro'
    },
    'p2009': {
        1: 'Venta',
        2: 'Autoconsumo',
        3: 'Trueque',
        4: 'Pago en especie',
        5: 'Otro'
    },
    
    # === Variables de Clasificación ===
    'area': {
        1: 'Urbano',
        2: 'Rural'
    },
    'pobreza': {
        0: 'No pobre',
        1: 'Pobre'
    },
    'extrema_pobreza': {
        0: 'No pobre extremo',
        1: 'Pobre extremo'
    },
    'quintil': {
        1: 'Quintil 1 (más pobre)',
        2: 'Quintil 2',
        3: 'Quintil 3',
        4: 'Quintil 4',
        5: 'Quintil 5 (más rico)'
    },
    'deciles': {
        1: 'Decil 1 (más pobre)',
        2: 'Decil 2',
        3: 'Decil 3',
        4: 'Decil 4',
        5: 'Decil 5',
        6: 'Decil 6',
        7: 'Decil 7',
        8: 'Decil 8',
        9: 'Decil 9',
        10: 'Decil 10 (más rico)'
    }
}

# ==============================================================================
# SECCIÓN 3: FUNCIONES AUXILIARES PARA MANEJO DE DATOS
# ==============================================================================

def get_variable_label(variable_name: str) -> Optional[str]:
    """Devuelve la etiqueta descriptiva de una variable"""
    return VARIABLE_DESCRIPTIONS.get(variable_name.lower())

def get_value_labels(variable_name: str) -> Dict[Union[int, str], str]:
    """Devuelve el diccionario de etiquetas de valores para una variable"""
    return VALUE_LABELS.get(variable_name.lower(), {})

def describe_variable(variable_name: str) -> str:
    """Provee una descripción completa de una variable con sus posibles valores"""
    label = get_variable_label(variable_name)
    value_labels = get_value_labels(variable_name)
    
    description = f"Variable: {variable_name}\nDescripción: {label or 'No encontrada'}"
    if value_labels:
        description += "\nValores posibles:"
        for code, val_label in value_labels.items():
            description += f"\n  {code}: {val_label}"
    
    return description

# ✅ Alias para compatibilidad con el resto del sistema
obtener_descripcion = get_variable_label
def generar_tabla_frecuencias(df: pd.DataFrame, variable: str) -> Optional[pd.DataFrame]:
    """Genera una tabla de frecuencias profesional para una variable usando VALUE_LABELS."""
    if variable not in df.columns:
        return pd.DataFrame({'Error': [f"La variable '{variable}' no está en el dataset."]})
    
    variable_lower = variable.lower()

    if variable_lower not in VALUE_LABELS:
        # Si no hay etiquetas, mostrar conteo simple
        conteo = df[variable].value_counts(dropna=False).reset_index()
        conteo.columns = ['Valor', 'Frecuencia']
        conteo['Porcentaje'] = (conteo['Frecuencia'] / conteo['Frecuencia'].sum() * 100).round(2)
        return conteo

    # Tabla con etiquetas
    conteo = df[variable].value_counts(dropna=False).reset_index()
    conteo.columns = ['Código', 'Frecuencia']
    conteo = conteo.sort_values('Código')

    etiquetas = VALUE_LABELS[variable_lower]
    conteo['Etiqueta'] = conteo['Código'].map(etiquetas).fillna('Sin etiqueta')
    total = conteo['Frecuencia'].sum()
    conteo['Porcentaje'] = (conteo['Frecuencia'] / total * 100).round(2)

    return conteo[['Código', 'Etiqueta', 'Frecuencia', 'Porcentaje']]

# (opcional: puedes imprimir para pruebas)
if __name__ == "__main__":
    print(describe_variable('p101'))
    print(describe_variable('dominio'))

def listar_variables_por_categoria() -> Dict[str, List[str]]:
    """Organiza las variables del diccionario por categorías temáticas."""
    return {
        'Identificación': ['año', 'mes', 'conglome', 'vivienda', 'hogar', 'ubigeo', 'dominio', 'estrato', 'factor07'],
        'Vivienda': ['p101', 'p102', 'p103a', 'p104', 'p105a', 'p106', 'p110', 'p111a', 'p1121', 'p1126', 'p1142', 'p1144', 'p117'],
        'Población': ['p203', 'p207', 'p208a', 'p209'],
        'Educación': ['p300a', 'p301a', 'p301b', 'p301c'],
        'Salud': ['p401', 'p401h', 'p419'],
        'Empleo e Ingresos': ['condocup', 'p501', 'p507', 'p511a', 'p512a', 'p513', 'p521', 'p524', 'i524', 'inghog1d', 'gashog1d'],
        'Programas Sociales': ['p701$02', 'p701$03', 'p710$04', 'p710$05'],
        'Indicadores Clave': ['nbi1', 'nbi2', 'nbi3', 'nbi4', 'nbi5', 'linea', 'pobreza']
    }
