from fastapi import FastAPI
from pydantic import BaseModel
import math


# python -m uvicorn main:app --reload
# http://127.0.0.1:8000



app = FastAPI()

class ZapataDeConcretro(BaseModel):
    peso: int
    dado: int
    rT: int
    fY: int
    fF: int
    
class propuestas(BaseModel):
    propuesta1: int
    propuesta2: int
    pC: int
    ladoSqrt: int
    fC: int
    fR: int
    
class varillaP(BaseModel):
    propuesta1: int
    propuesta2: int
    pC: int
    ladoSqrt: int
    fC: int
    fR: int
    fY: int
    fF: int
    
@app.get("/")
def index():
    dato = 45
    dato2 = "string"
    dato3 = 1000
    data = {
        "dato" : dato,
        "dato 2" : dato2,
        "dato 3" : dato3
    }
    return {"message": "alaverga", "data": data}

@app.post("/zapata1/datos")
def datosDeZapata(dato: ZapataDeConcretro):
    pesoEstimado = dato.peso * .1
    cargaTotal1 = dato.peso + pesoEstimado
    pU = 1.4 * cargaTotal1
    areaNecesaria = pU / dato.rT
    ladoSqrt = math.sqrt(areaNecesaria)
    pC = 1.4 * (dato.peso/areaNecesaria)
    return {"message": f'presion de contacto contra el suelo {pC}', "data" : pC}

@app.post("/zapata1/fallaDePunzonamiento")
def datosDeZapata(dato: propuestas):
    seccionCritica = dato.pC * ((dato.ladoSqrt ** 2) + ((dato.propuesta1 + dato.propuesta2)**2))
    areaDeSeccionCritica = ((4 * (dato.propuesta2 * 100)) * ((dato.propuesta1 * 100 ) + (dato.propuesta2 * 100)))
    esfuerzoCortante = ((seccionCritica * 1000) / areaDeSeccionCritica)
    fCR = (dato.fR * math.sqrt(dato.fR * dato.fC))
    uR = fCR 
    uU = esfuerzoCortante
    if uR > uU:
        print()
        return {"message": f'si paso uwu {uR}', "data": uR}
    else :
        print('no paso owo ', uU)
        return {"message": f'no paso owo {uU}'}
    
@app.post("/zapata1/MomentoDeSeccionCritica")
def datosDeZapata(dato: varillaP):
    mSC = dato.pC * ((dato.ladoSqrt * ((dato.ladoSqrt - dato.propuesta1)**2))/8)
    areaDeEsfuerzo = (mSC * 10**5) / (dato.fF * 0.9 * (dato.propuesta2 * 100) * dato.fY)
    varillas = [3,4,5,6,8,9,10]
    areasDeVarillas = [0.71,1.27,1.99,2.87,5.07,6.45,8.19]
    valorDeVarilla = 0
    diferenciaSuperior = 0
    varillaDeUso = 0
    areaDeVarilla = 0
    
    for index, varilla in enumerate(varillas):
        formula = (dato.ladoSqrt * 100) * (areasDeVarillas[index] / areaDeEsfuerzo)
        diferencia = formula - areaDeEsfuerzo
        if diferencia > 0:
            diferenciaSuperior = round(formula)
            areaDeVarilla = areasDeVarillas[index]
            varillaDeUso = varilla
            break

    i = diferenciaSuperior
    temp = diferenciaSuperior
    cuantillaDeRefuerzo= 0
    
    while i > 0:
        if (temp % 5) == 0:
            cuantillaDeRefuerzo = (areaDeVarilla / (temp * (dato.propuesta2 * 100)))
            refuerzoMinPorFlexion = (.7*(math.sqrt(dato.fC))) / dato.fY

            if cuantillaDeRefuerzo > refuerzoMinPorFlexion and temp > 15:
                break
            temp = temp - 1
            i = i - 1
        else:
            temp = temp - 1
            i = i - 1
    
    data = {
        "difSuperior": temp,
        "varillaDeUso": varillaDeUso,
        "areaDeVarilla":areaDeVarilla,
        "cuantillaDeRefuerzo": cuantillaDeRefuerzo,
        "refuerzoMinPorFlexion": refuerzoMinPorFlexion
    }
     
    return {
        "message":f"'la diferiencia superior es {temp} con varillas del {varillaDeUso} y medida de {areaDeVarilla} ,cuantillaDeRefuerzo {cuantillaDeRefuerzo} es mayor al refuerzo minimo por flexion {refuerzoMinPorFlexion}",
        "data": data
        }



    # print('la diferiencia superior es ', temp, "con varillas del ",varillaDeUso , "y medida de ", areaDeVarilla)  

    # print('cuantillaDeRefuerzo ', cuantillaDeRefuerzo, ' es mayor al refuerzo minimo por flexion ', refuerzoMinPorFlexion )

        



