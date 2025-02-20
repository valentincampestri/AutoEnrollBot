from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import re
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()

sesionIniciada = False
while not sesionIniciada:
    username = input('Ingresa el nombre de usuario para iniciar sesión (no es el mail):\n') 
    password = input('Ingresa la contraseña para iniciar sesión:\n')
    url = f"https://{username}:{password}@inscripcionespia.uade.edu.ar/InscripcionClaseBuscar.aspx?param=wC2JlH3T61E%3d-P0lkU2Vzc2lvbj0scGFyYW1BbHVtSWQ9MzI2MjE4LHBhcmFtTml2QWNhZD0xMzAscGFyYW1BbmlvQ2FsZW5kYXJpbz0yMDI0LHBhcmFtQ3VhdHJpbWVzdHJlPTU5NyxwYXJhbVNlZGU9MSxwYXJhbVRpcG9BZG1pbj0zNDAzMCxwYXJhbVRpcG9JbnZvY2Fkb3I9MixwYXJhbVByaVZlej0xLHBhcmFtT2ZyZWNpbWllbnRvPQ%3d%3d"
    driver.get(url)
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_btnSeleccionarMaterias")))
        sesionIniciada = True
    except Exception as e:
        print("Usuario/contraseña incorrectos. Inténtalo de nuevo.\n")


print("A continuación deberá ingresar todos los datos de la materia de uno en uno (en caso de querer inscribirse a más de una). Primero se le pedirá el código, luego el turno y finalmente se le preguntará si quiere inscribirse en días específicos. Luego se le preguntará si quiere ingresar otra materia, y repetirá el proceso. MÁXIMO 6 MATERIAS.")

materias = []
dias_elegidos = []
finalizacion = -1
turnos = ["MAÑANA", "TARDE", "NOCHE", "INTENSIVO", "VIRTUAL"]
sedes = ["MONSERRAT", "BELGRANO", "RECOLETA", "PINAMAR", "UADE VIRTUAL"]
numero_a_dia = {
    1: "LU",
    2: "MA",
    3: "MI",
    4: "JU",
    5: "VI"
}

dias_ocupados_por_turno = {
    "MAÑANA": [], 
    "TARDE": [],
    "NOCHE": [],
    "INTENSIVO": [],
    "VIRTUAL": []
}


