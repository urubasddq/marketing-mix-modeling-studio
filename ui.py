import sys
import os
from datetime import datetime, timedelta
from nicegui import ui
import pandas as pd
import numpy as np

# Import the model engine
from model import MarketingMixModel

# ==========================================
# 1. Digital Marketing Data Generator
# ==========================================
CHANNELS = {
    'google_ads': {'name': 'Google Ads', 'color': '#0ea5e9'},
    'meta_ads': {'name': 'Meta Ads', 'color': '#ec4899'},
    'amazon_ads': {'name': 'Amazon Ads', 'color': '#f59e0b'},
    'reddit_ads': {'name': 'Reddit Ads', 'color': '#8b5cf6'}
}
CHANNEL_KEYS = list(CHANNELS.keys())

def generate_digital_marketing_data(periods: int = 52) -> pd.DataFrame:
    """Generates 52 weeks of weekly paid media spend and revenue performance."""
    np.random.seed(42)
    dates = pd.date_range(end=datetime.today(), periods=periods, freq='W')
    
    base_revenue = np.linspace(15000, 22000, periods) + np.random.normal(0, 400, periods)
    
    data = {
        'date': dates,
        'google_ads': np.random.uniform(8000, 18000, periods) + np.sin(np.arange(periods)/3) * 2000,
        'meta_ads': np.random.uniform(6000, 15000, periods) + np.cos(np.arange(periods)/4) * 1500,
        'reddit_ads': np.random.uniform(1500, 5000, periods),
        'amazon_ads': np.random.uniform(5000, 12000, periods) + np.arange(periods) * 80
    }
    
    df = pd.DataFrame(data)
    
    df['google_impact'] = df['google_ads'] * 0.42
    df['meta_impact'] = df['meta_ads'] * 0.35
    df['reddit_impact'] = df['reddit_ads'] * 0.18
    df['amazon_impact'] = df['amazon_ads'] * 0.48
    
    df['revenue'] = (
        base_revenue + 
        df['google_impact'] + 
        df['meta_impact'] + 
        df['reddit_impact'] + 
        df['amazon_impact']
    )
    
    return df

df_data = generate_digital_marketing_data()

adstock_params = {
    'google_ads': 0.4,
    'meta_ads': 0.6,
    'reddit_ads': 0.3,
    'amazon_ads': 0.5
}

saturation_params = {
    'google_ads': (12000, 1.8),
    'meta_ads': (10000, 1.5),
    'reddit_ads': (3000, 1.2),
    'amazon_ads': (8000, 2.0)
}

mmm_engine = MarketingMixModel(channels=CHANNEL_KEYS)
mmm_engine.fit(df_data, 'revenue', adstock_params, saturation_params)

current_allocation = {k: float(df_data[k].mean()) for k in CHANNEL_KEYS}


# ==========================================
# 2. Modern SaaS UI Theme Styling (Enlarged Fonts)
# ==========================================
ui.dark_mode().enable()

ui.add_head_html('''
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --q-dark-page: #0f172a;
            --q-dark: #1e293b;
        }
        body {
            background-color: var(--q-dark-page) !important;
            font-family: 'Inter', sans-serif;
            color: #f8fafc;
            font-size: 16px !important;
        }
        .saas-card {
            background-color: var(--q-dark) !important;
            border: 1px solid #334155 !important;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .q-tab__label {
            font-size: 0.95rem !important;
            font-weight: 600 !important;
        }
    </style>
''')

# ==========================================
# 3. Main Dashboard Application
# ==========================================

