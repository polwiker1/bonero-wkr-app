import streamlit as st
import pandas as pd
import plotly.express as px
from utils import (
    calcular_rendimiento_simple,
    calcular_tir,
    es_cupon_cero_estrategico
)

st.set_page_config(page_title="Bonero WKR – Simulador Educativo", layout="wide")
with st.sidebar:
    st.image("logo_wkr.png", width=180)
    st.markdown("<h3 style='color:#0b84ff;'>Bonero WKR</h3>", unsafe_allow_html=True)
    st.caption("💼 Plataforma educativa de Wiker Blockchain")
    st.markdown("---")

    st.markdown("📲 **Conectá con Pablo:**", unsafe_allow_html=True)
    st.markdown("""
        <div style='font-size:14px; line-height:1.6;'>
            📞 <strong>WhatsApp:</strong> <a href='https://wa.me/543544561784' target='_blank'>+54 3544 561784</a><br>
            🔗 <strong>LinkedIn:</strong> <a href='https://www.linkedin.com/in/pabloamodio/' target='_blank'>Pablo Amodio</a><br>
            📸 <strong>Instagram:</strong> <a href='https://www.instagram.com/wikerblockchain/' target='_blank'>@wikerblockchain</a><br>
            💻 <strong>GitHub:</strong> <a href='https://github.com/polwiker1' target='_blank'>polwiker1</a><br>
            📘 <strong>Facebook:</strong> <a href='https://www.facebook.com/wikerblockchainpablo' target='_blank'>Wiker Blockchain Pablo</a>
        </div>
    """, unsafe_allow_html=True)
# Cargar dataset base
df = pd.read_csv("bonos.csv")

# Estructura de pestañas
tab1, tab2, tab3 = st.tabs(["📊 Simulador", "📡 Visualizador", "🎓 Aula Copilot"])

# ---------- TAB 1: Simulador ----------
with tab1:
    st.title("🧠 Bonero WKR • Centro de Aprendizaje en Bonos")
    st.caption("Una iniciativa educativa de Wiker Blockchain para democratizar la inversión")
    st.markdown("**Powered by Wiker Blockchain (WKR)** 💡")

    col1, col2 = st.columns(2)
    with col1:
        bono_1 = st.selectbox("Elegí el primer bono", df["Nombre"], key="bono1")
    with col2:
        bono_2 = st.selectbox("Elegí el segundo bono", df["Nombre"], key="bono2")

    monto = st.number_input("Ingresá el monto a invertir (ARS)", min_value=1000, step=500)

    def mostrar_info(bono_nombre):
        bono_info = df[df["Nombre"] == bono_nombre].iloc[0]
        valor_final, ganancia, anios = calcular_rendimiento_simple(
            monto, bono_info["Tasa"], bono_info["Fecha_vencimiento"]
        )
        tir_estimada = calcular_tir(bono_info["Precio"], bono_info["Tasa"], anios)

        st.subheader(f"🔹 {bono_nombre}")
        st.markdown(f"**Tasa de Cupón:** {bono_info['Tasa']}%")
        st.markdown(f"**Plazo estimado:** {anios:.2f} años")
        st.markdown(f"**Ganancia estimada:** ${ganancia:,.2f}")
        st.markdown(f"**Valor a vencimiento:** ${valor_final:,.2f}")
        st.markdown(f"**TIR estimada:** {tir_estimada:.2f}%")

        if es_cupon_cero_estrategico(bono_info, tir_estimada, anios):
            st.markdown("💥 **Cupón Cero Estratégico:** bono con alta proyección de recuperación. Ideal mantener hasta vencimiento.")

    col3, col4 = st.columns(2)
    with col3:
        mostrar_info(bono_1)
    with col4:
        mostrar_info(bono_2)
st.markdown("---")
st.markdown("""
<div style='background-color:#f5f7fa; padding:15px; border-left:5px solid #0b84ff; border-radius:10px; font-size:14px;'>
    ⚠️ <strong>Disclaimer educativo:</strong><br>
    Esta herramienta tiene fines exclusivamente pedagógicos. No constituye recomendación financiera, asesoramiento profesional ni sugerencia de inversión específica.<br><br>
    <strong>Autor:</strong> Pablo wkr<br>
    <strong>Rol:</strong> Asesor Productor Financiero 2.0 registrado<br>
    <strong>Formación:</strong> Curso especializado en Bonos Argentinos – Academia IOL<br>
</div>
""", unsafe_allow_html=True)
# ---------- TAB 2: Visualizador BYMA con TIR real ----------
from datetime import datetime

