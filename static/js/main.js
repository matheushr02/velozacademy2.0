// main.js - Funções JavaScript para o site VelozAcademy

// Função para verificar quando elementos estão visíveis durante o scroll
function onElementVisible(element, callback) {
    // Cria um novo Intersection Observer
    let observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                callback(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    // Se o elemento é um seletor de string, converte para um array de elementos
    if (typeof element === 'string') {
        document.querySelectorAll(element).forEach(el => observer.observe(el));
    } else {
        observer.observe(element);
    }
}

// Função para atualizar estilos específicos após mudança de tema
function refreshComponentsAfterThemeChange(theme) {
    console.log('Atualizando componentes para tema:', theme);
    
    // Força reatribuição de estilos em componentes específicos
    document.querySelectorAll('.card').forEach(card => {
        // Garante que a opacidade é mantida após a mudança de tema
        if (card.style.opacity !== '1') {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }
    });
}

// Aplica animações e configurações iniciais
document.addEventListener('DOMContentLoaded', function() {
    // Adiciona animação de fade-in aos cards
    onElementVisible('.card', (card) => {
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100);
    });

    // Evento para mudança de tema
    document.addEventListener('themeChanged', function(e) {
        setTimeout(() => refreshComponentsAfterThemeChange(e.detail.theme), 100);
    });

    // Verifica se há notificações para mostrar (exemplo)
    checkNotifications();
});

// Função exemplo para verificar notificações
function checkNotifications() {
    // Simulação de uma notificação
    // Na implementação real, isso viria de uma API
    console.log('Verificando notificações...');
}

/*
- Comentei para futuro uso em outra página, agora causa conflito por enquanto
// Adiciona comportamento de sticky header
window.addEventListener('scroll', function() {
    let header = document.querySelector('header');
    if (header) {
        // Verifica se o header existe antes de aplicar a classe
        if (window.scrollY > 50) {
            header.classList.add('shadow-sm');
        } else {
            header.classList.remove('shadow-sm');
        }
    }
}); 
*/

//+ Sidebar botão clicavel no mobile
document.addEventListener('DOMContentLoaded', function() {
    //? checa se o sidebar botão clicável existe
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
            ////document.querySelector('.sidebar').classList.toggle('active');
            document.body.classList.toggle('sidebar-active');
            
        });
        //todo Adicionar animação de transição ao abrir/fechar a sidebar
    }

    if (overlay) {
        overlay.addEventListener('click', function() {
            sidebar.classList.remove('active');
            document.body.classList.remove('sidebar-active');
        });
    }

    //? fecha a sidebar quando clicado no item menu no mobile
    const menuLinks = document.querySelectorAll('.sidebar .nav-link');
    if (window.innerWidth <= 576) {
        menuLinks.forEach(link => {
            link.addEventListener('click', function() {
                sidebar.classList.remove('active');
                document.body.classList.remove('sidebar-active');
            });
        });
    }
});