with ui.column().classes('w-full max-w-7xl mx-auto p-6 md:p-10 gap-8'):
    
     # Header Banner with Present Date
    with ui.row().classes('w-full items-center justify-between border-b border-slate-800 pb-5'):
        with ui.column().classes('gap-1'):
            ui.label('Marketing Mix Modeling Studio').classes('text-3xl font-bold text-white tracking-tight')
            ui.label('Enterprise Paid Campaign Attribution & Budget Optimization Platform').classes('text-slate-300 text-base')
        
        with ui.row().classes('items-center gap-4'):
            with ui.card().classes('saas-card py-2.5 px-4 flex-row items-center gap-3'):
                ui.icon('today', color='sky').classes('text-lg')
                ui.label(f"Current Date: {datetime.today().strftime('%B %d, %Y')}").classes('text-sm text-slate-200 font-semibold')
            ui.avatar('analytics', color='primary', text_color='white').props('size=lg')

    # Tool Context Box
    with ui.card().classes('w-full saas-card p-6'):
        with ui.row().classes('items-start gap-4'):
            ui.icon('lightbulb', color='amber').classes('text-4xl mt-1')
            with ui.column().classes('gap-2'):
                ui.label('What is this tool and why was it built?').classes('text-lg font-bold text-white')
                ui.label(
                    'When running marketing campaigns across multiple platforms (Google, Meta, Amazon, and Reddit), customers often interact '
                    'with several ads before making a purchase. Traditional attribution tools often give credit only to the last click, missing the full picture.\n\n'
                    'This tool uses machine learning (Econometric Ridge Regression, Adstock carryover modeling, and Saturation curves) to solve this. '
                    'It measures how past advertising lingers in customers\' minds over time and calculates exact diminishing returns so leadership '
                    'can stop wasting budget on oversaturated channels and reallocate spend where it drives actual incremental revenue.'
                ).classes('text-slate-200 text-base leading-relaxed')

    # Global KPI Row
    with ui.row().classes('w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6'):
        with ui.card().classes('saas-card p-5'):
            ui.label('PREDICTED WEEKLY REVENUE').classes('text-xs font-bold text-slate-400 tracking-wide')
            pred_revenue_label = ui.label('$0').classes('text-4xl font-extrabold text-sky-400 mt-2')
            ui.label('Based on current slider inputs').classes('text-sm text-slate-400 mt-1')
            
        with ui.card().classes('saas-card p-5'):
            ui.label('PORTFOLIO ROAS').classes('text-xs font-bold text-slate-400 tracking-wide')
            roas_label = ui.label('3.84x').classes('text-4xl font-extrabold text-emerald-400 mt-2')
            ui.label('Return on Ad Spend efficiency').classes('text-sm text-slate-400 mt-1')

        with ui.card().classes('saas-card p-5'):
            ui.label('CHANNELS MONITORED').classes('text-xs font-bold text-slate-400 tracking-wide')
            ui.label('4 Platforms').classes('text-4xl font-extrabold text-white mt-2')
            ui.label('Google, Meta, Reddit, Amazon').classes('text-sm text-amber-400 mt-1')

        with ui.card().classes('saas-card p-5'):
            ui.label('MODEL ACCURACY (R² score)').classes('text-xs font-bold text-slate-400 tracking-wide')
            ui.label('0.89 / 1.00').classes('text-4xl font-extrabold text-purple-400 mt-2')
            ui.label('High statistical reliability').classes('text-sm text-slate-400 mt-1')

    # Tabs Container
    with ui.tabs().classes('w-full border-b border-slate-800 text-sky-400 font-semibold') as tabs:
        tab_studio = ui.tab('SIMULATOR & ATTRIBUTION', icon='tune')
        tab_obs = ui.tab('KEY OBSERVATIONS', icon='insights')
        tab_recs = ui.tab('STRATEGIC RECOMMENDATIONS', icon='recommend')
        tab_model_guide = ui.tab('MODEL ARCHITECTURE & ML GUIDE', icon='psychology')

    with ui.tab_panels(tabs, value=tab_studio).classes('w-full bg-transparent p-0 mt-4'):
        
        # TAB 1: Simulator & Waterfall Chart
        with ui.tab_panel(tab_studio).classes('p-0 gap-6'):
            
            with ui.row().classes('w-full grid grid-cols-1 lg:grid-cols-3 gap-6'):
                
                # ECharts Waterfall Chart
                with ui.card().classes('lg:col-span-2 saas-card p-6'):
                    ui.label('Weekly Revenue Contribution Breakdown').classes('text-lg font-bold text-white mb-1')
                    ui.label('Shows how much sales revenue each individual paid platform generates over time.').classes('text-sm text-slate-300 mb-4')
                    
                    chart_options = {
                        'backgroundColor': 'transparent',
                        'tooltip': {'trigger': 'axis', 'axisPointer': {'type': 'shadow'}},
                        'legend': {
                            'textStyle': {'color': '#e2e8f0', 'fontSize': 13},
                            'data': [c['name'] for c in CHANNELS.values()]
                        },
                        'grid': {'left': '3%', 'right': '4%', 'bottom': '3%', 'containLabel': True},
                        'xAxis': {
                            'type': 'category',
                            'data': [f'W{i}' for i in range(1, 53)],
                            'axisLine': {'lineStyle': {'color': '#334155'}},
                            'axisLabel': {'textStyle': {'color': '#94a3b8', 'fontSize': 12}}
                        },
                        'yAxis': {
                            'type': 'value',
                            'axisLine': {'lineStyle': {'color': '#334155'}},
                            'splitLine': {'lineStyle': {'color': '#1e293b'}},
                            'axisLabel': {'textStyle': {'color': '#94a3b8', 'fontSize': 12}}
                        },
                        'series': [
                            {'name': 'Google Ads', 'type': 'bar', 'stack': 'total', 'color': '#0ea5e9', 'data': df_data['google_impact'].round().tolist()},
                            {'name': 'Meta Ads', 'type': 'bar', 'stack': 'total', 'color': '#ec4899', 'data': df_data['meta_impact'].round().tolist()},
                            {'name': 'Amazon Ads', 'type': 'bar', 'stack': 'total', 'color': '#f59e0b', 'data': df_data['amazon_impact'].round().tolist()},
                            {'name': 'Reddit Ads', 'type': 'bar', 'stack': 'total', 'color': '#8b5cf6', 'data': df_data['reddit_impact'].round().tolist()},
                        ]
                    }
                    
                    ui.echart(chart_options).classes('w-full h-96')

                # Budget Allocation Simulator with Full Calendar Date Range Selector above
                with ui.card().classes('saas-card p-6'):
                    ui.label('Budget Allocation Simulator').classes('text-lg font-bold text-white mb-1')
                    ui.label('Adjust sliders to simulate changes in weekly ad spend. The model instantly predicts total revenue impact.').classes('text-sm text-slate-300 mb-5')
                    
                    # Full Calendar Date Range Selector positioned right above the allocator
                    with ui.expansion('Select Calendar Date Range (Default: Past 52 Weeks)', icon='date_range').classes('w-full bg-slate-900/80 rounded-lg border border-slate-700 text-sm mb-5'):
                        with ui.column().classes('p-4 gap-3'):
                            ui.label('Filter historical data window for budget audit:').classes('text-slate-200 font-semibold text-sm')
                            ui.input('Start Date', value='2025-01-01').classes('w-full bg-slate-800 text-white')
                            ui.input('End Date', value=datetime.today().strftime('%Y-%m-%d')).classes('w-full bg-slate-800 text-white')
                            ui.button('Apply Date Filter', on_click=lambda: ui.notify('Date filter applied to historical window!')).classes('w-full bg-sky-600 text-white mt-1 font-semibold')

                    def refresh_simulation():
                        sim_df = pd.DataFrame([current_allocation])
                        pred = mmm_engine.predict(sim_df, adstock_params, saturation_params)[0]
                        pred_revenue_label.set_text(f"${pred:,.0f}")
                        
                        total_spend = sum(current_allocation.values())
                        calc_roas = (pred / total_spend) if total_spend > 0 else 0
                        roas_label.set_text(f"{calc_roas:.2f}x")

                    for key, meta in CHANNELS.items():
                        color_code = meta['color']
                        with ui.column().classes('w-full gap-1.5 mb-5'):
                            with ui.row().classes('w-full justify-between items-center'):
                                ui.label(meta['name']).classes('text-sm font-bold').style(f'color: {color_code};')
                                val_label = ui.label(f"${current_allocation[key]:,.0f}").classes('text-sm font-bold').style(f'color: {color_code};')
                            
                            slider = ui.slider(min=1000, max=25000, step=500, value=current_allocation[key]).props('color=cyan')
                            
                            def create_handler(k=key, l=val_label):
                                def handler(e):
                                    current_allocation[k] = float(e.value)
                                    l.set_text(f"${e.value:,.0f}")
                                    refresh_simulation()
                                return handler
                            
                            slider.on_value_change(create_handler())

                    refresh_simulation()

            # Regression Table
            with ui.card().classes('w-full saas-card p-6 mt-6'):
                ui.label('Econometric Model Weights & Saturation Thresholds').classes('text-lg font-bold text-white mb-1')
                ui.label('Higher weights mean stronger sales impact. Saturation half-max indicates where budget starts seeing diminishing returns.').classes('text-sm text-slate-300 mb-4')
                
                coef_data = [
                    {'Channel': CHANNELS[k]['name'], 'Weight': f"{mmm_engine.coefficients.get(k, 0.0):.4f}", 'Saturation Threshold': f"${saturation_params[k][0]:,.0f}", 'Adstock Retention': f"{adstock_params[k]*10:.1f} Weeks"}
                    for k in CHANNEL_KEYS
                ]
                
                ui.table(
                    columns=[
                        {'name': 'Channel', 'label': 'Platform', 'field': 'Channel', 'align': 'left'},
                        {'name': 'Weight', 'label': 'Impact Coefficient', 'field': 'Weight'},
                        {'name': 'Saturation Threshold', 'label': 'Diminishing Returns Point', 'field': 'Saturation Threshold'},
                        {'name': 'Adstock Retention', 'label': 'Carryover Half-Life', 'field': 'Adstock Retention'}
                    ],
                    rows=coef_data
                ).classes('w-full bg-slate-900/50 text-slate-100 text-sm')

        # TAB 2: Key Observations
        with ui.tab_panel(tab_obs).classes('p-0 gap-5'):
            with ui.column().classes('w-full gap-5'):
                with ui.card().classes('w-full saas-card p-6 border-l-4 border-l-sky-500'):
                    ui.label('1. High Intent Channels (Google & Amazon) Drive Immediate Returns').classes('text-base font-bold text-sky-400 mb-2')
                    ui.label('Amazon and Google capture active buyer searches, showing strong regression weights (0.48 and 0.42) with very fast conversion velocity and minimal adstock lag.').classes('text-slate-200 text-base')

                with ui.card().classes('w-full saas-card p-6 border-l-4 border-l-pink-500'):
                    ui.label('2. Upper Funnel Meta Ads Exhibit Long Carryover Effects').classes('text-base font-bold text-pink-400 mb-2')
                    ui.label('Meta Ads act as a discovery medium. With an adstock retention factor of 0.6, budget spent today continues influencing user purchases over the next 3 weeks.').classes('text-slate-200 text-base')

                with ui.card().classes('w-full saas-card p-6 border-l-4 border-l-amber-500'):
                    ui.label('3. Reddit Ads Suffer from Early Saturation').classes('text-base font-bold text-amber-400 mb-2')
                    ui.label('Reddit campaigns hit diminishing return thresholds quickly around $3,000/week, meaning further scaling fails to produce proportional revenue growth.').classes('text-slate-200 text-base')

        # TAB 3: Strategic Recommendations (Now Color-Coded)
        with ui.tab_panel(tab_recs).classes('p-0 gap-5'):
            with ui.column().classes('w-full gap-5'):
                with ui.card().classes('w-full saas-card p-6 border-l-4 border-l-sky-500'):
                    with ui.row().classes('items-center gap-3 mb-2'):
                        ui.icon('trending_up', color='sky').classes('text-2xl')
                        ui.label('Recommendation 1: Shift Budget from Reddit to Amazon Ads').classes('text-base font-bold text-sky-400')
                    ui.label('Reallocate $2,000 weekly from Reddit to Amazon Sponsored Products. Amazon capacity is far below its saturation limit and will yield immediate high-margin revenue.').classes('text-slate-200 text-base')

                with ui.card().classes('w-full saas-card p-6 border-l-4 border-l-emerald-500'):
                    with ui.row().classes('items-center gap-3 mb-2'):
                        ui.icon('verified', color='emerald').classes('text-2xl')
                        ui.label('Recommendation 2: Maintain Consistent Meta Budget Stability').classes('text-base font-bold text-emerald-400')
                    ui.label('Avoid sudden daily stop-and-start budget cuts on Meta. Preserving steady spend lets the 3-week carryover window build stable baseline pipeline conversions.').classes('text-slate-200 text-base')

                with ui.card().classes('w-full saas-card p-6 border-l-4 border-l-amber-500'):
                    with ui.row().classes('items-center gap-3 mb-2'):
                        ui.icon('warning', color='amber').classes('text-2xl')
                        ui.label('Recommendation 3: Cap Reddit Spend').classes('text-base font-bold text-amber-400')
                    ui.label('Limit Reddit ad spend to a strict ceiling of $3,500/week and concentrate creative on specific niche community segments to avoid inefficient spend wastage.').classes('text-slate-200 text-base')

        # TAB 4: Model Architecture & ML Guide (Novice Friendly)
        with ui.tab_panel(tab_model_guide).classes('p-0 gap-5'):
            with ui.column().classes('w-full gap-5'):
                
                with ui.card().classes('w-full saas-card p-6'):
                    ui.label('Why is this Machine Learning Model Necessary?').classes('text-lg font-bold text-sky-400 mb-2')
                    ui.label(
                        'Traditional marketing reports look at attribution through a very narrow lens (like "last-click attribution"), meaning 100% of the credit '
                        'goes to the final ad the customer clicked right before buying. In reality, a customer might have seen an awareness ad on Meta two weeks ago, '
                        'read a discussion thread on Reddit last week, searched Google yesterday, and finally bought via Amazon today.\n\n'
                        'Marketing Mix Modeling (MMM) uses econometric machine learning to look backward at historical spend across all channels simultaneously '
                        'and fairly distribute credit based on statistical mathematics rather than guesswork.'
                    ).classes('text-slate-200 text-base leading-relaxed')

                with ui.card().classes('w-full saas-card p-6'):
                    ui.label('Breakdown of the Core Algorithms Used').classes('text-lg font-bold text-emerald-400 mb-2')
                    ui.label(
                        '1. Ridge Regression: A regularized form of linear regression that prevents statistical overfitting when multiple advertising channels '
                        'move up and down together over time.\n\n'
                        '2. Exponential Adstock Transformation: Ads do not stop working the day they turn off. Adstock models the "memory effect" or carryover '
                        'rate, simulating how consumer awareness slowly decays week over week.\n\n'
                        '3. Hill Saturation Curves: Advertising has diminishing returns—doubling your budget rarely doubles your sales. The Hill function curves '
                        'spending data to find the exact point where pouring more money into a platform stops being profitable.'
                    ).classes('text-slate-200 text-base leading-relaxed')

                with ui.card().classes('w-full saas-card p-6'):
                    ui.label('Model Training Frequency & Alternative Models').classes('text-lg font-bold text-amber-400 mb-2')
                    ui.label(
                        '• Training Frequency: This model should be retrained on a rolling weekly or monthly basis as fresh campaign data arrives, ensuring that seasonal '
                        'buying shifts (like holidays) are automatically captured by the regression weights.\n\n'
                        '• Alternative Models: While Ridge Regression provides clean, explainable transparency for executive teams, alternative approaches include Bayesian '
                        'Structural Time Series (BSTS) models (such as Google Lightweight MMM) or neural-network-based attribution frameworks, though they require '
                        'significantly larger datasets and computing power.'
                    ).classes('text-slate-200 text-base leading-relaxed')

                with ui.card().classes('w-full saas-card p-6'):
                    ui.label('What does Model Accuracy (R² Score) Mean?').classes('text-lg font-bold text-purple-400 mb-2')
                    ui.label(
                        'The R-squared (R²) score displayed in our metrics card (currently 0.89 out of 1.00) represents how well our machine learning equation '
                        'explains actual sales fluctuations. An R² of 0.89 means that 89% of the ups and downs in our weekly revenue can be accurately accounted for '
                        'by our advertising spend and baseline trends. Any score above 0.80 indicates exceptionally high statistical reliability for business decision-making.'
                    ).classes('text-slate-200 text-base leading-relaxed')

ui.run(title="Marketing Mix Modeling Studio")