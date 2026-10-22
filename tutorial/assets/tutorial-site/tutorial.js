(() => {
  const storagePrefix = `rust-tutorial:${document.documentElement.dataset.tutorialId}`;
  const safelyRead = key => { try { return localStorage.getItem(key); } catch { return null; } };
  const safelyWrite = (key, value) => { try { localStorage.setItem(key, value); } catch { /* Reading works without storage. */ } };
  const themeButton = document.getElementById('theme-toggle');
  const setTheme = theme => {
    document.documentElement.dataset.theme = theme;
    themeButton.textContent = theme === 'dark' ? 'Light theme' : 'Dark theme';
    themeButton.setAttribute('aria-pressed', String(theme === 'dark'));
  };
  setTheme(safelyRead(`${storagePrefix}:theme`) === 'dark' ? 'dark' : 'light');
  themeButton.addEventListener('click', () => {
    const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    setTheme(theme);
    safelyWrite(`${storagePrefix}:theme`, theme);
  });
  document.getElementById('print').addEventListener('click', () => window.print());
  const checks = [...document.querySelectorAll('[data-checkpoint]')];
  const updateChecks = () => {
    document.getElementById('checkpoint-count').textContent = `${checks.filter(input => input.checked).length} / ${checks.length} checkpoints`;
  };
  checks.forEach(input => {
    input.checked = safelyRead(`${storagePrefix}:${input.dataset.checkpoint}`) === 'true';
    input.addEventListener('change', () => {
      safelyWrite(`${storagePrefix}:${input.dataset.checkpoint}`, String(input.checked));
      updateChecks();
    });
  });
  updateChecks();
  document.querySelectorAll('[data-code]').forEach(button => {
    button.addEventListener('click', async () => {
      const text = document.getElementById(button.dataset.code).textContent;
      try {
        if (navigator.clipboard && window.isSecureContext) {
          await navigator.clipboard.writeText(text);
        } else {
          const area = document.createElement('textarea');
          area.value = text;
          area.style.position = 'fixed';
          area.style.opacity = '0';
          document.body.append(area);
          area.select();
          const copied = document.execCommand('copy');
          area.remove();
          if (!copied) throw new Error('Copy unavailable');
        }
        button.textContent = 'Copied';
        document.getElementById('copy-status').textContent = 'Code copied without line numbers.';
        window.setTimeout(() => { button.textContent = 'Copy code'; }, 1800);
      } catch {
        button.textContent = 'Select code to copy';
        document.getElementById('copy-status').textContent = 'Automatic copying is unavailable. Select the code and copy it manually.';
      }
    });
  });
  const progress = document.getElementById('reading-progress');
  const updateProgress = () => {
    const distance = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.width = `${distance > 0 ? Math.min(100, Math.max(0, window.scrollY / distance * 100)) : 100}%`;
  };
  window.addEventListener('scroll', updateProgress, { passive: true });
  window.addEventListener('resize', updateProgress);
  updateProgress();
  const nav = [...document.querySelectorAll('.sidebar nav a')];
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) nav.forEach(link => link.classList.toggle('active', link.hash === `#${entry.target.id}`));
      });
    }, { rootMargin: '0px 0px -65% 0px', threshold: 0 });
    document.querySelectorAll('article h2').forEach(heading => observer.observe(heading));
  }
})();
