document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. LÓGICA DEL FORMULARIO DE CONTACTO ---
    const form = document.getElementById('contact-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('CONEXIÓN ESTABLECIDA: Datos enviados al sistema de Fernando Orellana.');
            form.reset();
        });
    }

    // --- 2. SINTETIZADOR DE AUDIO RETRO DE 8 BITS (EXCLUSIVO 1982) ---
    function play8BitSound(frequency, duration, type = 'square') {
        if (!document.body.classList.contains('theme-1982')) return;

        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            const audioCtx = new AudioContext();
            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();

            oscillator.type = type; 
            oscillator.frequency.value = frequency;

            gainNode.gain.setValueAtTime(0.04, audioCtx.currentTime); 
            gainNode.gain.exponentialRampToValueAtTime(0.00001, audioCtx.currentTime + duration);

            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);

            oscillator.start();
            oscillator.stop(audioCtx.currentTime + duration);
        } catch (e) {
            console.log("Audio deshabilitado por el navegador");
        }
    }

    // --- INTERRUPTOR DE RED (TRON 1982 vs 2010) ---
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('theme-1982');
            if (document.body.classList.contains('theme-1982')) {
                themeToggle.textContent = 'SISTEMA: 1982';
                themeToggle.style.borderColor = 'var(--tron-orange)';
                themeToggle.style.color = 'var(--tron-orange)';
                
                // Arpegio de arranque electrónico
                play8BitSound(200, 0.1);
                setTimeout(() => play8BitSound(400, 0.1), 80);
                setTimeout(() => play8BitSound(800, 0.2), 160);
            } else {
                themeToggle.textContent = 'SISTEMA: 2010';
                themeToggle.style.borderColor = 'var(--tron-blue)';
                themeToggle.style.color = 'var(--tron-blue)';
            }
        });
    }

    // Sonido táctil en botones para el modo 1982
    document.querySelectorAll('.btn-tron, .nav-links a').forEach(btn => {
        btn.addEventListener('click', () => {
            play8BitSound(900, 0.05, 'square');
        });
    });

    // --- 3. MENÚ HAMBURGUESA ---
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const links = document.querySelectorAll('.nav-links li a');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navLinks.classList.toggle('active');
        });

        links.forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
            });
        });
    }

    // --- 4. PREPARACIÓN PARA EFECTO DE ESCRITURA GLOBAL ---
    const textElements = document.querySelectorAll('.bio, .section-title, .job-title, .company, .skill-card label, .input-group label');

    textElements.forEach(el => {
        el.dataset.originalText = el.textContent.trim();
        el.textContent = ''; 
    });

    // --- 5. FUNCIÓN MÁQUINA DE ESCRIBIR ---
    function startTypingEffect(element) {
        element.classList.add('typing-started');
        const text = element.dataset.originalText;
        let index = 0;
        
        function type() {
            if (index < text.length) {
                element.textContent += text.charAt(index);
                index++;
                setTimeout(type, 15); 
            } else {
                element.classList.remove('typing-started');
                element.classList.add('typing-complete');
            }
        }
        type();
    }

    // --- 6. OBSERVADOR DE SCROLL (INTERSECTION OBSERVER) ---
    const containersToReveal = document.querySelectorAll('.skill-card, .experience-card, .hero-image, .contact-form');
    
    containersToReveal.forEach(el => el.classList.add('reveal'));
    textElements.forEach(el => el.classList.add('reveal'));

    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                
                if (entry.target.dataset.originalText && !entry.target.classList.contains('typing-complete') && !entry.target.classList.contains('typing-started')) {
                    startTypingEffect(entry.target);
                }
            }
        });
    }, observerOptions);

    containersToReveal.forEach(el => observer.observe(el));
    textElements.forEach(el => observer.observe(el));

    // --- 7. DESPLAZAMIENTO SUAVE (SMOOTH SCROLL) ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 70,
                    behavior: 'smooth'
                });
            }
        });
    });
});