// theme.js - Funções específicas para gerenciar o tema da aplicação

class ThemeManager {
  constructor() {
    this.themeKey = "theme";
    this.defaultTheme = "dark";
    this.toggleBtn = document.getElementById("theme-toggle");
    this.darkIcon = document.getElementById("dark-theme-icon");
    this.lightIcon = document.getElementById("light-theme-icon");

    // Inicializa o tema
    this.init();
  }

  init() {
    // Carrega o tema ao iniciar a página
    document.addEventListener("DOMContentLoaded", () => {
      this.loadTheme();
      this.setupListeners();
    });
  }

  loadTheme() {
    // Carrega o tema salvo ou usa o padrão
    const savedTheme = localStorage.getItem(this.themeKey) || this.defaultTheme;
    this.applyTheme(savedTheme);
  }

  setupListeners() {
    // Configura o listener para o botão de toggle
    if (this.toggleBtn) {
      this.toggleBtn.addEventListener("click", () => this.toggleTheme());
    }
  }

  toggleTheme() {
    // Alterna entre os temas
    const currentTheme = document.documentElement.getAttribute("data-bs-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";

    this.applyTheme(newTheme);
    this.saveTheme(newTheme);

    // Dispara evento customizado para notificar mudança de tema
    document.dispatchEvent(
      new CustomEvent("themeChanged", {
        detail: { theme: newTheme },
      })
    );

    console.log("Tema alterado para:", newTheme);
  }

  applyTheme(theme) {
    // Aplica o tema ao HTML e atualiza os ícones
    document.documentElement.setAttribute("data-bs-theme", theme);

    // Atualiza classes no body para estilos específicos
    document.body.classList.remove("theme-dark", "theme-light");
    document.body.classList.add("theme-" + theme);

    // Atualiza ícones
    if (this.darkIcon && this.lightIcon) {
      if (theme === "dark") {
        this.darkIcon.classList.remove("d-none");
        this.lightIcon.classList.add("d-none");
      } else {
        this.darkIcon.classList.add("d-none");
        this.lightIcon.classList.remove("d-none");
      }
    }
  }

  saveTheme(theme) {
    // Salva a preferência no localStorage
    localStorage.setItem(this.themeKey, theme);
  }
}

// Inicia o gerenciador de temas
const themeManager = new ThemeManager();
