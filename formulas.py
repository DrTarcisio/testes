# +
import streamlit as st

st.set_page_config(layout="wide", page_title="Fórmulas")

# Adicionar CSS para esconder a barra lateral
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# +
col0_1, col0_2, col0_3, col0_4 = st.columns([3,1,1,1])

with col0_1:
    st.title("Peroperatório")
with col0_2:
    try:
        peso = st.number_input("Peso (Kg)", f"{st.session_state.peso}")
    except:
        peso = st.number_input("Peso (Kg)", placeholder="em kg", value=None)
with col0_3:
    try:
        altura = st.number_input("Altura (cm)", f"{int(st.session_state.altura)}")
    except:
        altura = st.number_input("Altura (cm)", placeholder="em cm", value=None)
with col0_4:
    try:
        sexo = st.text_input("Sexo", f"{int(st.session_state.sexo)}")
    except:
        sexo = st.selectbox("Sexo", ['F','M'])         

if peso and altura:
        asc = (int(peso)*int(altura)/3600)**(0.5)
        st.write(f"ASC = {round(asc,2)}")

if peso and altura and sexo:
        if sexo.capitalize() == 'F':

            pm = int(altura)-105
            pmc = pm+0.3*(int(peso)-pm)
            if int(pm)>int(peso):
                pmc = peso
        else:
            pm = int(altura)-100
            pmc = pm+0.3*(int(peso)-pm)
            if int(pm)>int(peso):
                pmc = peso        

if peso and altura and sexo:
        f"PMC = {round(pmc)} kg"
        
tab1, tab2 , tab3= st.tabs(["Cálculos", "CEC", "Outros"])

# +
# TAB 1
with tab1:
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        if peso and altura and sexo:
            if sexo.capitalize() == 'F':

                pm = int(altura)-105
                pmc = pm+0.3*(int(peso)-pm)
                if int(pm)<int(peso):
                    pmc = peso

            else:
                pm = int(altura)-100
                pmc = pm+0.3*(int(peso)-pm)
                if int(pm)<int(peso):
                    pmc = peso

        with st.expander('mcg/kg/min --> mL/h'):
            mcgkgmin = st.number_input("mcg/kg/min --> mL/h", placeholder="mcg/kg/min", value= None, label_visibility='hidden')
            concentracao = st.number_input("Concentração", placeholder="mcg/mL", value=None, step=1)
            if mcgkgmin and concentracao and pmc:
                f"{mcgkgmin} mcg/kg/min = {round(mcgkgmin*pmc*60/concentracao,1)} mL/h"

    with col2:
        pass
    
    with col3:
        pass


# TAB 2
with tab2:
    col2a, col2b, col2c, col2d = st.columns([0.8,0.8,0.5,1],gap='large')
    
# Col2a        
    with col2a: 
        gasometria = [['pH',7.35,7.45],
                      ['PaCO2',30,45],
                      ['PaO2',60,280],
                      ['Htc',23,45],
                      ['Na+',130,150],
                      ['K+',3,5],
                      ['Cl-', 98,107],
                      ['Ca2+',0.97,1.3],
                      ['Glicose',85,180],
                      ['Lactato',0.3,2.2],
                      ['hCO3-',22,26],
                      ['BE-b',-3,3],
                      ['SatO2',0.92,0.99],
                      ['Hb',7,15]]
        gaso_dict1 = {i[0] : [i[1], i[2]] for i in gasometria[0:7] if len(i)>1}
        gaso_dict2 = {i[0] : [i[1], i[2]] for i in gasometria[7:] if len(i)>1}

        st.subheader("Gasometria")
        for k,v in gaso_dict1.items():
            st.number_input(k, placeholder=f'{v[0]} - {v[1]}',key=k, value=None)
    
# Col2b
    with col2b:
        for k,v in gaso_dict2.items():
            st.number_input(k, placeholder=f'{v[0]} - {v[1]}',key=k, value=None)
        satvO2 = st.number_input('SatVO2',placeholder='0.75', value=None)

