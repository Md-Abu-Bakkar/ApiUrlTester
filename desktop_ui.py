import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import threading
from api_tester import APITester
from data_manager import DataManager
from utils.helpers import validate_url

class ModernAPIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal API Tester - Professional Edition")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0f0f23')
        
        # Apply modern dark theme
        self.setup_styles()
        self.create_widgets()
        self.data_manager = DataManager()
        self.api_tester = APITester()
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors for dark theme
        bg_color = '#0f0f23'
        accent_color = '#00ff88'
        secondary_bg = '#1a1a2e'
        text_color = '#ffffff'
        
        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TLabel', background=bg_color, foreground=text_color, font=('Arial', 10))
        self.style.configure('TButton', background=accent_color, foreground='black', 
                           font=('Arial', 10, 'bold'), borderwidth=0)
        self.style.configure('TEntry', fieldbackground=secondary_bg, foreground=text_color)
        self.style.configure('TCombobox', fieldbackground=secondary_bg, foreground=text_color)
        self.style.configure('TNotebook', background=bg_color)
        self.style.configure('TNotebook.Tab', background=secondary_bg, foreground=text_color)
        
    def create_widgets(self):
        # Main container with gradient effect
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="🚀 Universal API Tester", 
                               font=('Arial', 24, 'bold'), foreground='#00ff88')
        title_label.pack(side=tk.LEFT)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # API Testing Tab
        self.create_api_tab()
        
        # Configuration Tab
        self.create_config_tab()
        
        # Results Tab
        self.create_results_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, style='TLabel')
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
    def create_api_tab(self):
        api_frame = ttk.Frame(self.notebook)
        self.notebook.add(api_frame, text="API Testing")
        
        # URL Section
        url_frame = ttk.LabelFrame(api_frame, text="API Endpoint", padding=10)
        url_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(url_frame, text="URL:").grid(row=0, column=0, sticky='w', pady=5)
        self.url_entry = ttk.Entry(url_frame, width=80)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # Method selection
        ttk.Label(url_frame, text="Method:").grid(row=1, column=0, sticky='w', pady=5)
        self.method_var = tk.StringVar(value="GET")
        method_combo = ttk.Combobox(url_frame, textvariable=self.method_var, 
                                   values=["GET", "POST", "PUT", "DELETE"], state="readonly")
        method_combo.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        # Headers Section
        headers_frame = ttk.LabelFrame(api_frame, text="Headers", padding=10)
        headers_frame.pack(fill=tk.X, pady=5)
        
        self.headers_text = scrolledtext.ScrolledText(headers_frame, height=4, width=80,
                                                     bg='#1a1a2e', fg='white', insertbackground='white')
        self.headers_text.pack(fill=tk.X)
        self.headers_text.insert('1.0', '{"Content-Type": "application/json"}')
        
        # Body Section (for POST/PUT)
        body_frame = ttk.LabelFrame(api_frame, text="Request Body", padding=10)
        body_frame.pack(fill=tk.X, pady=5)
        
        self.body_text = scrolledtext.ScrolledText(body_frame, height=6, width=80,
                                                  bg='#1a1a2e', fg='white', insertbackground='white')
        self.body_text.pack(fill=tk.X)
        
        # Control buttons
        button_frame = ttk.Frame(api_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        test_btn = ttk.Button(button_frame, text="🚀 Test API", command=self.test_api)
        test_btn.pack(side=tk.LEFT, padx=5)
        
        save_btn = ttk.Button(button_frame, text="💾 Save Config", command=self.save_config)
        save_btn.pack(side=tk.LEFT, padx=5)
        
    def create_config_tab(self):
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="Configuration")
        
        # Authentication section
        auth_frame = ttk.LabelFrame(config_frame, text="Authentication", padding=10)
        auth_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(auth_frame, text="Username:").grid(row=0, column=0, sticky='w', pady=5)
        self.username_entry = ttk.Entry(auth_frame, width=40)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Label(auth_frame, text="Password:").grid(row=1, column=0, sticky='w', pady=5)
        self.password_entry = ttk.Entry(auth_frame, width=40, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Label(auth_frame, text="API Token:").grid(row=2, column=0, sticky='w', pady=5)
        self.token_entry = ttk.Entry(auth_frame, width=40)
        self.token_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        # Telegram Bot section
        telegram_frame = ttk.LabelFrame(config_frame, text="Telegram Bot", padding=10)
        telegram_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(telegram_frame, text="Bot Token:").grid(row=0, column=0, sticky='w', pady=5)
        self.bot_token_entry = ttk.Entry(telegram_frame, width=40)
        self.bot_token_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # Load existing config
        self.load_config()
        
    def create_results_tab(self):
        results_frame = ttk.Frame(self.notebook)
        self.notebook.add(results_frame, text="Results")
        
        # Response display
        response_frame = ttk.LabelFrame(results_frame, text="API Response", padding=10)
        response_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.response_text = scrolledtext.ScrolledText(response_frame, height=20, width=80,
                                                      bg='#1a1a2e', fg='#00ff88', 
                                                      font=('Consolas', 10))
        self.response_text.pack(fill=tk.BOTH, expand=True)
        
    def test_api(self):
        url = self.url_entry.get().strip()
        if not validate_url(url):
            messagebox.showerror("Error", "Please enter a valid URL")
            return
            
        self.status_var.set("Testing API...")
        
        # Get request data
        headers = self.get_headers()
        body = self.get_body()
        
        # Run in thread to prevent UI freeze
        thread = threading.Thread(target=self.execute_api_test, 
                                args=(url, self.method_var.get(), headers, body))
        thread.daemon = True
        thread.start()
        
    def execute_api_test(self, url, method, headers, body):
        try:
            response = self.api_tester.test_endpoint(url, method, headers, body)
            
            # Update UI in main thread
            self.root.after(0, self.display_results, response)
            
            # Save results
            self.data_manager.save_response(response)
            
            self.root.after(0, lambda: self.status_var.set("API Test Completed"))
            
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            
    def display_results(self, response):
        self.response_text.delete('1.0', tk.END)
        self.response_text.insert('1.0', json.dumps(response, indent=2))
        
    def get_headers(self):
        try:
            headers_text = self.headers_text.get('1.0', tk.END).strip()
            return json.loads(headers_text) if headers_text else {}
        except:
            return {}
            
    def get_body(self):
        try:
            body_text = self.body_text.get('1.0', tk.END).strip()
            return json.loads(body_text) if body_text else {}
        except:
            return {}
            
    def save_config(self):
        config = {
            'username': self.username_entry.get(),
            'password': self.password_entry.get(),
            'api_token': self.token_entry.get(),
            'telegram_bot_token': self.bot_token_entry.get()
        }
        
        try:
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=2)
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {str(e)}")
            
    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, config.get('username', ''))
            
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, config.get('password', ''))
            
            self.token_entry.delete(0, tk.END)
            self.token_entry.insert(0, config.get('api_token', ''))
            
            self.bot_token_entry.delete(0, tk.END)
            self.bot_token_entry.insert(0, config.get('telegram_bot_token', ''))
            
        except FileNotFoundError:
            pass  # Config file doesn't exist yet

def run_desktop_ui():
    root = tk.Tk()
    app = ModernAPIApp(root)
    root.mainloop()