while len(materias) < 4 and finalizacion != 2:
    codigo = input('Ingrese el código de la materia con puntos (ejemplo: 3.2.241):\n')
    
    if not re.match(r'^\d\.\d\.\d{3}$', codigo):
        print("Error: Formato incorrecto de materia. Debe ser X.X.XXX donde X es un número. Por favor, vuelva a ingresar.\n")
        continue
    
    sede_existente = False
    while not sede_existente:
        sede = input("1- Montserrat\n2- Belgrano\n3- Recoleta\n4- Pinamar\n5- Virtual\nIngrese el número de la sede preferida: ")
        if sede.isdigit() and 1 <= int(sede) <= len(sedes):
            sede_elegida = sedes[int(sede) - 1]
            sede_existente = True
        else:
            print("\nSeleccione un número de sede válido (1-5).\n")
    
    if sede_elegida == "UADE VIRTUAL":
        turno_elegido = "VIRTUAL"
    else:
        turno_existente = False
        while not turno_existente:
            turno = input("1- Mañana\n2- Tarde\n3- Noche\n4- Intensivo\nIngrese el número del turno preferido: ")
            if turno.isdigit() and 1 <= int(turno) <= len(turnos)-1:
                turno_elegido = turnos[int(turno) - 1]
                turno_existente = True
            else:
                print("\nSeleccione un número de turno válido (1-4).\n")

    dias_elegidos = []

    if turno_elegido != "Intensivo":
        print("\nSi desea ser inscripto cualquier día de la semana, ingrese 0.\nSi desea ser inscripto en un día en específico, inregese algún número de los de abajo. El orden en que envía estos días (si es que envía varios), determinará su prioridad. Si desea ingresar más de 1 día (es decir, ser inscripto en cualquiera de las opciones), ingresarlos separados SOLAMENTE con una coma (","). EL MÁXIMO ES DE 4 DÍAS.")
        dias_existentes = False
        while not dias_existentes:
            dia = input("0- Ninguno\n1- Lunes\n2- Martes\n3- Miércoles\n4- Jueves\n5- Viernes\nIngrese su selección: ")
            
            if dia == '0':
                dias_elegidos = list(numero_a_dia.values())
            else:
                diasSplit = dia.split(",")
                validos = True
                temp_dias_elegidos = []

                for d in diasSplit:
                    if d.strip().isdigit() and 1 <= int(d.strip()) <= len   (numero_a_dia):
                        dia_elegido = numero_a_dia[int(d.strip())]
                        if dia_elegido not in temp_dias_elegidos:
                            temp_dias_elegidos.append(dia_elegido)
                        else:
                            print(f"Ya ha seleccionado {dia_elegido}. Seleccione otro.")
                            validos = False
                            break
                    else:
                        validos = False
                        break

                if not validos:
                    print('\nSeleccione uno o varios (separados solo por ",") números de días válidos (1-5). Solo presione 0 si no desea elegir ninguno.\n')
                elif len(temp_dias_elegidos) + len(dias_elegidos) > 4:
                    print("Ha seleccionado más de 4 días en total. Por favor, vuelva a ingresar.")
                else:
                    dias_elegidos.extend(temp_dias_elegidos)
                    if len(dias_elegidos) <= 4:
                        dias_existentes = True
    else:
        dias_elegidos = list(numero_a_dia.values())
                    

    materias.append({"codigo": codigo, "sede": sede_elegida, "turno": turno_elegido, "dias": dias_elegidos.copy()})

    while True:
        finalizacion = input("Presione 1 si desea ingresar más materias.\nPresione 2 si no desea ingresar más materias.\nElección: ")
        
        if finalizacion.isdigit() and int(finalizacion) in [1, 2]:
            finalizacion = int(finalizacion)
            break
        else:
            print("La opción ingresada es inválida. Por favor, vuelva a ingresar.\n")

            

print("\nMaterias ingresadas:")
for materia in materias:
    print(f"Código: {materia['codigo']}, Sede: {materia['sede']}, Turno: {materia['turno']}, Días: {', '.join(materia['dias'])}")
 
btn_buscar = driver.find_element(By.ID, "ContentPlaceHolder1_btnSeleccionarMaterias")
btn_buscar.click()

time.sleep(random.uniform(2, 4))

