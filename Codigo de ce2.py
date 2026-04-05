import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
import cmath

# --- Nova Classe para o Diagrama Fasorial ---
class PhasorDiagramApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Plano Fasorial")
        self.master.geometry("800x700")
        self.master.transient(master.master) # Make it transient to the main window
        self.master.grab_set() # Make it modal

        self.phasors = [] # List to store phasors: [{'magnitude': m, 'angle': a, 'label': l}]
        self.colors = ["blue", "red", "green", "purple", "orange", "brown", "pink", "gray"] # Cores para os fasores

        self.setup_interface()

    def setup_interface(self):
        # Frame de Controles
        control_frame = ttk.LabelFrame(self.master, text="Controles do Fasor", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10), padx=10)

        ttk.Button(control_frame, text="Adicionar Fasor", command=self.add_phasor_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Editar Fasor Selecionado", command=self.edit_phasor_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Remover Fasor Selecionado", command=self.remove_phasor).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Limpar Todos os Fasores", command=self.clear_phasors).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Plotar Fasores", command=self.plot_phasors).pack(side=tk.LEFT, padx=5)

        # Frame para a lista de fasores
        list_frame = ttk.LabelFrame(self.master, text="Fasores Adicionados", padding="10")
        list_frame.pack(fill=tk.X, pady=(0, 10), padx=10)

        columns = ("Rótulo", "Magnitude", "Ângulo (°)")
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<Double-1>', lambda event: self.edit_phasor_dialog())

        # Frame para o gráfico
        graph_frame = ttk.LabelFrame(self.master, text="Diagrama Fasorial", padding="10")
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update_phasor_list()
        self.plot_phasors()

    def add_phasor_dialog(self):
        self._phasor_input_dialog("Adicionar Novo Fasor", self._add_phasor)

    def edit_phasor_dialog(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um fasor para editar.")
            return
        
        index = self.tree.index(selected_item[0])
        phasor_data = self.phasors[index]
        self._phasor_input_dialog("Editar Fasor", self._edit_phasor, index, phasor_data)

    def _phasor_input_dialog(self, title, callback, index=None, initial_data=None):
        dialog = tk.Toplevel(self.master)
        dialog.title(title)
        dialog.geometry("300x250")
        dialog.transient(self.master)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Magnitude:").pack(anchor=tk.W)
        magnitude_var = tk.StringVar(value=initial_data['magnitude'] if initial_data else "")
        ttk.Entry(frame, textvariable=magnitude_var).pack(fill=tk.X, pady=5)

        ttk.Label(frame, text="Ângulo (°):").pack(anchor=tk.W)
        angle_var = tk.StringVar(value=initial_data['angle'] if initial_data else "")
        ttk.Entry(frame, textvariable=angle_var).pack(fill=tk.X, pady=5)

        ttk.Label(frame, text="Rótulo (opcional):").pack(anchor=tk.W)
        label_var = tk.StringVar(value=initial_data['label'] if initial_data else "")
        ttk.Entry(frame, textvariable=label_var).pack(fill=tk.X, pady=5)

        def on_save():
            try:
                magnitude = float(magnitude_var.get())
                angle = float(angle_var.get())
                label = label_var.get().strip()
                if not label:
                    label = f"{magnitude}∠{angle}°"
                callback(magnitude, angle, label, index)
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

        ttk.Button(frame, text="Salvar", command=on_save).pack(pady=10)
        dialog.bind('<Return>', lambda event: on_save())

    def _add_phasor(self, magnitude, angle, label, _):
        self.phasors.append({'magnitude': magnitude, 'angle': angle, 'label': label})
        self.update_phasor_list()
        self.plot_phasors()

    def _edit_phasor(self, magnitude, angle, label, index):
        self.phasors[index] = {'magnitude': magnitude, 'angle': angle, 'label': label}
        self.update_phasor_list()
        self.plot_phasors()

    def remove_phasor(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um fasor para remover.")
            return
        index = self.tree.index(selected_item[0])
        del self.phasors[index]
        self.update_phasor_list()
        self.plot_phasors()

    def clear_phasors(self):
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja remover todos os fasores?"):
            self.phasors.clear()
            self.update_phasor_list()
            self.plot_phasors()

    def update_phasor_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for phasor in self.phasors:
            self.tree.insert('', 'end', values=(phasor['label'], phasor['magnitude'], phasor['angle']))

    def plot_phasors(self):
        self.ax.clear()
        if not self.phasors:
            self.canvas.draw()
            return

        max_magnitude = 0
        for i, phasor in enumerate(self.phasors):
            magnitude = phasor['magnitude']
            angle_deg = phasor['angle']
            label = phasor['label']

            angle_rad = np.radians(angle_deg)
            complex_phasor = cmath.rect(magnitude, angle_rad)

            color = self.colors[i % len(self.colors)] # Cycle through colors

            self.ax.arrow(0, 0, complex_phasor.real, complex_phasor.imag,
                          head_width=0.05 * magnitude, head_length=0.08 * magnitude,
                          fc=color, ec=color, length_includes_head=True, label=label)
            max_magnitude = max(max_magnitude, magnitude)

        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)

        plot_limit = max_magnitude * 1.2 if max_magnitude > 0 else 1.5
        self.ax.set_xlim(-plot_limit, plot_limit)
        self.ax.set_ylim(-plot_limit, plot_limit)
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.set_xlabel('Eixo Real')
        self.ax.set_ylabel('Eixo Imaginário')
        self.ax.set_title('Diagrama Fasorial')
        self.ax.legend()
        self.canvas.draw()


# --- Classe Principal FasorPlotter  ---
class FasorPlotter:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Funções e Fasores - Circuitos Elétricos")
        self.root.geometry("1000x750")
        
        # Lista para armazenar as funções (ondas senoidais)
        self.funcoes = []
        
        # Variáveis para controle do intervalo de plotagem
        self.angulo_inicial = tk.StringVar(value="0")
        self.angulo_final = tk.StringVar(value="720")
        
        # Configurar a interface
        self.setup_interface()
        
        # Adicionar uma função padrão
        self.adicionar_funcao_padrao()
        
    def setup_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de controles
        control_frame = ttk.LabelFrame(main_frame, text="Controles de Funções", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Primeira linha de controles
        primeira_linha = ttk.Frame(control_frame)
        primeira_linha.pack(fill=tk.X, pady=(0, 10))
        
        # Botão para adicionar função
        ttk.Button(primeira_linha, text="Adicionar Função cos(ωt + θ)", 
                  command=self.abrir_dialog_funcao).pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão para limpar todas as funções
        ttk.Button(primeira_linha, text="Limpar Todas", 
                  command=self.limpar_funcoes).pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão para plotar
        ttk.Button(primeira_linha, text="🔄 Atualizar Gráfico", 
                  command=self.plotar_grafico).pack(side=tk.LEFT, padx=(0, 10))
        
        # NOVO: Botão para abrir o Plano Fasorial
        ttk.Button(primeira_linha, text="Abrir Plano Fasorial", 
                  command=self.open_phasor_diagram).pack(side=tk.LEFT, padx=(0, 10))

        # Segunda linha - Controles de intervalo
        segunda_linha = ttk.Frame(control_frame)
        segunda_linha.pack(fill=tk.X)
        
        # Label para o controle de intervalo
        ttk.Label(segunda_linha, text="Intervalo de plotagem:", 
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        
        # Ângulo inicial
        ttk.Label(segunda_linha, text="De:").pack(side=tk.LEFT, padx=(0, 5))
        angulo_inicial_entry = ttk.Entry(segunda_linha, textvariable=self.angulo_inicial, width=8)
        angulo_inicial_entry.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(segunda_linha, text="°").pack(side=tk.LEFT, padx=(0, 15))
        
        # Ângulo final
        ttk.Label(segunda_linha, text="Até:").pack(side=tk.LEFT, padx=(0, 5))
        angulo_final_entry = ttk.Entry(segunda_linha, textvariable=self.angulo_final, width=8)
        angulo_final_entry.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(segunda_linha, text="°").pack(side=tk.LEFT, padx=(0, 15))
        
        # Botões de preset para intervalos comuns
        ttk.Button(segunda_linha, text="0° a 720°", 
                  command=lambda: self.definir_intervalo(0, 720)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(segunda_linha, text="0° a 360°", 
                  command=lambda: self.definir_intervalo(0, 360)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(segunda_linha, text="-360° a 360°", 
                  command=lambda: self.definir_intervalo(-360, 360)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(segunda_linha, text="-720° a 720°", 
                  command=lambda: self.definir_intervalo(-720, 720)).pack(side=tk.LEFT, padx=(0, 5))
        
        # Bind Enter para atualizar automaticamente
        angulo_inicial_entry.bind('<Return>', lambda event: self.plotar_grafico())
        angulo_final_entry.bind('<Return>', lambda event: self.plotar_grafico())
        
        # Frame para lista de funções
        list_frame = ttk.LabelFrame(main_frame, text="Funções Adicionadas", padding="10")
        list_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Treeview para mostrar as funções
        columns = ("Função", "ω (rad/s)", "θ (graus)", "Amplitude")
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=6)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        # Scrollbar para a treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para botões de ação
        action_frame = ttk.Frame(list_frame)
        action_frame.pack(pady=(10, 0), fill=tk.X)
        
        # Botões de ação
        ttk.Button(action_frame, text="✏️ Editar Selecionada", 
                  command=self.editar_funcao).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="🗑️ Remover Selecionada", 
                  command=self.remover_funcao).pack(side=tk.LEFT)
        
        # Permitir duplo clique para editar
        self.tree.bind('<Double-1>', lambda event: self.editar_funcao())
        
        # Frame para o gráfico
        graph_frame = ttk.LabelFrame(main_frame, text="Gráfico", padding="10")
        graph_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurar matplotlib
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def definir_intervalo(self, inicial, final):
        """Define o intervalo de plotagem"""
        self.angulo_inicial.set(str(inicial))
        self.angulo_final.set(str(final))
        self.plotar_grafico()
        
    def abrir_dialog_funcao(self):
        """Abre dialog para adicionar nova função"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Adicionar Função")
        dialog.geometry("450x400")
        dialog.resizable(False, False)
        
        # Centralizar o dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Frame principal do dialog
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(frame, text="Adicionar função: A·cos(ωt + θ)", 
                 font=("Arial", 12, "bold")).pack(pady=(0, 20))
        
        # Amplitude
        ttk.Label(frame, text="Amplitude (A):").pack(anchor=tk.W)
        amplitude_var = tk.StringVar(value="1")
        ttk.Entry(frame, textvariable=amplitude_var, width=20).pack(pady=(0, 10), fill=tk.X)
        
        # Frequência angular
        ttk.Label(frame, text="Frequência angular ω (rad/s):").pack(anchor=tk.W)
        omega_var = tk.StringVar(value="1")
        ttk.Entry(frame, textvariable=omega_var, width=20).pack(pady=(0, 10), fill=tk.X)
        
        # Ângulo de fase
        ttk.Label(frame, text="Ângulo de fase θ (graus):").pack(anchor=tk.W)
        ttk.Label(frame, text="(Ex: 90.2 para 90.2°, -45 para -45°)", 
                 font=("Arial", 8)).pack(anchor=tk.W)
        theta_var = tk.StringVar(value="0")
        ttk.Entry(frame, textvariable=theta_var, width=20).pack(pady=(0, 10), fill=tk.X)
        
        # Label (opcional)
        ttk.Label(frame, text="Rótulo da função (opcional):").pack(anchor=tk.W)
        label_var = tk.StringVar()
        ttk.Entry(frame, textvariable=label_var, width=20).pack(pady=(0, 20), fill=tk.X)
        
        # Função para adicionar
        def adicionar():
            try:
                A = float(amplitude_var.get())
                w = float(omega_var.get())
                theta = float(theta_var.get())
                label = label_var.get().strip()
                
                if not label:
                    label = f"{A}·cos({w}t + {theta}°)"
                
                self.funcoes.append({
                    'amplitude': A,
                    'omega': w,
                    'theta': theta,
                    'label': label
                })
                
                self.atualizar_lista()
                dialog.destroy()
                messagebox.showinfo("Sucesso", f"Função '{label}' adicionada com sucesso!\nClique em 'Atualizar Gráfico' para visualizar.")
                
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
        
        # Frame para os botões
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Botões com espaçamento adequado
        btn_adicionar = ttk.Button(button_frame, text="✓ Adicionar Função", command=adicionar)
        btn_adicionar.pack(side=tk.LEFT, padx=(0, 10), ipadx=10, ipady=5)
        
        btn_cancelar = ttk.Button(button_frame, text="✗ Cancelar", command=dialog.destroy)
        btn_cancelar.pack(side=tk.LEFT, ipadx=10, ipady=5)
        
        # Permitir Enter para adicionar
        dialog.bind('<Return>', lambda event: adicionar())
        
    def adicionar_funcao_padrao(self):
        """Adiciona uma função padrão para exemplo"""
        self.funcoes.append({
            'amplitude': 1,
            'omega': 1,
            'theta': 0,
            'label': 'Tensão: cos(t)'
        })
        self.funcoes.append({
            'amplitude': 1,
            'omega': 1,
            'theta': -30,
            'label': 'Corrente: cos(t - 30°)'
        })
        self.atualizar_lista()
        self.plotar_grafico()
    
    def atualizar_lista(self):
        """Atualiza a lista de funções na interface"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for func in self.funcoes:
            self.tree.insert('', 'end', values=(
                func['label'],
                func['omega'],
                func['theta'],
                func['amplitude']
            ))
    
    def editar_funcao(self):
        """Edita a função selecionada"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma função para editar.")
            return
        
        index = self.tree.index(selected[0])
        func_atual = self.funcoes[index]
        
        # Criar dialog de edição (similar ao de adição)
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Função")
        dialog.geometry("450x400")
        dialog.resizable(False, False)
        
        # Centralizar o dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Frame principal do dialog
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        ttk.Label(main_frame, text="Editar função: A·cos(ωt + θ)", 
                 font=("Arial", 12, "bold")).pack(pady=(0, 20))
        
        # Frame para os campos
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill=tk.BOTH, expand=True)
        
        # Amplitude (com valor atual)
        ttk.Label(fields_frame, text="Amplitude (A):").pack(anchor=tk.W, pady=(0, 5))
        amplitude_var = tk.StringVar(value=str(func_atual['amplitude']))
        ttk.Entry(fields_frame, textvariable=amplitude_var, width=30).pack(fill=tk.X, pady=(0, 15))
        
        # Frequência angular (com valor atual)
        ttk.Label(fields_frame, text="Frequência angular ω (rad/s):").pack(anchor=tk.W, pady=(0, 5))
        omega_var = tk.StringVar(value=str(func_atual['omega']))
        ttk.Entry(fields_frame, textvariable=omega_var, width=30).pack(fill=tk.X, pady=(0, 15))
        
        # Ângulo de fase (com valor atual)
        ttk.Label(fields_frame, text="Ângulo de fase θ (graus):").pack(anchor=tk.W, pady=(0, 5))
        ttk.Label(fields_frame, text="(Ex: 90.2 para 90.2°, -45 para -45°)", 
                 font=("Arial", 8)).pack(anchor=tk.W)
        theta_var = tk.StringVar(value=str(func_atual['theta']))
        ttk.Entry(fields_frame, textvariable=theta_var, width=30).pack(fill=tk.X, pady=(0, 15))
        
        # Label (com valor atual)
        ttk.Label(fields_frame, text="Rótulo da função (opcional):").pack(anchor=tk.W, pady=(0, 5))
        label_var = tk.StringVar(value=func_atual['label'])
        ttk.Entry(fields_frame, textvariable=label_var, width=30).pack(fill=tk.X, pady=(0, 20))
        
        # Função para salvar alterações
        def salvar_alteracoes():
            try:
                A = float(amplitude_var.get())
                w = float(omega_var.get())
                theta = float(theta_var.get())
                label = label_var.get().strip()
                
                if not label:
                    label = f"{A}·cos({w}t + {theta}°)"
                
                # Atualizar a função na lista
                self.funcoes[index] = {
                    'amplitude': A,
                    'omega': w,
                    'theta': theta,
                    'label': label
                }
                
                self.atualizar_lista()
                dialog.destroy()
                messagebox.showinfo("Sucesso", f"Função '{label}' editada com sucesso!\nClique em 'Atualizar Gráfico' para visualizar as mudanças.")
                
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
        
        # Frame fixo para os botões na parte inferior
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        # Botões grandes e visíveis
        btn_salvar = ttk.Button(button_frame, text="💾 SALVAR", 
                               command=salvar_alteracoes, width=20)
        btn_salvar.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_cancelar = ttk.Button(button_frame, text="✗ CANCELAR", 
                                 command=dialog.destroy, width=20)
        btn_cancelar.pack(side=tk.LEFT)
        
        # Focar no primeiro campo
        dialog.after(100, lambda: fields_frame.winfo_children()[1].focus())
        
        # Atalhos de teclado
        dialog.bind('<Return>', lambda event: salvar_alteracoes())
        dialog.bind('<Escape>', lambda event: dialog.destroy())

    def remover_funcao(self):
        """Remove a função selecionada"""
        selected = self.tree.selection()
        if selected:
            index = self.tree.index(selected[0])
            del self.funcoes[index]
            self.atualizar_lista()
            messagebox.showinfo("Removido", "Função removida! Clique em 'Atualizar Gráfico' para visualizar as mudanças.")
        else:
            messagebox.showwarning("Aviso", "Selecione uma função para remover.")
    
    def limpar_funcoes(self):
        """Remove todas as funções"""
        if self.funcoes:
            self.funcoes.clear()
            self.atualizar_lista()
            self.ax.clear()
            self.canvas.draw()
            messagebox.showinfo("Limpo", "Todas as funções foram removidas!")
        else:
            messagebox.showinfo("Aviso", "Não há funções para remover.")
    
    def plotar_grafico(self):
        """Plota o gráfico com todas as funções"""
        if not self.funcoes:
            messagebox.showwarning("Aviso", "Adicione pelo menos uma função para plotar.")
            return
        
        # Validar os valores de intervalo
        try:
            angulo_min = float(self.angulo_inicial.get())
            angulo_max = float(self.angulo_final.get())
            
            if angulo_min >= angulo_max:
                messagebox.showerror("Erro", "O ângulo inicial deve ser menor que o ângulo final.")
                return
                
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos para os ângulos.")
            return
        
        self.ax.clear()
        
        # Definir o range de tempo baseado nos ângulos especificados
        # Converter graus para radianos para os cálculos
        t_rad_min = np.radians(angulo_min)
        t_rad_max = np.radians(angulo_max)
        
        # Criar um array com mais pontos para suavidade, proporcional ao intervalo
        num_pontos = max(1000, int(abs(angulo_max - angulo_min) * 3))  # Mais pontos para intervalos maiores
        t_rad = np.linspace(t_rad_min, t_rad_max, num_pontos)
        t_deg = np.degrees(t_rad)  # Converter para graus para o eixo x
        
        # Cores para as diferentes funções
        cores = ["blue", "red", "green", "orange", "purple", "brown", "pink", "gray"]
        
        for i, func in enumerate(self.funcoes):
            A = func['amplitude']
            w = func['omega']
            theta_deg = func['theta']
            theta_rad = np.radians(theta_deg)  # Converter para radianos
            label = func['label']
            
            # Calcular a função
            y = A * np.cos(w * t_rad + theta_rad)
            
            # Plotar
            cor = cores[i % len(cores)]
            self.ax.plot(t_deg, y, label=label, color=cor, linewidth=2)
        
        # Configurar o gráfico
        self.ax.set_xlabel('Ângulo (graus)', fontsize=12)
        self.ax.set_ylabel('Amplitude', fontsize=12)
        self.ax.set_title(f'Análise de Funções - Intervalo: {angulo_min}° a {angulo_max}°', 
                         fontsize=14, fontweight='bold')
        self.ax.grid(True, linestyle='--', alpha=0.3)
        self.ax.legend()
        
        # Configurar os ticks do eixo x de forma inteligente
        intervalo_total = angulo_max - angulo_min
        
        if intervalo_total <= 360:
            step = 30  # A cada 30 graus para intervalos pequenos
        elif intervalo_total <= 720:
            step = 45  # A cada 45 graus para intervalos médios
        elif intervalo_total <= 1440:
            step = 90  # A cada 90 graus para intervalos grandes
        else:
            step = 180  # A cada 180 graus para intervalos muito grandes
        
        # Calcular os ticks
        tick_inicial = int(angulo_min // step) * step
        if tick_inicial < angulo_min:
            tick_inicial += step
        
        ticks = []
        tick_atual = tick_inicial
        while tick_atual <= angulo_max:
            ticks.append(tick_atual)
            tick_atual += step
        
        if ticks:
            self.ax.set_xticks(ticks)
            
            # Adicionar linhas verticais para facilitar a leitura
            for x in ticks:
                if angulo_min <= x <= angulo_max:
                    self.ax.axvline(x=x, color='gray', linestyle='--', alpha=0.3)
        
        # Definir os limites do eixo x
        self.ax.set_xlim(angulo_min, angulo_max)
        
        self.canvas.draw()

    def open_phasor_diagram(self):
        phasor_window = tk.Toplevel(self.root)
        PhasorDiagramApp(phasor_window)

def main():
    root = tk.Tk()
    app = FasorPlotter(root)
    root.mainloop()

if __name__ == "__main__":
    main()

