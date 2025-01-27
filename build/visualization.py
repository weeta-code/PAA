import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from subprocess import run
import numpy as np
from dataclasses import dataclass
from typing import Dict

@dataclass
class SystemParameters:
    f: float  # Natural frequency
    zeta: float  # Damping ratio
    r: float  # Response factor

class SecondOrderSimulation:
    def __init__(self):
        self.build_dir = Path(__file__).parent.absolute()
        self.executable = str(self.build_dir / 'AnimationExample')
        self.params_file = str(self.build_dir / 'system_params.txt')
        self.data_file = str(self.build_dir / 'animation_data.csv')
        
        self.default_params = {
            'fast': SystemParameters(f=2.0, zeta=0.5, r=0.8),
            'smooth': SystemParameters(f=0.8, zeta=1.0, r=0.5),
            'over': SystemParameters(f=1.5, zeta=0.3, r=1.2)
        }

    def run_simulation(self, parameters: Dict[str, SystemParameters]) -> pd.DataFrame:
        with open(self.params_file, 'w') as f:
            for params in parameters.values():
                f.write(f"{params.f} {params.zeta} {params.r}\n")

        run([self.executable], check=True)
        
        return pd.read_csv(self.data_file)

def create_response_plot(data: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['Frame'], y=data['Fast'],
        name='Fast System', line=dict(color='#1f77b4', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=data['Frame'], y=data['Smoothed'],
        name='Smooth System', line=dict(color='#2ca02c', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=data['Frame'], y=data['Overshoot'],
        name='Overshoot System', line=dict(color='#ff7f0e', width=2)
    ))
    
    fig.update_layout(
        title='Second-Order System Responses',
        xaxis_title='Frame',
        yaxis_title='Position',
        template='plotly_white',
        height=600,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

def main():
    st.set_page_config(
        page_title="Second-Order System Analysis",
        layout="wide"
    )
    
    st.title("Second-Order System Response Analysis")
    
    simulation = SecondOrderSimulation()
    
    col1, col2, col3 = st.columns(3)
    
    # Based off System Dynamics Theory
    f_range = (0.1, 5.0)
    zeta_range = (0.1, 2.0)
    r_range = (0.1, 2.0)
    
    current_params = {}
    
    # Fast System Controls
    with col1:
        st.subheader("Fast System Parameters")
        fast_f = st.slider("Natural Frequency (Hz)", 
                          min_value=f_range[0], max_value=f_range[1], 
                          value=simulation.default_params['fast'].f,
                          key='fast_f',
                          help="Higher values lead to faster oscillations")
        fast_zeta = st.slider("Damping Ratio", 
                            min_value=zeta_range[0], max_value=zeta_range[1],
                            value=simulation.default_params['fast'].zeta,
                            key='fast_zeta',
                            help="Controls oscillation decay rate")
        fast_r = st.slider("Response Factor",
                          min_value=r_range[0], max_value=r_range[1],
                          value=simulation.default_params['fast'].r,
                          key='fast_r',
                          help="Affects system's velocity response")
        current_params['fast'] = SystemParameters(fast_f, fast_zeta, fast_r)

    # Smooth System Controls
    with col2:
        st.subheader("Smooth System Parameters")
        smooth_f = st.slider("Natural Frequency (Hz)",
                           min_value=f_range[0], max_value=f_range[1],
                           value=simulation.default_params['smooth'].f,
                           key='smooth_f')
        smooth_zeta = st.slider("Damping Ratio",
                              min_value=zeta_range[0], max_value=zeta_range[1],
                              value=simulation.default_params['smooth'].zeta,
                              key='smooth_zeta')
        smooth_r = st.slider("Response Factor",
                           min_value=r_range[0], max_value=r_range[1],
                           value=simulation.default_params['smooth'].r,
                           key='smooth_r')
        current_params['smooth'] = SystemParameters(smooth_f, smooth_zeta, smooth_r)

    # Overshoot System Controls
    with col3:
        st.subheader("Overshoot System Parameters")
        over_f = st.slider("Natural Frequency (Hz)",
                          min_value=f_range[0], max_value=f_range[1],
                          value=simulation.default_params['over'].f,
                          key='over_f')
        over_zeta = st.slider("Damping Ratio",
                            min_value=zeta_range[0], max_value=zeta_range[1],
                            value=simulation.default_params['over'].zeta,
                            key='over_zeta')
        over_r = st.slider("Response Factor",
                          min_value=r_range[0], max_value=r_range[1],
                          value=simulation.default_params['over'].r,
                          key='over_r')
        current_params['over'] = SystemParameters(over_f, over_zeta, over_r)

    try:
        data = simulation.run_simulation(current_params)
        fig = create_response_plot(data)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("System Analysis")
        col1, col2, col3 = st.columns(3)
        
        for system, data_col in zip(['Fast', 'Smoothed', 'Overshoot'], [col1, col2, col3]):
            with data_col:
                st.write(f"**{system} System Metrics**")
                series = data[system]
                metrics = {
                    "Peak Value": f"{series.max():.2f}",
                    "Settling Time (frames)": f"{np.where(np.abs(series - series.iloc[-1]) < 0.05 * 5.0)[0][0]}",
                    "Overshoot (%)": f"{((series.max() - 5.0) / 5.0 * 100):.1f}%"
                }
                for metric, value in metrics.items():
                    st.metric(metric, value)
                
    except Exception as e:
        st.error(f"Simulation Error: {str(e)}")

if __name__ == "__main__":
    main()