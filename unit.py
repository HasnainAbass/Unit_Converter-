import streamlit as st
import pandas as pd
import time

st.set_page_config(
    page_title="Unit Converter",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

CONVERSIONS = {
    "Length": {
        "Meter": 1,
        "Kilometer": 0.001,
        "Centimeter": 100,
        "Millimeter": 1000,
        "Mile": 0.000621371,
        "Yard": 1.09361,
        "Foot": 3.28084,
        "Inch": 39.3701,
        "Nautical Mile": 0.000539957
    },
    "Weight/Mass": {
        "Kilogram": 1,
        "Gram": 1000,
        "Milligram": 1000000,
        "Metric Ton": 0.001,
        "Pound": 2.20462,
        "Ounce": 35.274,
        "Stone": 0.157473
    },
    "Temperature": {
        "Celsius": "C",
        "Fahrenheit": "F",
        "Kelvin": "K"
    },
    "Area": {
        "Square Meter": 1,
        "Square Kilometer": 0.000001,
        "Square Mile": 3.861e-7,
        "Square Yard": 1.19599,
        "Square Foot": 10.7639,
        "Acre": 0.000247105,
        "Hectare": 0.0001
    },
    "Volume": {
        "Cubic Meter": 1,
        "Liter": 1000,
        "Milliliter": 1000000,
        "Gallon (US)": 264.172,
        "Quart (US)": 1056.69,
        "Pint (US)": 2113.38,
        "Cup": 4226.75
    },
    "Speed": {
        "Meters per Second": 1,
        "Kilometers per Hour": 3.6,
        "Miles per Hour": 2.23694,
        "Knots": 1.94384
    },
    "Time": {
        "Second": 1,
        "Minute": 1/60,
        "Hour": 1/3600,
        "Day": 1/86400,
        "Week": 1/604800,
        "Month": 1/2592000,
        "Year": 1/31536000
    },
    "Digital Storage": {
        "Byte": 1,
        "Kilobyte": 1/1024,
        "Megabyte": 1/1048576,
        "Gigabyte": 1/1073741824,
        "Terabyte": 1/1099511627776
    },
    "Energy": {
        "Joule": 1,
        "Kilojoule": 0.001,
        "Calorie": 0.239006,
        "Kilocalorie": 0.000239006,
        "Watt-hour": 0.000277778,
        "Kilowatt-hour": 0.000000277778
    },
    "Pressure": {
        "Pascal": 1,
        "Kilopascal": 0.001,
        "Bar": 0.00001,
        "PSI": 0.000145038,
        "Atmosphere": 0.00000986923
    }
}

def main():
    
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap');
        
        * {
            font-family: 'Roboto', sans-serif;
        }
        
        h1, h2, h3, .futuristic-text {
            font-family: 'Orbitron', sans-serif;
        }
        
        /* Futuristic container with 3D effect */
        .neo-container {
            background: linear-gradient(145deg, #1a1a1a, #2a2a2a);
            color: #fff;
            border: 1px solid rgba(0, 195, 255, 0.2);
            border-radius: 15px;
            box-shadow: 0 0 15px rgba(0, 195, 255, 0.2),
                       inset 0 0 15px rgba(0, 195, 255, 0.1);
            padding: 2rem;
            position: relative;
            overflow: hidden;
            transform-style: preserve-3d;
            perspective: 1000px;
        }
        
        .neo-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(0,195,255,0.1) 0%, transparent 60%);
            animation: rotate 20s linear infinite;
        }
        
        /* Holographic effect */
        .holographic {
            background: linear-gradient(135deg, 
                rgba(0,195,255,0.1) 0%,
                rgba(0,195,255,0.05) 50%,
                rgba(0,195,255,0.1) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0,195,255,0.2);
            box-shadow: 0 8px 32px 0 rgba(0,195,255, 0.1);
        }
        
        /* 3D Button */
        .stButton>button {
            background: linear-gradient(45deg, #000428, #004e92);
            color: #00c3ff;
            border: 1px solid rgba(0,195,255,0.3);
            padding: 1rem 2rem;
            border-radius: 10px;
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            transform-style: preserve-3d;
            transform: translateZ(0);
            box-shadow: 0 5px 15px rgba(0,195,255,0.2),
                       inset 0 0 15px rgba(0,195,255,0.1);
        }
        
        .stButton>button:hover {
            transform: translateY(-5px) translateZ(10px);
            box-shadow: 0 15px 30px rgba(0,195,255,0.3),
                       inset 0 0 20px rgba(0,195,255,0.2);
            text-shadow: 0 0 10px rgba(0,195,255,0.5);
        }
        
        /* Neon text effect */
        .neon-text {
            color: #fff;
            text-shadow: 0 0 5px #00c3ff,
                        0 0 10px #00c3ff,
                        0 0 20px #00c3ff;
            animation: neon-pulse 2s infinite;
        }
        
        @keyframes neon-pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }
        
        /* Cyber frame */
        .cyber-frame {
            border: 2px solid rgba(0,195,255,0.3);
            position: relative;
            padding: 20px;
            background: rgba(0,0,0,0.7);
        }
        
        .cyber-frame::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            width: 15px;
            height: 15px;
            border-top: 2px solid #00c3ff;
            border-left: 2px solid #00c3ff;
        }
        
        .cyber-frame::after {
            content: '';
            position: absolute;
            bottom: -2px;
            right: -2px;
            width: 15px;
            height: 15px;
            border-bottom: 2px solid #00c3ff;
            border-right: 2px solid #00c3ff;
        }
        
        /* Futuristic inputs */
        .stNumberInput input {
            background: rgba(0,0,0,0.7);
            border: 1px solid rgba(0,195,255,0.3);
            color: #00c3ff;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,195,255,0.1);
        }
        
        .stSelectbox > div {
            background: rgba(0,0,0,0.7) !important;
            border: 1px solid rgba(0,195,255,0.3) !important;
            color: #00c3ff !important;
            border-radius: 8px;
        }
        
        /* Result display with 3D effect */
        .result-display {
            background: linear-gradient(145deg, #000428, #004e92);
            padding: 2rem;
            border-radius: 15px;
            transform-style: preserve-3d;
            transform: perspective(1000px) rotateX(5deg);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            border: 1px solid rgba(0,195,255,0.3);
            position: relative;
        }
        
        .result-display::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, transparent, rgba(0,195,255,0.1));
            pointer-events: none;
        }
        
        /* Scanning line animation */
        @keyframes scan {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(100%); }
        }
        
        .scan-line {
            position: absolute;
            width: 100%;
            height: 2px;
            background: rgba(0,195,255,0.5);
            animation: scan 2s linear infinite;
        }
        
        /* Loading animation */
        .cyber-loading {
            width: 100%;
            height: 4px;
            background: rgba(0,195,255,0.1);
            position: relative;
            overflow: hidden;
            border-radius: 2px;
        }
        
        .cyber-loading::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 30%;
            height: 100%;
            background: #00c3ff;
            animation: cyber-load 1s ease-in-out infinite;
            box-shadow: 0 0 10px #00c3ff;
        }
        
        @keyframes cyber-load {
            0% { left: -30%; }
            100% { left: 100%; }
        }
        
        /* Matrix rain effect */
        @keyframes matrix-rain {
            0% { 
                background-position: 0% 0%;
                opacity: 0.3;
            }
            100% { 
                background-position: 0% 100%;
                opacity: 0.1;
            }
        }
        
        /* Glitch effect */
        @keyframes glitch {
            0% { transform: translate(0); }
            20% { transform: translate(-2px, 2px); }
            40% { transform: translate(-2px, -2px); }
            60% { transform: translate(2px, 2px); }
            80% { transform: translate(2px, -2px); }
            100% { transform: translate(0); }
        }
        
        /* Hologram flicker */
        @keyframes hologram-flicker {
            0% { opacity: 1; }
            50% { opacity: 0.95; }
            52% { opacity: 0.8; }
            54% { opacity: 0.95; }
            100% { opacity: 1; }
        }
        
        /* Glowing border effect */
        .cyber-border {
            position: relative;
        }
        
        .cyber-border::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #00c3ff, transparent, #00c3ff);
            border-radius: 16px;
            z-index: -1;
            animation: border-glow 3s linear infinite;
        }
        
        @keyframes border-glow {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        /* Holographic display */
        .holo-display {
            background: rgba(0, 195, 255, 0.05);
            border: 1px solid rgba(0, 195, 255, 0.2);
            box-shadow: 0 0 20px rgba(0, 195, 255, 0.1);
            animation: hologram-flicker 2s infinite;
        }
        
        /* 3D floating effect */
        .float-3d {
            transform-style: preserve-3d;
            perspective: 1000px;
        }
        
        .float-3d:hover {
            animation: float-rotate 5s;
        }
        
        @keyframes float-rotate {
            0%, 100% { transform: rotateX(0deg) rotateY(0deg); }
            25% { transform: rotateX(2deg) rotateY(2deg); }
            75% { transform: rotateX(-2deg) rotateY(-2deg); }
        }
        
        /* Cyber button enhancements */
        .stButton>button {
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            animation: glitch 0.3s infinite;
        }
        
        .stButton>button::before {
            content: '';
            position: absolute;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(0, 195, 255, 0.2),
                transparent
            );
            transform: translateX(-100%);
            animation: cyber-shine 3s infinite;
        }
        
        @keyframes cyber-shine {
            100% { transform: translateX(100%); }
        }
        
        /* Enhanced result display */
        .result-display {
            position: relative;
            overflow: hidden;
        }
        
        .result-display::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(
                transparent,
                rgba(0, 195, 255, 0.1),
                transparent 30%
            );
            animation: rotate 4s linear infinite;
        }
        
        @keyframes rotate {
            100% { transform: rotate(360deg); }
        }
        
        /* Data stream effect */
        .data-stream {
            position: relative;
            overflow: hidden;
        }
        
        .data-stream::after {
            content: '10100110101';
            position: absolute;
            font-family: 'Courier New', monospace;
            font-size: 10px;
            color: rgba(0, 195, 255, 0.2);
            white-space: nowrap;
            animation: stream 20s linear infinite;
        }
        
        @keyframes stream {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(100%); }
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='neo-container cyber-border float-3d'>
            <div class='scan-line' style='left: 0;'></div>
            <div class='data-stream'></div>
            <h1 class='neon-text' style='font-size: 3rem; text-align: center;'>
               Unit Convertify
            </h1>
            <p style='text-align: center; color: #00c3ff; font-family: "Orbitron", sans-serif;'>
                VERSION 3.0 // ADVANCED CONVERSION SYSTEM
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='cyber-frame holographic holo-display float-3d'>
            <div class='scan-line' style='left: 0;'></div>
            <div class='data-stream'></div>
            <h2 class='neon-text' style='text-align: center; margin-bottom: 2rem;'>
                SELECT PARAMETERS
            </h2>
    """, unsafe_allow_html=True)
    
    left_col, main_col, right_col = st.columns([1, 2, 1])
    
    with main_col:
       
        st.markdown("""
            <div class='converter-box neumorphic floating-card'>
                <h2 style='color: #1a73e8; font-size: 1.5rem; margin-bottom: 2rem; text-align: center;'>
                    Select Your Conversion
                </h2>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='category-header'>Select Conversion Category</div>", unsafe_allow_html=True)
        category = st.selectbox("", list(CONVERSIONS.keys()), key="category")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("<p style='color: #1E88E5; font-weight: 600; font-size: 1.1rem;'>From</p>", unsafe_allow_html=True)
            from_unit = st.selectbox("", list(CONVERSIONS[category].keys()), key="from")
            value = st.number_input("Enter Value", value=0.0, key="value", 
                                  help="Enter the value you want to convert")
            
        with col2:
            st.markdown("<p style='color: #1E88E5; font-weight: 600; font-size: 1.1rem;'>To</p>", unsafe_allow_html=True)
            to_unit = st.selectbox("", list(CONVERSIONS[category].keys()), key="to")
        
        if st.button("INITIATE CONVERSION ⚡"):
            with st.spinner(''):
                st.markdown("""
                    <div class='cyber-loading'></div>
                """, unsafe_allow_html=True)
                time.sleep(0.5)
                if category == "Temperature":
                    result = convert_temperature(value, from_unit, to_unit)
                else:
                    result = convert_units(value, from_unit, to_unit, CONVERSIONS[category])
            
                st.markdown(f"""
                    <div class='result-display cyber-border holo-display float-3d'>
                        <div class='scan-line'></div>
                        <div class='data-stream'></div>
                        <div style='text-align: center;'>
                            <p style='color: #00c3ff; font-family: "Orbitron", sans-serif;'>
                                INPUT: {value} {from_unit}
                            </p>
                            <h3 class='neon-text' style='font-size: 2.5rem; margin: 1rem 0;'>
                                {result:.6f}
                            </h3>
                            <p style='color: #00c3ff; font-family: "Orbitron", sans-serif;'>
                                OUTPUT: {to_unit}
                            </p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with st.expander("ℹ️ About this converter"):
        st.markdown("""
        <div style='background: linear-gradient(145deg, #ffffff, #f5f7fa); padding: 1.5rem; border-radius: 15px;'>
            <h4 style='color: #1E88E5; font-size: 1.3rem; margin-bottom: 1rem;'>Available Conversion Categories:</h4>
            <div class='category-card'>
                <ul style='list-style-type: none; padding-left: 0; margin: 0;'>
                    <li class='category-item' style='margin: 0.8rem 0;'><span class='category-icon'>📏</span> <strong>Length:</strong> Common distance measurements</li>
                    <li class='category-item' style='margin: 0.8rem 0;'><span class='category-icon'>⚖️</span> <strong>Weight/Mass:</strong> Mass and weight units</li>
                    <li class='category-item' style='margin: 0.8rem 0;'><span class='category-icon'>🌡️</span> <strong>Temperature:</strong> Celsius, Fahrenheit, and Kelvin</li>
                    <li class='category-item' style='margin: 0.8rem 0;'><span class='category-icon'>📐</span> <strong>Area:</strong> Land and space measurements</li>
                    <li class='category-item' style='margin: 0.8rem 0;'><span class='category-icon'>🧊</span> <strong>Volume:</strong> Liquid and space volume</li>
                    <li class='category-item' style='margin: 0.8rem 0;'><span class='category-icon'>🏃</span> <strong>Speed:</strong> Various velocity units</li>
                    <li class='category-item' style='margin: 0.8rem 0;'><span class='category-icon'>⏰</span> <strong>Time:</strong> Time duration units</li>
                    <li class='category-item' style='margin: 0.8rem 0;'><span class='category-icon'>💾</span> <strong>Digital Storage:</strong> Computer memory units</li>
                    <li class='category-item' style='margin: 0.8rem 0;'><span class='category-icon'>⚡</span> <strong>Energy:</strong> Power and energy units</li>
                    <li class='category-item' style='margin: 0.8rem 0;'><span class='category-icon'>🎈</span> <strong>Pressure:</strong> Force per unit area</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class='neo-container' style='margin-top: 2rem;'>
            <div class='scan-line'></div>
            <p style='text-align: center; color: #00c3ff; font-family: "Orbitron", sans-serif;'>
                ENGINEERED BY HASNAIN Abass // SYSTEM ACTIVE
            </p>
        </div>
    """, unsafe_allow_html=True)

def convert_units(value, from_unit, to_unit, conversion_dict):
    base_value = value / conversion_dict[from_unit]
    return base_value * conversion_dict[to_unit]

def convert_temperature(value, from_unit, to_unit):
    if from_unit == "Fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    else:
        celsius = value
    if to_unit == "Fahrenheit":
        return (celsius * 9/5) + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15
    else:
        return celsius

if __name__ == "__main__":
    main() 
