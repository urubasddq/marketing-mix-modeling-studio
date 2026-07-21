import sys
import os
from nicegui import ui
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple

# Import the model engine
from model import MarketingMixModel

# ==========================================
# Phase 2a: Synthetic Data Generator
# ==========================================
def generate_synthetic_data(periods: int = 104) -> pd.DataFrame:
    """Generates 2 years of weekly dummy marketing and sales data."""
    dates = pd.date_range(start='2022-01-01', periods=periods, freq='W')
    
    # Generate base sales (increasing trend + random noise)
    base_sales = np.linspace(10000, 25000, periods) + np.random.normal(0, 500, periods)
    
    # Generate media spend with varying trends and seasonality
    np.random.seed(42)
    data = {
        'date': dates,
        'tv_spend': np.random.uniform(5000, 15000, periods) + np.sin(np.arange(periods)/4)*2000,
        'digital_spend': np.random.uniform(2000, 8000, periods) + np.arange(periods)*50,
        'radio_spend': np.random.uniform(1000, 4000, periods)
    }
    
    df = pd.DataFrame(data)
    
    # Define true underlying elasticities (impact)
    coeff_tv = 0.3
    coeff_digital = 0.5
    coeff_radio = 0.15
    
    # Add non-linear impact (simulating adstock/saturation)
    # For generation, we use a simple lagged moving average to simulate carryover
    df['tv_adstocked'] = df['tv_spend'].rolling(4).mean().fillna(df['tv_spend'])
    
    # Generate base revenue
    df['revenue'] = (
        base_sales +
        (df['tv_adstocked'] * coeff_tv) +
        (df['digital_spend'] * coeff_digital) +
        (df['radio_spend'] * coeff_radio)
    )
    
    return df

# Initialize Data and Model
CHANNEL_COLS = ['tv_spend', 'digital_spend', 'radio_spend']
df_data = generate_synthetic_data()

# Define Model Hyperparameters (In a real app, these are tuned)
adstock_params = {
    'tv_spend': 0.8,      # High carryover
    'digital_spend': 0.3, # Low carryover
    'radio_spend': 0.5    # Medium carryover
}
saturation_params = {
    'tv_spend': (10000, 1.5), # (half-max, slope)
    'digital_spend': (5000, 2.0),
    'radio_spend': (2500, 1.2)
}

mmm_engine = MarketingMixModel(channels=CHANNEL_COLS)
mmm_engine.fit(df_data, 'revenue', adstock_params, saturation_params)


# ==========================================
# Phase 2b: NiceGUI Dashboard Layout
# ==========================================

# Apply "Data Science Studio" Aesthetic
ui.dark_mode().enable()

# Custom CSS for slate/teal/amber theme inspired by image_0.png
ui.add_head_html('''
    <style>
        :root {
            --q-color-primary: #14b8a6; /* Teal */
            --q-color-secondary: #f59e0b; /* Amber */
            --q-dark: #1e293b; /* Slate Background */
            --q-dark-page: #0f172a; /* Deep Slate Card Background */
        }
        body { background-color: var(--q-dark-page); }
        .nicegui-card {
            background-color: var(--q-dark);
            border-radius: 12px;
            border: 1px solid #334155;
        }
        .chiclet {
            background: rgba(20, 184, 166, 0.1);
            border: 1px solid var(--q-color-primary);
            color: var(--q-color-primary);
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8em;
        }
    </style>
''')

# State variables for simulation
current_allocation = {k: df_data[k].mean() for k in CHANNEL_COLS}
simulation_result_label = ui.label()

def update_simulation():
    """Callback to run prediction when sliders change."""
    # Create a single-row dataframe for prediction
    sim_df = pd.DataFrame([current_allocation])
    
    # Run through model preprocessing and prediction
    prediction = mmm_engine.predict(sim_df, adstock_params, saturation_params)
    
    # Update the KPI card
    # We need to access the label by reference or update globally. 
    # For simplicity in this example, we update a global ref.
    total_revenue_kpi.set_text(f"${prediction[0]:,.0f}")
    
    # Trigger ECharts update (not implemented in this snippet, but conceptually required)

def create_kpi_card(title: str, value: str, icon: str, delta: str = None):
    with ui.card().classes('w-full p-5'):
        with ui.row().classes('items-center justify-between no-wrap'):
            ui.label(title).classes('text-slate-400 font-medium')
            ui.icon(icon).classes('text-teal-400 text-2xl')
        ui.label(value).classes('text-white text-4xl font-bold mt-2')
        if delta:
             ui.label(delta).classes('text-amber-400 text-sm mt-1')

