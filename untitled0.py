import streamlit as st
import numpy as np
import pandas as pd

# ==============================================================================
# IMPORTACIÓN DE TUS LIBRERÍAS REALES
# ==============================================================================
try:
    from libreria_funciones_proyecto1 import calcular_imc
    from libreria_clases_proyecto1 import Empleado
except ImportError as e:
    st.error(f"Error al importar las librerías: {e}. Asegúrate de haber subido los archivos correctos a tu GitHub.")

# ==============================================================================
# CONFIGURACIÓN DEL MENÚ LATERAL (OBLIGATORIO)
# ==============================================================================
st.sidebar.title("Navegación")
opcion = st.sidebar.selectbox(
    "Selecciona una sección:", 
    ["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"]
)

# ==============================================================================
# 1. SECCIÓN: HOME
# ==============================================================================
if opcion == "Home":
    st.title("Proyecto Módulo 1 - Fundamentos de Programación")
    st.subheader("Especialización en Python for Analytics")
    st.write("**Módulo:** Módulo 1 - Python Fundamentals")
    st.write("**Estudiante:** Alvaro Rivera Espinoza")
    st.write("**Año:** 2026")
    st.markdown("---")
    st.markdown("### Descripción del Proyecto")
    st.write("Esta aplicación interactiva web fue desarrollada en Streamlit e integra "
             "estructuras de datos (listas, diccionarios), librerías de analítica (NumPy, Pandas), "
             "modularización con funciones externas y Programación Orientada a Objetos (POO).")

# ==============================================================================
# 2. SECCIÓN: EJERCICIO 1 (Flujo de Caja con Listas)
# ==============================================================================
elif opcion == "Ejercicio 1":
    st.title("Ejercicio 1 - Flujo de Caja con Listas")
    st.markdown("Registre y controle sus movimientos financieros de ingresos y gastos.")
    
    if 'movimientos' not in st.session_state:
        st.session_state.movimientos = []
        
    concepto = st.text_input("Concepto o Descripción del movimiento:")
    tipo = st.selectbox("Tipo de movimiento:", ["Ingreso", "Gasto"])
    valor = st.number_input("Valor ($):", min_value=0.0, step=50.0)
    
    if st.button("Agregar movimiento"):
        if concepto:
            st.session_state.movimientos.append({"Concepto": concepto, "Tipo": tipo, "Valor": valor})
            st.success("¡Movimiento registrado con éxito!")
        else:
            st.warning("Por favor, introduce un concepto válido.")
        
    if st.session_state.movimientos:
        st.markdown("#### Historial de Movimientos")
        df_movs = pd.DataFrame(st.session_state.movimientos)
        st.dataframe(df_movs)
        
        total_ingresos = sum(m['Valor'] for m in st.session_state.movimientos if m['Tipo'] == 'Ingreso')
        total_gastos = sum(m['Valor'] for m in st.session_state.movimientos if m['Tipo'] == 'Gasto')
        saldo_final = total_ingresos - total_gastos
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Ingresos", f"${total_ingresos:,.2f}")
        col2.metric("Total Gastos", f"${total_gastos:,.2f}")
        col3.metric("Saldo Final", f"${saldo_final:,.2f}")
        
        if saldo_final >= 0:
            st.success(f"🟢 Flujo a Favor: Tu saldo actual es positivo.")
        else:
            st.error(f"🔴 Flujo en Contra: Tus gastos superan a tus ingresos.")

# ==============================================================================
# 3. SECCIÓN: EJERCICIO 2 (Registro con NumPy y DataFrames)
# ==============================================================================
elif opcion == "Ejercicio 2":
    st.title("Ejercicio 2 - Registro con NumPy y DataFrames")
    st.markdown("Formulario de registro de inventario de productos utilizando vectores de NumPy.")
    
    if 'productos_lista' not in st.session_state:
        st.session_state.productos_lista = []
        
    prod_nombre = st.text_input("Nombre del Producto:")
    prod_categoria = st.selectbox("Categoría:", ["Tecnología", "Alimentos", "Oficina", "Otros"])
    prod_precio = st.number_input("Precio Unitario ($):", min_value=0.0, step=5.0)
    prod_cantidad = st.number_input("Cantidad en Stock:", min_value=0, step=1)
    
    if st.button("Registrar Producto"):
        if prod_nombre:
            total_calculado = prod_precio * prod_cantidad
            st.session_state.productos_lista.append([prod_nombre, prod_categoria, prod_precio, prod_cantidad, total_calculado])
            st.success("¡Producto registrado en el inventario!")
        else:
            st.warning("Por favor, introduce el nombre del producto.")
            
    if st.session_state.productos_lista:
        np_data = np.array(st.session_state.productos_lista, dtype=object)
        df_productos = pd.DataFrame(
            np_data, 
            columns=["Producto", "Categoría", "Precio Unitario", "Cantidad", "Total Inventario"]
        )
        st.markdown("#### Matriz de Inventario Actualizada")
        st.dataframe(df_productos)

