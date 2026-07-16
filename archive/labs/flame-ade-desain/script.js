/**
 * Flame ADE — Landing Page Interactions
 * Vanilla JS — zero dependencies
 */
document.addEventListener('DOMContentLoaded', () => {

  /* ═══════════════════════════════════════════
   * 1. TERMINAL TYPING ANIMATION
   * ═══════════════════════════════════════════ */
  const terminalLines = [
    { type: 'command', text: 'brew install flame-ade' },
    { type: 'output',  text: 'Downloading flame-ade@1.1.0...' },
    { type: 'output',  text: '📦 Package size: 6.8 MB' },
    { type: 'success', text: '✓ Installed successfully' },
    { type: 'command', text: 'flame-ade --version' },
    { type: 'info',    text: 'Flame ADE v1.1.0 (Tauri 2 + Rust + React 19)' },
    { type: 'command', text: 'flame-ade .' },
    { type: 'success', text: '🔥 Flame ADE is running — http://localhost:1420' },
    { type: 'output',  text: '' },
    { type: 'info',    text: '  Terminal    ✓  xterm.js + WebGL' },
    { type: 'info',    text: '  Editor      ✓  CodeMirror 6' },
    { type: 'info',    text: '  AI Panel    ✓  BYOK ready' },
    { type: 'info',    text: '  Explorer    ✓  loaded' },
    { type: 'info',    text: '  Git         ✓  connected' },
    { type: 'output',  text: '' },
    { type: 'success', text: '✓ All systems operational' }
  ];

  const terminalBody = document.getElementById('terminal-body');
  let terminalAnimating = false;
  let terminalTimeout = null;

  const sleep = (ms) => new Promise(r => setTimeout(r, ms));

  const clearTerminal = () => {
    if (terminalBody) terminalBody.innerHTML = '';
  };

  const addTerminalLine = (type, text) => {
    const line = document.createElement('div');
    line.className = 'terminal-line';

    if (type === 'command') {
      const prompt = document.createElement('span');
      prompt.className = 'terminal-prompt';
      prompt.textContent = '❯';
      line.appendChild(prompt);
    }

    const span = document.createElement('span');
    span.className = `typed-text terminal-${type}`;
    span.textContent = text;
    line.appendChild(span);

    terminalBody.appendChild(line);
    terminalBody.scrollTop = terminalBody.scrollHeight;
    return span;
  };

  const typeText = async (element, text, speed = 30) => {
    for (let i = 0; i < text.length; i++) {
      element.textContent = text.substring(0, i + 1);
      await sleep(speed);
    }
  };

  const runTerminalAnimation = async () => {
    if (!terminalBody || terminalAnimating) return;
    terminalAnimating = true;

    while (terminalAnimating) {
      clearTerminal();

      for (const line of terminalLines) {
        if (!terminalAnimating) return;

        if (line.type === 'command') {
          const span = addTerminalLine('command', '');
          await typeText(span, line.text, 30);
          await sleep(200);
        } else {
          addTerminalLine(line.type, line.text);
          await sleep(line.text ? 80 : 30);
        }
      }

      // Add blinking cursor at end
      const cursorLine = document.createElement('div');
      cursorLine.className = 'terminal-line';
      const prompt = document.createElement('span');
      prompt.className = 'terminal-prompt';
      prompt.textContent = '❯';
      cursorLine.appendChild(prompt);
      const cursor = document.createElement('span');
      cursor.className = 'terminal-cursor';
      cursorLine.appendChild(cursor);
      terminalBody.appendChild(cursorLine);

      // Wait before restart
      await sleep(4000);
    }
  };

  // Start animation when terminal is visible
  if (terminalBody) {
    const terminalObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !terminalAnimating) {
          runTerminalAnimation();
        } else if (!entry.isIntersecting) {
          terminalAnimating = false;
        }
      });
    }, { threshold: 0.3 });

    terminalObserver.observe(terminalBody);
  }


  /* ═══════════════════════════════════════════
   * 2. STATS COUNTER ANIMATION
   * ═══════════════════════════════════════════ */
  const animateCounter = (el) => {
    const target = parseInt(el.dataset.value, 10);
    const suffix = el.dataset.suffix || '';
    const duration = 2000;
    const startTime = performance.now();

    const easeOut = (t) => 1 - Math.pow(1 - t, 3);

    const update = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easedProgress = easeOut(progress);
      const current = Math.round(easedProgress * target);

      el.textContent = current + suffix;

      if (progress < 1) {
        requestAnimationFrame(update);
      }
    };

    requestAnimationFrame(update);
  };

  const statValues = document.querySelectorAll('.stat-value');
  if (statValues.length) {
    const statsObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          statsObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    statValues.forEach(el => statsObserver.observe(el));
  }


  /* ═══════════════════════════════════════════
   * 3. SMOOTH SCROLL NAVIGATION
   * ═══════════════════════════════════════════ */
  const NAVBAR_HEIGHT = 72;

  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      if (href === '#') return;

      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        const top = target.getBoundingClientRect().top + window.scrollY - NAVBAR_HEIGHT;
        window.scrollTo({ top, behavior: 'smooth' });

        // Close mobile menu if open
        navLinks?.classList.remove('active');
        navToggle?.classList.remove('active');
      }
    });
  });

  // Update active nav link on scroll
  const sections = document.querySelectorAll('section[id]');
  const navAnchors = document.querySelectorAll('.nav-links a[href^="#"]');

  const updateActiveNav = () => {
    const scrollY = window.scrollY + NAVBAR_HEIGHT + 100;

    sections.forEach(section => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      const id = section.getAttribute('id');

      if (scrollY >= top && scrollY < top + height) {
        navAnchors.forEach(a => {
          a.classList.remove('active');
          if (a.getAttribute('href') === `#${id}`) {
            a.classList.add('active');
          }
        });
      }
    });
  };


  /* ═══════════════════════════════════════════
   * 4. NAVBAR SCROLL EFFECT
   * ═══════════════════════════════════════════ */
  const navbar = document.getElementById('navbar');

  const handleScroll = () => {
    if (window.scrollY > 50) {
      navbar?.classList.add('scrolled');
    } else {
      navbar?.classList.remove('scrolled');
    }
    updateActiveNav();
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll(); // Initial check


  /* ═══════════════════════════════════════════
   * 5. REVEAL ON SCROLL (JS FALLBACK)
   * ═══════════════════════════════════════════ */
  const supportsScrollTimeline = CSS.supports('animation-timeline', 'view()');

  if (!supportsScrollTimeline) {
    const revealElements = document.querySelectorAll('.reveal-on-scroll');

    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    revealElements.forEach(el => revealObserver.observe(el));
  }


  /* ═══════════════════════════════════════════
   * 6. MOBILE MENU TOGGLE
   * ═══════════════════════════════════════════ */
  const navToggle = document.getElementById('nav-toggle');
  const navLinks = document.getElementById('nav-links');

  navToggle?.addEventListener('click', () => {
    navToggle.classList.toggle('active');
    navLinks?.classList.toggle('active');
  });

  // Close on link click
  navLinks?.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navToggle?.classList.remove('active');
      navLinks?.classList.remove('active');
    });
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (navLinks?.classList.contains('active') &&
        !navLinks.contains(e.target) &&
        !navToggle?.contains(e.target)) {
      navToggle?.classList.remove('active');
      navLinks?.classList.remove('active');
    }
  });


  /* ═══════════════════════════════════════════
   * 7. HERO PARTICLES (subtle floating dots)
   * ═══════════════════════════════════════════ */
  const particlesContainer = document.getElementById('hero-particles');
  if (particlesContainer) {
    for (let i = 0; i < 20; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.cssText = `
        left: ${Math.random() * 100}%;
        top: ${Math.random() * 100}%;
        width: ${2 + Math.random() * 4}px;
        height: ${2 + Math.random() * 4}px;
        animation-delay: ${Math.random() * 6}s;
        animation-duration: ${4 + Math.random() * 4}s;
        opacity: ${0.15 + Math.random() * 0.35};
      `;
      particlesContainer.appendChild(particle);
    }
  }

});