while len(materias) > 0:
    for materia in materias:
        codigo = materia['codigo']
        turno_elegido = materia['turno']
        dias_elegidos = materia['dias']
        sede = materia['sede']

        try:
            fila = driver.find_element(By.XPATH, "//td[@class='colCodigo' and text()='{}']/..".format(codigo.strip()))
            checkbox = fila.find_element(By.XPATH, ".//td[@class='colAcciones']/span/input[@type='checkbox']")
            checkbox.click()

        except NoSuchElementException:
            print(f"La materia '{codigo}' no está disponible en la web de inscripción.")
            materias.remove(materia)
            continue
        
        time.sleep(random.uniform(2, 4))

        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        time.sleep(random.uniform(2, 4))

        select_turno = driver.find_element(By.ID, "ContentPlaceHolder1_cboTurno")
        select_turno.send_keys(turno_elegido)
        btn_chico = driver.find_element(By.CLASS_NAME, "btn_chico")
        btn_chico.click()
        time.sleep(random.uniform(2, 4))

        dias_clase = driver.find_elements(By.XPATH, ".//td[@class='tdDiaResaltado']/following-sibling::input")

        inscripcion_exitosa = False
        for dia in dias_elegidos:
            try:
                elementos_resaltados = driver.find_elements(By.CLASS_NAME, 'tdDiaResaltado')

                for elemento in elementos_resaltados:
                    hidden_input = elemento.find_element(By.XPATH, ".//following-sibling::input[@type='hidden']")
                    name_value = hidden_input.get_attribute("name")

                    if name_value.endswith(dia) or dias_elegidos == []:
                        dia_id_builder = hidden_input.get_attribute("id")
                        dia_id = dia_id_builder.split("_")[-1]

                        sede_element = driver.find_element(By.XPATH, f"//span[@id='ContentPlaceHolder1_rptMateriaClases_grdClases_0_grdResultados_0_lblSede_{dia_id}']")
                        sede_text = sede_element.text.strip()

                        regimen_element = driver.find_element(By.XPATH, f"//span[@id='ContentPlaceHolder1_rptMateriaClases_grdClases_0_grdResultados_0_lblRegimenCursadaDescripcion_{dia_id}']")
                        regimen_text = regimen_element.text.strip()

                        if sede_text == sede:
                            if materia['turno'] in ["MAÑANA", "TARDE", "NOCHE"]:
                                if regimen_text != "SEMANAL":
                                    continue
                            elif materia['turno'] == "VIRTUAL":
                                if "UADE VIRTUAL" not in sede_text:
                                    continue
                            elif materia['turno'] == "INTENSIVO":
                                if regimen_text != "INTENSIVO":
                                    continue
                            else:
                                continue

                            btn_carrito_id = f"ContentPlaceHolder1_rptMateriaClases_grdClases_0_grdResultados_0_btnCarritoAlta_{dia_id}"

                            try:
                                btn_carrito = driver.find_element(By.ID, btn_carrito_id)
                                btn_carrito.click()
                                print(f"Se ha agregado al carrito la clase para el día {dia}.")

                                if sede_text == "PINAMAR" and regimen_text == "SEMANAL":
                                    button = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(@class, 'ui-button') and contains(@class, 'ui-state-default') and contains(@class, 'ui-corner-all') and contains(@class, 'ui-button-text-only') and .//span[text()='Sí, agregar']]")))
                                    button.click()

                                WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.ID, "ContentPlaceHolder1_btnConfirmarCarrito")))
                                btn_confirmar_carrito = driver.find_element(By.ID, "ContentPlaceHolder1_btnConfirmarCarrito")
                                btn_confirmar_carrito.click()

                                WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.ID, "ContentPlaceHolder1_chkTerminos")))
                                btn_aceptar_terminos = driver.find_element(By.ID, "ContentPlaceHolder1_chkTerminos")
                                btn_aceptar_terminos.click()
                                print(f"Inscripción realizada con éxito para la materia {codigo}, en el turno {turno_elegido} los días {dia}, sede {sede}")

                                dias_ocupados_por_turno[turno_elegido].append(dia)
                        
                                for m in materias:
                                    if m != materia and m['turno'] == turno_elegido:
                                        if dia in m['dias']:
                                            m['dias'].remove(dia)
                                        if m['dias'] == []:
                                            materias.remove(m)

                                materias.remove(materia)
                                driver.get(url)
                                btn_buscar = driver.find_element(By.ID, "ContentPlaceHolder1_btnSeleccionarMaterias")
                                btn_buscar.click()
                                inscripcion_exitosa = True    
                                break
                            except NoSuchElementException:
                                continue

            except Exception as e:
                print(f"Error al procesar el día '{dia}':", e)
                
        if not inscripcion_exitosa:
            print(f"No hay vacante para la materia {codigo}, turno {turno_elegido} en la sede {materia['sede']}, para los días solicitados.")

            btn_buscar = driver.find_element(By.ID, "ContentPlaceHolder1_btnSeleccionarMaterias")
            btn_buscar.click()
            fila = driver.find_element(By.XPATH, "//td[@class='colCodigo' and text()='{}']/..".format(codigo.strip()))
            checkbox = fila.find_element(By.XPATH, ".//td[@class='colAcciones']/span/input[@type='checkbox']")
            checkbox.click()
        time.sleep(random.uniform(6, 8))

driver.quit()