# ==============================================================================
# 4. SECCIÓN: EJERCICIO 3 (Funciones desde Librería Externa + Histórico)
# ==============================================================================
elif opcion == "Ejercicio 3":
    st.title("Ejercicio 3 - Funciones desde Librería Externa")
    st.markdown("Cálculo del Índice de Masa Corporal (IMC) usando la función externa `calcular_imc` con registro histórico.")
    
    if 'historico_imc' not in st.session_state:
        st.session_state.historico_imc = []
        
    peso = st.number_input("Peso Actual (Kilogramos):", min_value=1.0, max_value=250.0, value=70.0)
    altura = st.number_input("Altura (Metros):", min_value=0.5, max_value=2.5, value=1.70)
    
    if st.button("Ejecutar Función IMC"):
        try:
            res_dict = calcular_imc(peso_kg=peso, altura_m=altura)
            st.markdown("---")
            st.subheader("Resultado de la Ejecución:")
            st.metric(label="IMC Calculado", value=f"{res_dict['imc']:.2f}")
            st.info(f"Clasificación asignada por la función: **{res_dict['clasificacion']}**")
            
            st.session_state.historico_imc.append({
                "Peso (kg)": peso,
                "Altura (m)": altura,
                "IMC Obtenido": round(res_dict['imc'], 2),
                "Clasificación": res_dict['clasificacion']
            })
        except Exception as e:
            st.error(f"Error en la ejecución de la función: {e}")
            
    if st.session_state.historico_imc:
        st.markdown("#### Histórico de Ejecuciones del Módulo")
        st.dataframe(pd.DataFrame(st.session_state.historico_imc))

# ==============================================================================
# 5. SECCIÓN: EJERCICIO 4 (Clases y Operaciones CRUD completas)
# ==============================================================================
elif opcion == "Ejercicio 4":
    st.title("Ejercicio 4 - Operaciones CRUD con Clases")
    st.markdown("Sistema de administración de Personal utilizando Programación Orientada a Objetos (Clase `Empleado`).")
    
    if 'db_empleados' not in st.session_state:
        st.session_state.db_empleados = {}
        
    tab_crear, tab_leer, tab_actualizar, tab_eliminar = st.tabs(["Crear", "Leer (Visualizar)", "Actualizar", "Eliminar"])
    
    with tab_crear:
        st.subheader("Registrar nuevo empleado")
        emp_nombre = st.text_input("Nombre Completo del Empleado:")
        emp_salario = st.number_input("Salario Base ($):", min_value=1.0, value=1000.0, step=100.0)
        emp_bono = st.number_input("Porcentaje de Bono (%):", min_value=0.0, max_value=100.0, value=5.0)
        emp_desc = st.number_input("Porcentaje de Descuento (%):", min_value=0.0, max_value=100.0, value=2.0)
        
        if st.button("Guardar Objeto Empleado"):
            if emp_nombre:
                try:
                    nuevo_empleado = Empleado(emp_nombre, emp_salario, emp_bono, emp_desc)
                    st.session_state.db_empleados[emp_nombre] = nuevo_empleado
                    st.success(f"¡Objeto para '{emp_nombre}' creado e insertado con éxito!")
                except Exception as e:
                    st.error(f"Error al instanciar la clase: {e}")
            else:
                st.warning("El nombre es un campo obligatorio.")
                
    with tab_leer:
        st.subheader("Visualización de registros (POO)")
        if st.session_state.db_empleados:
            lista_datos = []
            for nombre, obj in st.session_state.db_empleados.items():
                lista_datos.append({
                    "Nombre": obj.nombre,
                    "Salario Base": f"${obj.salario_base:,.2f}",
                    "Bono ($)": f"${obj.calcular_bono():,.2f}",
                    "Descuentos ($)": f"${obj.calcular_descuento():,.2f}",
                    "Salario Neto": f"${obj.calcular_salario_neto():,.2f}"
                })
            st.dataframe(pd.DataFrame(lista_datos))
        else:
            st.info("No hay empleados registrados actualmente.")
            
    with tab_actualizar:
        st.subheader("Modificar parámetros de un empleado")
        if st.session_state.db_empleados:
            emp_selec = st.selectbox("Selecciona el empleado a modificar:", list(st.session_state.db_empleados.keys()), key="upd_sel")
            obj_modificar = st.session_state.db_empleados[emp_selec]
            
            nuevo_salario = st.number_input("Nuevo Salario Base ($):", min_value=1.0, value=float(obj_modificar.salario_base))
            nuevo_bono = st.number_input("Nuevo Porcentaje de Bono (%):", min_value=0.0, max_value=100.0, value=float(obj_modificar.porcentaje_bono))
            nuevo_desc = st.number_input("Nuevo Porcentaje de Descuento (%):", min_value=0.0, max_value=100.0, value=float(obj_modificar.porcentaje_descuento))
            
            if st.button("Actualizar Registro"):
                obj_modificar.salario_base = nuevo_salario
                obj_modificar.porcentaje_bono = nuevo_bono
                obj_modificar.porcentaje_descuento = nuevo_desc
                st.success(f"¡Los datos de {emp_selec} han sido modificados!")
        else:
            st.info("No hay registros para modificar.")
            
    with tab_eliminar:
        st.subheader("Dar de baja un registro")
        if st.session_state.db_empleados:
            emp_eliminar = st.selectbox("Selecciona el empleado a eliminar:", list(st.session_state.db_empleados.keys()), key="del_sel")
            if st.button("Eliminar Permanentemente", type="primary"):
                del st.session_state.db_empleados[emp_eliminar]
                st.success(f"El registro de '{emp_eliminar}' ha sido borrado del sistema.")
                st.rerun()
        else:
            st.info("No hay registros para eliminar.")