# --- Main Layout ---
with ui.column().classes('w-full p-6 lg:p-10 gap-8'):
    
    # Header
    with ui.row().classes('w-full items-center justify-between'):
        ui.label('Marketing Mix Modeling Studio').classes('text-3xl font-bold text-white')
        with ui.row().classes('items-center gap-4'):
             ui.label('Powered by Scikit-Learn & NiceGUI').classes('text-slate-500')
             ui.avatar(color='teal').props('icon=science')

    # KPI Row
    with ui.row().classes('w-full grid grid-cols-1 md:grid-cols-3 gap-6'):
        total_revenue_kpi = ui.label(f"${df_data['revenue'].mean():,.0f}") # Global ref for update
        create_kpi_card('Baseline Predicted Revenue', total_revenue_kpi.text, 'attach_money')
        create_kpi_card('Overall ROI', '4.2x', 'trending_up', '+12% vs Last Year')
        create_kpi_card('Model R-Squared', f"{mmm_engine.pipeline.named_steps['ridge'].score(mmm_engine.preprocess_features(df_data[CHANNEL_COLS], adstock_params, saturation_params), df_data['revenue']):.2f}", 'check_circle')

    # Charts and Simulation Row
    with ui.row().classes('w-full grid grid-cols-1 xl:grid-cols-3 gap-6'):
        
        # Apache ECharts Decomposition (Placeholder setup)
        with ui.card().classes('xl:col-span-2 p-6 min-h-[400px]'):
            ui.label('Revenue Decomposition Waterfall').classes('text-xl font-semibold text-white mb-4')
            # ECharts component implementation goes here (requires passing transformed data)
            # For now, just a placeholder
            with ui.element('div').classes('w-full h-full bg-slate-900 rounded flex items-center justify-center'):
                ui.label('Apache ECharts Visualization').classes('text-slate-600')

        # Budget Simulator
        with ui.card().classes('p-6'):
            ui.label('Budget Allocation Simulator').classes('text-xl font-semibold text-white mb-2')
            ui.label('Adjust weekly spend to see predicted revenue impact.').classes('text-slate-400 mb-6')
            
            with ui.column().classes('gap-6'):
                for channel in CHANNEL_COLS:
                    channel_name = channel.replace('_', ' ').title()
                    
                    # Slider config
                    max_val = df_data[channel].max() * 2
                    
                    with ui.column().classes('gap-1'):
                        with ui.row().classes('justify-between'):
                            ui.label(channel_name).classes('text-white')
                            ui.label().bind_text_from(current_allocation, channel, backward=lambda v: f"${v:,.0f}")
                        
                        slider = ui.slider(min=0, max=max_val, step=100, value=current_allocation[channel]) \
                            .props('color=teal')
                        
                        # Bind slider to state and trigger update
                        def create_setter(c):
                            return lambda e: (current_allocation.update({c: e.value}), update_simulation())
                        slider.on_value_change(create_setter(channel))

    # Model Coefficients Table
    with ui.row().classes('w-full'):
         with ui.card().classes('w-full p-6'):
            ui.label('Channel Regression Weights (Scaled Impact)').classes('text-xl font-semibold text-white mb-4')
            
            # Convert coefficients to a display dataframe
            coef_df = pd.DataFrame({
                'Channel': [c.replace('_', ' ').title() for c in mmm_engine.channels],
                'Coefficient Weight': [mmm_engine.coefficients[c] for c in mmm_engine.channels],
                'Status': ['High Impact', 'Medium Impact', 'Low Impact'] # Placeholder logic
            })
            
            table = ui.table(columns=[
                {'name': 'Channel', 'label': 'Channel', 'field': 'Channel', 'align': 'left'},
                {'name': 'Coefficient Weight', 'label': 'Weight', 'field': 'Coefficient Weight', 'sortable': True},
                {'name': 'Status', 'label': 'Evaluation', 'field': 'Status', 'align': 'center'}
            ], rows=coef_df.to_dict('records')).classes('bg-slate-800 text-white')
            
            # Style the status column
            table.add_slot('body-cell-Status', '''
                <q-td :props="props">
                    <span :class="props.value === 'High Impact' ? 'chiclet' : 'chiclet opacity-50'">
                        {{ props.value }}
                    </span>
                </q-td>
            ''')

ui.run(title="MMM Studio")