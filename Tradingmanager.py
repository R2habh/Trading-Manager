import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime
import random
import math

class ProfessionalTradingManager:
    def __init__(self, root):
        self.root = root
        self.root.title("R2HABH TRADING MANAGER // CYBERPUNK EDITION") # Updated title
        self.root.geometry("1200x900")
        self.root.configure(bg='#0A0A0A') # Very dark, almost black
        self.root.minsize(1000, 800)
        
        # Cyberpunk Color Scheme
        self.bg_color = '#0A0A0A' # Main background - nearly black
        self.panel_color = '#1A1A2A' # Dark blue-grey for panels
        self.accent_color = '#00FF8C' # Neon Green - main highlight
        self.win_color = '#00FF8C' # Same neon green for wins
        self.loss_color = '#FF00A0' # Neon Pink/Magenta for losses
        self.text_color = '#E0FBFC' # Light white/grey for general text
        self.highlight_color = '#00BFFF' # Electric Blue for titles/emphases
        self.progress_color = '#00BFFF' # Matches highlight color
        self.button_color = '#2A2A3A' # Dark button base
        self.entry_bg = '#0F0F0F' # Even darker for entry fields

        # Initialize variables (unchanged business logic)
        self.initial_capital = 50.0
        self.daily_growth_target = 5.0
        self.stop_loss_limit = 5.0
        self.starting_trade_value = 1.0
        self.trade_multiplier = 1.5
        
        # Session variables
        self.current_balance = self.initial_capital
        self.daily_start_balance = self.initial_capital
        self.current_trade_value = self.starting_trade_value
        self.trades_history = []
        self.wins_count = 0
        self.losses_count = 0
        self.session_date = datetime.now().strftime("%Y-%m-%d")
        self.trading_tips = [
            "Risk Management: Never risk more than 1-2% of your capital on a single trade",
            "Discipline: Stick to your trading plan even during emotional times",
            "Consistency: Focus on consistent small gains rather than chasing big wins",
            "Psychology: The market is 80% psychology, 20% strategy",
            "Patience: Wait for high-probability setups instead of forcing trades",
            "Education: Spend as much time learning as you do trading",
            "Journaling: Track every trade to identify patterns and improve",
            "Adaptation: Markets change - your strategy should evolve too",
            "Position Sizing: Use appropriate position sizes for your account",
            "Risk/Reward: Aim for at least 1:2 risk/reward ratio in your trades"
        ]
        
        # Load previous session if exists
        self.load_session()
        
        # Create GUI
        self.create_widgets()
        self.update_display()
        self.show_random_tip()

    def create_widgets(self):
        """Creates and arranges all the widgets in the main window using a structured grid layout."""
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        main_frame.columnconfigure(0, weight=1, minsize=380)  # Left pane
        main_frame.columnconfigure(1, weight=2, minsize=520)  # Right pane
        main_frame.rowconfigure(0, weight=0)  # Header
        main_frame.rowconfigure(1, weight=1)  # Content

        # ===== HEADER SECTION =====
        self.create_header(main_frame)

        # ===== LEFT PANE =====
        left_pane = tk.Frame(main_frame, bg=self.bg_color)
        left_pane.grid(row=1, column=0, sticky='nsew', padx=(0, 10))
        left_pane.rowconfigure(0, weight=0)  # Settings
        left_pane.rowconfigure(1, weight=0)  # Trade execution
        left_pane.rowconfigure(2, weight=1)  # Controls (expands to push them down)
        
        settings_frame = self.create_panel(left_pane, "⚙️ PARAMETER GRID", 0, 0)
        self.create_settings(settings_frame)
        
        trade_frame = self.create_panel(left_pane, "🎯 EXECUTION INTERFACE", 1, 0, pady_config=(15, 0))
        self.create_trade_execution(trade_frame)
        
        bottom_left_frame = tk.Frame(left_pane, bg=self.bg_color)
        bottom_left_frame.grid(row=2, column=0, sticky='sew', pady=(15, 0))
        self.create_control_buttons(bottom_left_frame)

        # ===== RIGHT PANE =====
        right_pane = tk.Frame(main_frame, bg=self.bg_color)
        right_pane.grid(row=1, column=1, sticky='nsew', padx=(10, 0))
        right_pane.rowconfigure(0, weight=0) # Account Overview
        right_pane.rowconfigure(1, weight=1) # Tabs (History, Knowledge)

        balance_frame = self.create_panel(right_pane, "💰 ASSET OVERVIEW", 0, 0)
        self.create_balance_display(balance_frame)
        
        self.create_right_notebook(right_pane, 1, 0)

    def create_header(self, parent):
        """Creates the main header section."""
        header_frame = tk.Frame(parent, bg=self.bg_color)
        header_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        
        title_label = tk.Label(
            header_frame, text="R2HABH TRADING MANAGER",
            font=('Cyberpunk', 28, 'bold'), fg=self.highlight_color, bg=self.bg_color # Attempting a different font (might default)
        )
        title_label.pack(side='left', anchor='w')
        
        subtitle_label = tk.Label(
            header_frame, text="RISK PROTOCOLS • CAPITAL INITIATION • DISCIPLINE MATRIX", # Cyberpunk lingo
            font=('Cyberpunk', 13), fg=self.text_color, bg=self.bg_color # Attempting a different font
        )
        subtitle_label.pack(side='left', anchor='sw', padx=15, pady=(0, 4))

    def create_panel(self, parent, title, r, c, padx_config=(0, 0), pady_config=(0, 0)):
        """Helper function to create a styled LabelFrame panel."""
        frame = tk.LabelFrame(
            parent, text=title, fg=self.highlight_color, bg=self.panel_color,
            font=('Arial', 12, 'bold'), relief=tk.FLAT, bd=2, highlightbackground=self.highlight_color, highlightthickness=1, # Flat but with border glow
            padx=10, pady=10 
        )
        frame.grid(row=r, column=c, sticky='nsew', padx=padx_config, pady=pady_config)
        parent.columnconfigure(c, weight=1)
        return frame

    def create_settings(self, parent):
        self.capital_var = tk.StringVar(value=str(self.initial_capital))
        self.growth_var = tk.StringVar(value=str(self.daily_growth_target))
        self.stop_loss_var = tk.StringVar(value=str(self.stop_loss_limit))
        self.multiplier_var = tk.StringVar(value=str(self.trade_multiplier))
        
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        
        labels = [
            ("INITIAL CAPITAL ($):", self.capital_var),
            ("DAILY GROWTH TARGET (%):", self.growth_var),
            ("STOP LOSS LIMIT (%):", self.stop_loss_var),
            ("LOSS MULTIPLIER:", self.multiplier_var)
        ]
        
        for i, (label_text, var) in enumerate(labels):
            tk.Label(
                parent, text=label_text, fg=self.text_color, bg=self.panel_color,
                font=('Arial', 11), anchor='w'
            ).grid(row=i, column=0, sticky='w', padx=15, pady=8)
            
            entry = tk.Entry(
                parent, textvariable=var, bg=self.entry_bg, fg=self.accent_color, insertbackground=self.accent_color, # Neon cursor
                font=('Consolas', 11), relief=tk.FLAT, width=15 # Monospaced font for entries
            )
            entry.grid(row=i, column=1, sticky='ew', padx=15, pady=8)
        
        update_btn = tk.Button(
            parent, text="APPLY PROTOCOL UPDATE", command=self.update_settings, bg=self.button_color,
            fg=self.highlight_color, font=('Arial', 10, 'bold'), relief=tk.FLAT, padx=15, pady=8,
            activebackground='#3A3A4A', activeforeground=self.highlight_color # Darker hover with neon text
        )
        update_btn.grid(row=4, column=0, columnspan=2, sticky='ew', padx=15, pady=(10, 5))

    def create_balance_display(self, parent):
        parent.columnconfigure(0, weight=1)
        
        self.balance_label = tk.Label(
            parent, text="$0.00", font=('Digital-7', 42, 'bold'), fg=self.accent_color, # Digital font for balance
            bg=self.panel_color, pady=15
        )
        self.balance_label.grid(row=0, column=0, sticky='nsew')
        
        stats_frame = tk.Frame(parent, bg=self.panel_color)
        stats_frame.grid(row=1, column=0, sticky='ew', padx=20, pady=(0, 10))
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        
        target_frame = tk.Frame(stats_frame, bg=self.panel_color)
        target_frame.grid(row=0, column=0, sticky='w')
        tk.Label(target_frame, text="DAILY TARGET:", fg=self.text_color, bg=self.panel_color, font=('Arial', 10)).pack(anchor='w')
        self.daily_target_label = tk.Label(target_frame, text="$0.00", fg=self.highlight_color, bg=self.panel_color, font=('Digital-7', 14, 'bold')) # Digital font
        self.daily_target_label.pack(anchor='w')
        
        stop_frame = tk.Frame(stats_frame, bg=self.panel_color)
        stop_frame.grid(row=0, column=1, sticky='e')
        tk.Label(stop_frame, text="STOP LOSS THRESHOLD:", fg=self.text_color, bg=self.panel_color, font=('Arial', 10)).pack(anchor='e')
        self.stop_loss_label = tk.Label(stop_frame, text="$0.00", fg=self.loss_color, bg=self.panel_color, font=('Digital-7', 14, 'bold')) # Digital font
        self.stop_loss_label.pack(anchor='e')
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Cyber.Horizontal.TProgressbar", 
                        background=self.progress_color, 
                        troughcolor=self.entry_bg, 
                        thickness=15, # Thicker for impact
                        bordercolor=self.panel_color, 
                        lightcolor=self.progress_color, 
                        darkcolor=self.progress_color)
        
        self.progress_var = tk.DoubleVar()
        progress_container = tk.Frame(parent, bg=self.panel_color)
        progress_container.grid(row=2, column=0, sticky='ew', padx=20, pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(progress_container, variable=self.progress_var, maximum=100, mode='determinate', style="Cyber.Horizontal.TProgressbar")
        self.progress_bar.pack(fill='x', expand=True)
        
        self.progress_label = tk.Label(parent, text="PROGRESS: 0%", fg=self.text_color, bg=self.panel_color, font=('Arial', 10))
        self.progress_label.grid(row=3, column=0, sticky='e', padx=20, pady=(0, 10))

    def create_trade_execution(self, parent):
        parent.columnconfigure(0, weight=1)
        
        self.trade_value_label = tk.Label(parent, text="TRADE VALUE: $1.00", font=('Digital-7', 22, 'bold'), fg=self.accent_color, bg=self.panel_color)
        self.trade_value_label.pack(pady=10)
        
        buttons_frame = tk.Frame(parent, bg=self.panel_color)
        buttons_frame.pack(fill='x', expand=True, padx=10, pady=5)
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        
        self.win_button = tk.Button(
            buttons_frame, text="✅ GAIN PROTOCOL", command=self.execute_win, bg=self.win_color, fg='black', # Black text on neon
            font=('Arial', 13, 'bold'), height=2, relief=tk.FLAT, bd=0, 
            activebackground='#00CC77', activeforeground='black' 
        )
        self.win_button.grid(row=0, column=0, padx=(0, 5), sticky='nsew')
        
        self.lose_button = tk.Button(
            buttons_frame, text="❌ LOSS PROTOCOL", command=self.execute_loss, bg=self.loss_color, fg='white', # White text on neon
            font=('Arial', 13, 'bold'), height=2, relief=tk.FLAT, bd=0, 
            activebackground='#EE008C', activeforeground='white' 
        )
        self.lose_button.grid(row=0, column=1, padx=(5, 0), sticky='nsew')
        
        session_frame = tk.Frame(parent, bg=self.panel_color)
        session_frame.pack(fill='x', expand=True, padx=10, pady=(5, 10))
        session_frame.columnconfigure(0, weight=1)
        session_frame.columnconfigure(1, weight=1)
        
        win_frame = tk.Frame(session_frame, bg=self.panel_color)
        win_frame.grid(row=0, column=0, sticky='w')
        tk.Label(win_frame, text="WINS:", fg=self.text_color, bg=self.panel_color, font=('Arial', 10)).pack(side='left')
        self.wins_label = tk.Label(win_frame, text="0", fg=self.win_color, bg=self.panel_color, font=('Digital-7', 14, 'bold')) # Digital font
        self.wins_label.pack(side='left', padx=5)
        
        loss_frame = tk.Frame(session_frame, bg=self.panel_color)
        loss_frame.grid(row=0, column=1, sticky='e')
        tk.Label(loss_frame, text="LOSSES:", fg=self.text_color, bg=self.panel_color, font=('Arial', 10)).pack(side='left')
        self.losses_label = tk.Label(loss_frame, text="0", fg=self.loss_color, bg=self.panel_color, font=('Digital-7', 14, 'bold')) # Digital font
        self.losses_label.pack(side='left', padx=5)

    def create_right_notebook(self, parent, r, c):
        """Creates the notebook widget for the right pane, combining History and Knowledge."""
        notebook_frame = tk.Frame(parent, bg=self.panel_color, bd=0)
        notebook_frame.grid(row=r, column=c, sticky='nsew', pady=(15, 0))
        notebook_frame.grid_rowconfigure(0, weight=1)
        notebook_frame.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.configure('Cyber.TNotebook', background=self.panel_color, borderwidth=0)
        style.configure('TNotebook.Tab', 
                        background=self.bg_color, 
                        foreground=self.text_color,
                        font=('Arial', 11, 'bold'),
                        padding=[15, 8], 
                        borderwidth=0,
                        lightcolor=self.bg_color, darkcolor=self.bg_color # No border gradient
                        )
        style.map('TNotebook.Tab', 
                  background=[('selected', self.panel_color)],
                  foreground=[('selected', self.highlight_color)], # Neon blue for selected tab text
                  expand=[('selected', [1, 1, 1, 0])] 
                  )
        
        notebook = ttk.Notebook(notebook_frame, style='Cyber.TNotebook')
        notebook.grid(row=0, column=0, sticky='nsew')
        
        # Create frames for each tab
        history_tab = tk.Frame(notebook, bg=self.panel_color, padx=10, pady=10)
        wisdom_tab = tk.Frame(notebook, bg=self.panel_color, padx=10, pady=10)
        strategy_tab = tk.Frame(notebook, bg=self.panel_color, padx=10, pady=10)
        risk_tab = tk.Frame(notebook, bg=self.panel_color, padx=10, pady=10)

        notebook.add(history_tab, text='📊 DATA LOG') # Cyberpunk naming
        notebook.add(wisdom_tab, text='💡 KNOWLEDGE CORE')
        notebook.add(strategy_tab, text='📈 STRATEGY PROTOCOLS')
        notebook.add(risk_tab, text='🛡️ RISK ANALYTICS')

        # Populate tabs
        self.create_history_display(history_tab)
        self.populate_wisdom_tab(wisdom_tab)
        self.populate_strategy_tab(strategy_tab)
        self.populate_risk_tab(risk_tab)

    def create_history_display(self, parent):
        """Creates the ScrolledText widget for trade history."""
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self.history_text = scrolledtext.ScrolledText(
            parent, bg=self.entry_bg, fg=self.text_color, font=('Consolas', 10), # Monospaced font
            state='disabled', padx=10, pady=10, relief=tk.FLAT, bd=0, insertbackground=self.text_color # Cursor color
        )
        self.history_text.grid(row=0, column=0, sticky='nsew')

    def populate_wisdom_tab(self, parent):
        """Populates the Trading Wisdom tab."""
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self.tip_label = tk.Label(
            parent, text="", wraplength=480, justify='left', fg=self.text_color, 
            bg=self.panel_color, font=('Arial', 12, 'italic'), padx=15, pady=15
        )
        self.tip_label.grid(row=0, column=0, sticky='nsew')
        
        next_tip_btn = tk.Button(
            parent, text="GENERATE NEW BYTE", command=self.show_random_tip, bg=self.button_color,
            fg=self.accent_color, font=('Arial', 11), relief=tk.FLAT, padx=10, pady=5, # Neon text
            activebackground='#3A3A4A', activeforeground=self.accent_color
        )
        next_tip_btn.grid(row=1, column=0, sticky='e', pady=(10,0))

    def populate_strategy_tab(self, parent):
        """Populates the Market Strategy tab."""
        strategy_text = """// HOLOGRAPHIC PRICE ACTION PROTOCOL V3.1 //

1. TREND INITIATION SCAN:
   • Scan Daily/4H data streams for dominant market vector.
   • Engage only with higher timeframe momentum flux.
   • Core Algorithms: 200 EMA Predictive, Quantum Trendline Analysis, Fractal High/Low Detection.

2. RETRACEMENT SEQUENCE LOCK:
   • Identify system pullbacks to critical support/resistance nodes.
   • Optimal Recalibration Zones: 38.2%-61.8% Fibonacci Algorithms.
   • Confirmation Packet: Pin-Bar, Engulfing Candlestick Patterns.

3. ENTRY CONFIRMATION FIRE:
   • Entry Trigger: Bullish Reversal Signature (Uptrend).
   • Stop Loss Protocol: 1-2% below entry point or last secure low.
   • Profit Exfiltration: Minimum 1:2 risk-reward ratio."""
        
        strategy_label = tk.Label(
            parent, text=strategy_text, wraplength=480, justify='left', 
            fg=self.text_color, bg=self.panel_color, font=('Consolas', 10), # Monospaced font
            padx=15, pady=15, anchor='nw'
        )
        strategy_label.pack(fill='both', expand=True)

    def populate_risk_tab(self, parent):
        """Populates the Risk Management tab."""
        risk_text = """// QUANTUM RISK MANAGEMENT CORE //

1. POSITION ALGORITHM SIZING:
   • Formula: (ACCOUNT RISK % × BALANCE) ÷ (ENTRY - STOP LOSS).
   • Absolute Limit: Never exceed 1-2% risk per data-transaction.

2. STOP LOSS DISPLACEMENT:
   • Technical Coordinates: Below major support/resistance nodes.
   • Volatility Calibration: Based on ATR (1.5-2× standard deviation).
   • Time-Lock Expiration: Disengage if trade fails to activate within parameters.

3. PROFIT SHIELD PROTOCOLS:
   • Zero-Risk Shift: Move stop to break-even at 1× risk.
   • Trailing Safeguard: Dynamically adjust stop to secure gains.
   • Partial Exfiltration: Scale out of positions at pre-defined profit nodes."""

        risk_label = tk.Label(
            parent, text=risk_text, wraplength=480, justify='left', 
            fg=self.text_color, bg=self.panel_color, font=('Consolas', 10), # Monospaced font
            padx=15, pady=15, anchor='nw'
        )
        risk_label.pack(fill='both', expand=True)

    def create_control_buttons(self, parent):
        """Creates the main control buttons and the quote label."""
        parent.columnconfigure((0, 1, 2), weight=1)
        
        button_style = {
            'font': ('Arial', 10, 'bold'), 'relief': tk.FLAT, 'padx': 15, 'pady': 8
        }
        
        new_day_btn = tk.Button(parent, text="🌅 NEW CYCLE", command=self.new_day, bg='#0080FF', fg='black', **button_style, activebackground='#0066CC') # Electric Blue
        new_day_btn.grid(row=0, column=0, padx=5, sticky='ew')
        
        reset_btn = tk.Button(parent, text="🔄 REBOOT SYSTEM", command=self.reset_session, bg='#FF4500', fg='white', **button_style, activebackground='#CC3700') # Orange-Red
        reset_btn.grid(row=0, column=1, padx=5, sticky='ew')
        
        save_btn = tk.Button(parent, text="💾 SAVE MEMORY", command=self.save_session, bg='#8A2BE2', fg='white', **button_style, activebackground='#6A1BBF') # Electric Purple
        save_btn.grid(row=0, column=2, padx=5, sticky='ew')
        
        quotes = [
            "DISCIPLINE IS THE ALGORITHM BETWEEN GOALS AND ACHIEVEMENT.",
            "THE MARKET IS A DATA CONDUIT TRANSFERRING CRYPTOS FROM THE IMPATIENT TO THE PATIENT.",
            "RISK EMERGES FROM AN ABSENCE OF DATA INTEGRITY.",
            "THE FOUR MOST DANGEROUS COMMANDS IN INVESTING: 'THIS CYCLE IS DIFFERENT.'",
            "IN TRADING, OPTIMIZATION IS THE ULTIMATE SOPHISTICATION."
        ]
        
        self.quote_label = tk.Label(
            parent, text=random.choice(quotes), fg=self.highlight_color, bg=self.bg_color,
            font=('Consolas', 10, 'italic'), padx=10, wraplength=350, justify='center' # Monospaced font for quotes
        )
        self.quote_label.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(15, 0))

    # ===================================================================
    # BUSINESS LOGIC AND HELPER METHODS (Unchanged from original code)
    # ===================================================================

    def show_random_tip(self):
        tip = random.choice(self.trading_tips)
        self.tip_label.config(text=tip)
    
    def update_settings(self):
        try:
            new_capital = float(self.capital_var.get())
            self.daily_growth_target = float(self.growth_var.get())
            self.stop_loss_limit = float(self.stop_loss_var.get())
            self.trade_multiplier = float(self.multiplier_var.get())
            
            if new_capital <= 0: raise ValueError("Capital must be positive")
            if self.daily_growth_target <= 0: raise ValueError("Growth target must be positive")
            if self.stop_loss_limit <= 0: raise ValueError("Stop loss must be positive")
            if self.trade_multiplier <= 1: raise ValueError("Multiplier must be greater than 1")
            
            if new_capital != self.initial_capital:
                self.initial_capital = new_capital
                self.current_balance = new_capital
                self.daily_start_balance = new_capital
                self.current_trade_value = self.starting_trade_value
                self.trades_history = []
                self.wins_count = 0
                self.losses_count = 0
                messagebox.showinfo("Capital Updated", f"Capital updated to ${new_capital:.2f}\nSession has been reset.")
            else:
                self.initial_capital = new_capital
            
            self.enable_trading()
            self.update_display()
            messagebox.showinfo("Success", "SETTINGS PROTOCOL APPLIED! 🎉") # Cyberpunk message
            
        except ValueError as e:
            messagebox.showerror("Error", f"INPUT ERROR: {str(e)}") # Cyberpunk message
    
    def calculate_daily_target(self):
        return self.daily_start_balance * (1 + self.daily_growth_target / 100)
    
    def calculate_stop_loss(self):
        return max(0.01, self.daily_start_balance * (1 - self.stop_loss_limit / 100))
    
    def execute_win(self):
        if self.check_can_trade():
            self.current_balance += self.current_trade_value
            self.trades_history.append({
                'type': 'WIN', 'amount': self.current_trade_value, 'balance': self.current_balance,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })
            self.wins_count += 1
            self.current_trade_value = self.starting_trade_value
            self.update_display()
            self.check_daily_target()
            
    def execute_loss(self):
        if self.check_can_trade():
            self.current_balance -= self.current_trade_value
            self.trades_history.append({
                'type': 'LOSE', 'amount': self.current_trade_value, 'balance': self.current_balance,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })
            self.losses_count += 1
            self.current_trade_value = max(1.0, self.current_trade_value * self.trade_multiplier)
            self.update_display()
            self.check_stop_loss()
    
    def check_can_trade(self):
        if self.current_balance < self.current_trade_value:
            messagebox.showwarning("INSUFFICIENT CREDITS", f"INSUFFICIENT BALANCE FOR ${self.current_trade_value:.2f} TRADE!") # Cyberpunk message
            return False
        stop_loss = self.calculate_stop_loss()
        if self.current_balance <= stop_loss:
            messagebox.showwarning("STOP LOSS BREACHED", "STOP LOSS THRESHOLD REACHED! SYSTEM LOCKDOWN INITIATED!") # Cyberpunk message
            self.disable_trading() 
            return False
        return True
    
    def check_daily_target(self):
        if self.current_balance >= self.calculate_daily_target():
            self.show_success_popup()
            self.disable_trading()
    
    def check_stop_loss(self):
        if self.current_balance <= self.calculate_stop_loss():
            self.show_stop_loss_popup()
            self.disable_trading()
    
    def show_success_popup(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("PROTOCOL COMPLETE! // SUCCESS!") # Cyberpunk title
        dialog.geometry("400x300")
        dialog.configure(bg=self.panel_color)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="✅", font=('Arial', 48), fg=self.accent_color, bg=self.panel_color).pack(pady=10) # Green checkmark
        tk.Label(dialog, text="DAILY TARGET ACHIEVED! // DATA INTEGRITY OPTIMAL!", font=('Arial', 14, 'bold'), fg=self.highlight_color, bg=self.panel_color, wraplength=350, justify='center').pack(pady=5)
        
        info_frame = tk.Frame(dialog, bg=self.panel_color)
        info_frame.pack(pady=10)
        tk.Label(info_frame, text=f"CURRENT BALANCE: ${self.current_balance:.2f}", font=('Digital-7', 12), fg=self.text_color, bg=self.panel_color).pack() # Digital font
        profit = self.current_balance - self.daily_start_balance
        tk.Label(info_frame, text=f"CYCLE PROFIT: ${profit:.2f}", font=('Digital-7', 14, 'bold'), fg=self.win_color, bg=self.panel_color).pack(pady=5) # Digital font
        
        tk.Label(dialog, text="CONGRATULATIONS! YOUR DISCIPLINE IS UNMATCHED. PROCEEDING WITH OPTIMAL PROTOCOLS.", font=('Arial', 10), fg=self.highlight_color, bg=self.panel_color, justify='center', wraplength=350).pack(pady=10)
        tk.Button(dialog, text="ACKNOWLEDGE", command=dialog.destroy, bg=self.button_color, fg=self.accent_color, font=('Arial', 10, 'bold'), width=18, relief=tk.FLAT, activebackground='#3A3A4A', activeforeground=self.accent_color).pack(pady=10)
        
        self.center_dialog(dialog)
    
    def show_stop_loss_popup(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("EMERGENCY PROTOCOL! // STOP LOSS BREACH!") # Cyberpunk title
        dialog.geometry("450x300")
        dialog.configure(bg=self.panel_color)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="⚠️ SYSTEM BREACH! 📉", font=('Arial', 16, 'bold'), fg=self.loss_color, bg=self.panel_color).pack(pady=20)
        
        info_frame = tk.Frame(dialog, bg=self.panel_color)
        info_frame.pack(pady=10)
        tk.Label(info_frame, text=f"CURRENT BALANCE: ${self.current_balance:.2f}", font=('Digital-7', 12), fg=self.text_color, bg=self.panel_color).pack() # Digital font
        loss_amount = self.daily_start_balance - self.current_balance
        tk.Label(info_frame, text=f"CYCLE LOSS: ${loss_amount:.2f}", font=('Digital-7', 14, 'bold'), fg=self.loss_color, bg=self.panel_color).pack() # Digital font
        
        tk.Label(dialog, text="TRADING INTERFACE OFFLINE TO PROTECT REMAINING ASSETS. INITIATE NEW PROTOCOL?", font=('Arial', 10), fg=self.text_color, bg=self.panel_color, justify='center', wraplength=400).pack(pady=15)
        
        buttons_frame = tk.Frame(dialog, bg=self.panel_color)
        buttons_frame.pack(pady=20)
        tk.Button(buttons_frame, text="🔄 REINITIALIZE CAPITAL", command=lambda: self.reset_to_original_capital(dialog), bg='#FF4500', fg='white', font=('Arial', 10, 'bold'), width=22, relief=tk.FLAT, activebackground='#CC3700').pack(side='left', padx=10) # Orange-Red
        tk.Button(buttons_frame, text="➡️ CONTINUE WITH CURRENT ASSETS", command=lambda: self.continue_with_current_balance(dialog), bg=self.button_color, fg=self.highlight_color, font=('Arial', 10, 'bold'), width=28, relief=tk.FLAT, activebackground='#3A3A4A', activeforeground=self.highlight_color).pack(side='right', padx=10)
        
        self.center_dialog(dialog)

    def center_dialog(self, dialog):
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
    
    def reset_to_original_capital(self, dialog):
        self.current_balance = self.initial_capital
        self.daily_start_balance = self.initial_capital
        self.current_trade_value = self.starting_trade_value
        self.trades_history = []
        self.wins_count = 0
        self.losses_count = 0
        self.session_date = datetime.now().strftime("%Y-%m-%d")
        self.enable_trading()
        self.update_display()
        dialog.destroy()
        messagebox.showinfo("REINITIALIZATION COMPLETE", f"🔄 ASSET REINITIALIZATION COMPLETE!\n\nNEW BALANCE: ${self.current_balance:.2f}") # Cyberpunk message
    
    def continue_with_current_balance(self, dialog):
        self.daily_start_balance = self.current_balance
        self.current_trade_value = self.starting_trade_value
        self.trades_history = []
        self.wins_count = 0
        self.losses_count = 0
        self.session_date = datetime.now().strftime("%Y-%m-%d")
        self.enable_trading()
        self.update_display()
        dialog.destroy()
        messagebox.showinfo("SESSION CONTINUED", f"➡️ NEW CYCLE INITIATED WITH CURRENT ASSETS!\n\nSTARTING BALANCE: ${self.current_balance:.2f}") # Cyberpunk message
    
    def disable_trading(self):
        self.win_button.config(state='disabled', bg='#1A1A1A', activebackground='#1A1A1A', fg='#555555') # Darker disabled state, muted text
        self.lose_button.config(state='disabled', bg='#1A1A1A', activebackground='#1A1A1A', fg='#555555')
    
    def enable_trading(self):
        self.win_button.config(state='normal', bg=self.win_color, activebackground='#00CC77', fg='black')
        self.lose_button.config(state='normal', bg=self.loss_color, activebackground='#EE008C', fg='white')
    
    def new_day(self):
        self.daily_start_balance = self.current_balance
        self.current_trade_value = self.starting_trade_value
        self.trades_history = []
        self.wins_count = 0
        self.losses_count = 0
        self.session_date = datetime.now().strftime("%Y-%m-%d")
        self.enable_trading()
        self.update_display()
        messagebox.showinfo("NEW CYCLE INITIATED", f"🌅 NEW TRADING CYCLE INITIATED!\n\nSTARTING BALANCE: ${self.daily_start_balance:.2f}") # Cyberpunk message
    
    def reset_session(self):
        if messagebox.askyesno("RESET SYSTEM", "CONFIRM SYSTEM RESET? ALL DATA WILL BE WIPED."): # Cyberpunk message
            self.current_balance = self.initial_capital
            self.daily_start_balance = self.initial_capital
            self.current_trade_value = self.starting_trade_value
            self.trades_history = []
            self.wins_count = 0
            self.losses_count = 0
            self.session_date = datetime.now().strftime("%Y-%m-%d")
            self.enable_trading()
            self.update_display()
    
    def update_display(self):
        self.balance_label.config(text=f"${self.current_balance:.2f}")
        
        daily_target = self.calculate_daily_target()
        stop_loss = self.calculate_stop_loss()
        self.daily_target_label.config(text=f"${daily_target:.2f}")
        self.stop_loss_label.config(text=f"${stop_loss:.2f}")
        
        target_diff = daily_target - self.daily_start_balance
        progress = ((self.current_balance - self.daily_start_balance) / target_diff) * 100 if target_diff > 0 else 0
        self.progress_var.set(max(0, min(100, progress)))
        self.progress_label.config(text=f"PROGRESS: {progress:.1f}%")
        
        self.trade_value_label.config(text=f"TRADE VALUE: ${self.current_trade_value:.2f}")
        self.wins_label.config(text=f"{self.wins_count}")
        self.losses_label.config(text=f"{self.losses_count}")
        
        self.capital_var.set(f"{self.initial_capital:.2f}")
        self.growth_var.set(f"{self.daily_growth_target:.1f}")
        self.stop_loss_var.set(f"{self.stop_loss_limit:.1f}")
        self.multiplier_var.set(f"{self.trade_multiplier:.1f}")
        
        self.update_history_display()
    
    def update_history_display(self):
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, tk.END)
        header = f"{'TIME':<10} {'TYPE':<6} {'AMOUNT':<10} {'BALANCE':<10}\n" + "---" * 15 + "\n" # Shorter dashes
        self.history_text.insert(tk.END, header, 'header')
        
        for trade in reversed(self.trades_history):
            line = f"{trade['timestamp']:<10} {trade['type']:<6} ${trade['amount']:<8.2f} ${trade['balance']:<8.2f}\n"
            tag = "win" if trade['type'] == 'WIN' else "loss"
            self.history_text.insert(tk.END, line, tag)
            
        self.history_text.tag_config('header', font=('Consolas', 10, 'bold'), foreground=self.highlight_color) # Monospaced, neon header
        self.history_text.tag_config('win', foreground=self.win_color) # Neon green win
        self.history_text.tag_config('loss', foreground=self.loss_color) # Neon pink loss
        self.history_text.config(state='disabled')
        self.history_text.see(tk.END)
    
    def save_session(self):
        session_data = {
            'current_balance': self.current_balance, 'daily_start_balance': self.daily_start_balance,
            'current_trade_value': self.current_trade_value, 'trades_history': self.trades_history,
            'wins_count': self.wins_count, 'losses_count': self.losses_count, 'session_date': self.session_date,
            'settings': {
                'initial_capital': self.initial_capital, 'daily_growth_target': self.daily_growth_target,
                'stop_loss_limit': self.stop_loss_limit, 'trade_multiplier': self.trade_multiplier
            }
        }
        try:
            with open('trading_manager_session.json', 'w') as f:
                json.dump(session_data, f, indent=4)
            messagebox.showinfo("SUCCESS", "SESSION DATA LOGGED. ✅") # Cyberpunk message
        except Exception as e:
            messagebox.showerror("ERROR", f"DATA CORRUPTION: FAILED TO SAVE SESSION: {str(e)}") # Cyberpunk message
    
    def load_session(self):
        try:
            if os.path.exists('trading_manager_session.json'):
                with open('trading_manager_session.json', 'r') as f:
                    session_data = json.load(f)
                
                settings = session_data.get('settings', {})
                self.initial_capital = settings.get('initial_capital', 50.0)
                self.daily_growth_target = settings.get('daily_growth_target', 5.0)
                self.stop_loss_limit = settings.get('stop_loss_limit', 5.0)
                self.trade_multiplier = settings.get('trade_multiplier', 1.5)

                self.current_balance = session_data.get('current_balance', self.initial_capital)
                self.daily_start_balance = session_data.get('daily_start_balance', self.initial_capital)
                self.current_trade_value = session_data.get('current_trade_value', self.starting_trade_value)
                self.trades_history = session_data.get('trades_history', [])
                self.wins_count = session_data.get('wins_count', 0)
                self.losses_count = session_data.get('losses_count', 0)
                self.session_date = session_data.get('session_date', datetime.now().strftime("%Y-%m-%d"))
        except Exception as e:
            messagebox.showerror("LOAD ERROR", f"DATA STREAM INTERRUPTED: COULD NOT LOAD SESSION FILE. INITIATING FRESH BOOT.\nERROR: {e}") # Cyberpunk message

def main():
    root = tk.Tk()
    app = ProfessionalTradingManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