# Col2c
    with col2c:
        st.subheader('CEC')

        fluxo_bomba = st.number_input("Fluxo de Bomba", placeholder='L/min', value=None)
        

        if st.session_state['Hb'] and st.session_state['SatO2'] and satvO2:
            cao2 = 1.34*st.session_state['Hb']*st.session_state['SatO2'] #arterial
            cvo2 = 1.34*st.session_state['Hb']*satvO2 #venoso

            do2_cec = 10*fluxo_bomba*cao2
            if do2_cec < 290:
                f'DO2 = :red[{round(do2_cec)}]'
            else:
                f'DO2 = {round(do2_cec)}'
            
            if cao2 and cvo2:
                er_o2 = (cao2 - cvo2)/cao2
                if er_o2 < 0.25:
                    f'ERO2 = :red[{round(er_o2*100)}%]'
                else:
                    f'ERO2 = {round(er_o2*100)}%'

            vo2_cec = 10*fluxo_bomba*cvo2 # VR: 3,5ml/kg/min
            vo2_cec2 = 10*fluxo_bomba*(cao2-cvo2)

            if fluxo_bomba:
                f'VO2 = {round(vo2_cec)}'
                f'VO2 = {round(vo2_cec2)}'

        st.write('')

        pam = st.number_input('PAM', placeholder='mmHg', value=None)
        pvc = st.number_input('PVC', placeholder='mmHg', value=None)     

        if peso and altura and sexo:
            do2_min = 2.5*pmc
            if fluxo_bomba:
                ic = fluxo_bomba/asc
                f'IC = {round(ic,2)}'

        if pam and pvc and fluxo_bomba:
            rvs = ((pam-pvc)/fluxo_bomba*80)
            f'RVS = {round(rvs)}'

# Col2d
    with col2d:
        if st.session_state['Na+'] and st.session_state['hCO3-'] and st.session_state['Cl-']:
            anion_gap = st.session_state['Na+'] - (st.session_state['hCO3-'] + st.session_state['Cl-'])
            if anion_gap >12:
                f"AG = :red[{anion_gap}]"
            else:
                f"AG = {anion_gap}"
        
        if st.session_state.pH and st.session_state.pH < 7.35:
            if st.session_state['hCO3-'] and st.session_state['hCO3-']<22:
                ac_comp = st.session_state['PaCO2']*1.5+8
                if ac_comp<35:
                    f':red[Acidose Metabólica Descompensada]'
                elif ac_comp>45:
                    f':red[Acidose Mista]'
                else:
                    f':red[Acidose Respiratória Compensada]'
                    
        elif st.session_state.pH and st.session_state.pH > 7.45:
            if st.session_state['hCO3-']>26:
                ac_comp = st.session_state['PaCO2']+15
                if ac_comp<35:
                    f':red[Alcalose Metabólica Mista]'
                elif ac_comp>45:
                    f':red[Alcalose Metabólica Descompensada]'
                else:
                    f':red[Alcalose Metabólica Compensada]'

        for a,b in gaso_dict1.items() and gaso_dict2.items():
            if st.session_state[f'{a}'] and (st.session_state[f'{a}'] > b[1] or st.session_state[f'{a}']<b[0]):
                f"{a}: :red[{st.session_state[f'{a}']}]"

# TAB 3
with tab3:
    col3a, col3b = st.columns(2,gap='medium')

# Col3a        
    with col3a:
        st.markdown(f'''Fórmulas

CaO2 = 1,36 * Hb * SatO2 + (PaO2 * 0,0034) 

DC = VS * FC 

DO2 = DC * CaO2    

VO2 = DC * CvO2    [VR: 3,5 ml/kg/min]

VO2 = DC * (CaO2 - CvO2)

O2ER = DO2/VO2 ou (CaO2 - CvO2)/CaO2    [VR: < 25%]

RVS = (PAM - PVC)/ DC * 80 

DO2 = 10 * pumpflow * CaO2


                    ''')

    with col3b:
        st.markdown(f'''Resumo de Artigos:

        DO2 (>290) e ERO2 (<25%) é melhor que IC e SvO2. (RR 1.18)



                    ''')
# -

# !streamlit run formulas.py


