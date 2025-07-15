from datetime import datetime
import numpy_financial as npf

def calcular_rendimiento_simple(monto, tasa_anual, fecha_vencimiento_str):
    fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, "%Y-%m-%d")
    hoy = datetime.today()
    años = (fecha_vencimiento - hoy).days / 365
    ganancia = monto * (tasa_anual / 100) * años
    valor_final = monto + ganancia
    return round(valor_final, 2), round(ganancia, 2), round(años, 2)

def calcular_tir(precio, tasa_cupon, anios):
    if anios <= 0:
        return None

    flujo_caja = [-precio]
    for i in range(1, int(anios) + 1):
        flujo_caja.append(tasa_cupon)
    flujo_caja[-1] += 100  # Amortización al final

    tir = npf.irr(flujo_caja)
    if tir is None:
        return None
    return round(tir * 100, 2)

def es_cupon_cero_estrategico(bono, tir, anios):
    return (
        bono["Tasa"] == 0 and
        bono["Precio"] < 60 and
        anios <= 3 and
        tir >= 70
    )