with tab2:
    st.header("🔄 Visualizador BYMA – Carga de CSV con TIR real")

    uploaded = st.file_uploader("📁 Subí tu archivo CSV exportado de BYMA", type="csv")
    if uploaded:
        df_byma = pd.read_csv(uploaded)
        hoy = datetime.today()

        df_byma["Años"] = df_byma["Fecha_vencimiento"].apply(
            lambda x: (pd.to_datetime(x) - hoy).days / 365
        )
        df_byma = df_byma[df_byma["Años"] > 0].reset_index(drop=True)

        tir_list = []
        for _, row in df_byma.iterrows():
            try:
                tir = calcular_tir(row["Precio"], row["Tasa"], row["Años"])
            except:
                tir = None
            tir_list.append(tir)
        df_byma["TIR (%)"] = tir_list

        df_byma = df_byma.sort_values("Años")
        st.subheader("📋 Bonos ordenados por vencimiento")
        st.dataframe(df_byma[["Nombre", "Precio", "Tasa", "Años", "TIR (%)"]], use_container_width=True)

        if df_byma["TIR (%)"].dropna().empty:
            st.warning("⚠️ No hay bonos con TIR válida para graficar.")
        else:
            st.subheader("📊 TIR comparativa por bono")
            fig = px.bar(
                df_byma.dropna(subset=["TIR (%)"]),
                x="Nombre",
                y="TIR (%)",
                color="Años",
                color_continuous_scale="Blues",
                text="TIR (%)"
            )
            fig.update_layout(
                yaxis_title="TIR (%)",
                xaxis_title="Bono",
                height=400,
                title="Rendimiento proyectado según datos de BYMA"
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📎 Subí un archivo .csv exportado desde BYMA para comenzar.")
st.markdown("---")
st.markdown("""
<div style='background-color:#f5f7fa; padding:15px; border-left:5px solid #0b84ff; border-radius:10px; font-size:14px;'>
    ⚠️ <strong>Disclaimer educativo:</strong><br>
    Esta herramienta tiene fines exclusivamente pedagógicos. No constituye recomendación financiera, asesoramiento profesional ni sugerencia de inversión específica.<br><br>
    <strong>Autor:</strong> Pablo wkr<br>
    <strong>Rol:</strong> Asesor Productor Financiero 2.0 registrado<br>
    <strong>Formación:</strong> Curso especializado en Bonos Argentinos – Academia IOL<br>
</div>
""", unsafe_allow_html=True)
# ---------- TAB 3: Aula Copilot ----------
with tab3:
    st.title("🎓 Aula Copilot Interactiva")

    st.header("📘 ¿Qué es un bono?")
    st.write("Un bono es un préstamo que vos le hacés a un gobierno o empresa. A cambio, te devuelven el dinero más un interés.")

    st.header("💥 ¿Qué es un bono cupón cero?")
    st.write("Es un bono que no paga intereses cada año. Se compra con descuento y paga todo junto al vencimiento.")

    st.header("📈 ¿Qué es la TIR?")
    st.write("Es la tasa de rentabilidad estimada si mantenés el bono hasta que venza. Cuanto más alta, más gana tu inversión.")

    st.markdown("---")

    st.header("🧮 Simulación educativa")
    monto = st.slider("Elegí un monto hipotético a invertir (ARS)", 1000, 100000, 10000, 5000)
    tasa = st.slider("Tasa anual (%)", 0.0, 120.0, 70.0)
    plazo = st.slider("Plazo en años", 0.5, 5.0, 2.0, 0.5)

    ganancia = monto * (tasa / 100) * plazo
    total = monto + ganancia
    st.success(f"Al invertir ${monto:,.0f} a {tasa}% durante {plazo} años, ganarías ${ganancia:,.0f}. Total estimado: ${total:,.0f}")

    st.markdown("---")

    st.header("🔗 Referencias recomendadas")
    st.markdown("- [📚 Glosario del BCRA](https://www.bcra.gob.ar/BCRAyVos/Glosario.asp)")
    st.markdown("- [📝 Cursos gratuitos de Educación Financiera (EfEd)](https://efinanciera.educ.ar)")
    st.markdown("- [📊 Finanzas Públicas (Ministerio de Economía)](https://www.argentina.gob.ar/economia/finanzas)")
    st.markdown("- [📦 GitHub - Bonos y renta fija](https://github.com/topics/bonds)")

    st.markdown("---")

    st.header("💬 Hablemos del bono")
    bono_seleccionado = st.text_input("Escribí el nombre de un bono (ej: AE24, DICP)...")
    if bono_seleccionado:
        st.info(f"🔍 Analizando {bono_seleccionado.upper()}... Este bono podría tener una TIR atractiva si cotiza bajo la par. Revisá su cupón, vencimiento y precio actual para estimar su rendimiento real.")