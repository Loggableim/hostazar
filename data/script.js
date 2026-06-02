/* ===== hostazar.com – Megapage JavaScript ===== */
(function () {
  'use strict';

  const CAT_COLORS = {
    gaming: { bg: 'rgba(76,175,80,0.2)', color: '#66bb6a' },
    webhosting: { bg: 'rgba(33,150,243,0.2)', color: '#64b5f6' },
    devops: { bg: 'rgba(255,152,0,0.2)', color: '#ffb74d' }
  };
  const CAT_LABELS = { gaming: 'Gaming', webhosting: 'Webhosting', devops: 'DevOps' };
  const CAT_EMOJI = { gaming: '🎮', webhosting: '🌐', devops: '⚙️' };
  const PAGE_SIZE = 12;

  let app = {
    catalog: [],
    filtered: [],
    currentPage: 1,
    searchTerm: '',
    activeCategory: 'all',
    gridEl: null,
    searchEl: null,
    filterEl: null,
    paginationEl: null,
    articleCountEl: null
  };

  /* ---- helpers ---- */
  function escapeHtml(s) {
    const d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  }

  function buildCard(a) {
    const catData = CAT_COLORS[a.category] || CAT_COLORS.gaming;
    const catLabel = CAT_LABELS[a.category] || a.category;
    const catEmoji = CAT_EMOJI[a.category] || '📄';
    const imgSrc = `/images/${a.image}`;
    return `
<article class="blog-card" data-slug="${escapeHtml(a.slug)}" data-category="${escapeHtml(a.category)}" data-tags="${escapeHtml(a.tags ? a.tags.join(',') : '')}">
  <a href="/artikel/${escapeHtml(a.slug)}.html" class="card-img-link">
    <div class="card-img">
      <img src="${imgSrc}" alt="${escapeHtml(a.title)}" loading="lazy" onerror="this.parentElement.innerHTML='<span class=\\'placeholder-icon\\'>${catEmoji}</span>'">
    </div>
  </a>
  <div class="card-body">
    <div class="card-meta">
      <span class="card-tag ${escapeHtml(a.category)}" style="background:${catData.bg};color:${catData.color}">${catLabel}</span>
      <span>${a.date || '2026'}</span>
      ${a.readingTime ? `<span>· ${a.readingTime} Min</span>` : ''}
    </div>
    <h3><a href="/artikel/${escapeHtml(a.slug)}.html">${escapeHtml(a.title)}</a></h3>
    <p class="card-excerpt">${escapeHtml(a.excerpt ? a.excerpt.substring(0, 150) + (a.excerpt.length > 150 ? '…' : '') : '')}</p>
    <div class="card-footer">
      <span class="read-more"><a href="/artikel/${escapeHtml(a.slug)}.html">Weiterlesen →</a></span>
    </div>
  </div>
</article>`;
  }

  function renderCards() {
    if (!app.gridEl) return;
    const start = (app.currentPage - 1) * PAGE_SIZE;
    const page = app.filtered.slice(start, start + PAGE_SIZE);
    app.gridEl.innerHTML = page.length ? page.map(buildCard).join('') :
      '<div class="no-results"><p>😕 Keine Artikel gefunden. <a href="#" class="search-reset-link">Filter zurücksetzen</a></p></div>';
    renderPagination();

    // Bind reset link
    const resetLink = app.gridEl.querySelector('.search-reset-link');
    if (resetLink) resetLink.addEventListener('click', function (e) { e.preventDefault(); app.resetFilters(); });
  }

  function renderPagination() {
    const el = app.paginationEl;
    if (!el) return;
    const total = Math.ceil(app.filtered.length / PAGE_SIZE);
    if (total <= 1) { el.innerHTML = ''; return; }
    let html = '<div class="pagination">';
    if (app.currentPage > 1) {
      html += `<a href="#" data-page="${app.currentPage - 1}" class="page-btn prev">‹ Zurück</a>`;
    }
    for (let i = 1; i <= total; i++) {
      if (i === app.currentPage) {
        html += `<span class="page-btn active">${i}</span>`;
      } else if (i === 1 || i === total || Math.abs(i - app.currentPage) <= 2) {
        html += `<a href="#" data-page="${i}" class="page-btn">${i}</a>`;
      } else if (Math.abs(i - app.currentPage) === 3) {
        html += `<span class="page-dots">…</span>`;
      }
    }
    if (app.currentPage < total) {
      html += `<a href="#" data-page="${app.currentPage + 1}" class="page-btn next">Weiter ›</a>`;
    }
    html += '</div>';
    el.innerHTML = html;

    el.querySelectorAll('.page-btn[data-page]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        app.goToPage(parseInt(this.dataset.page));
      });
    });

    updateArticleCount();
  }

  function updateArticleCount() {
    if (!app.articleCountEl) return;
    const total = app.filtered.length;
    const showing = Math.min(PAGE_SIZE, total);
    const start = (app.currentPage - 1) * PAGE_SIZE + 1;
    app.articleCountEl.innerHTML = `<span class="result-count">${total} Artikel${app.searchTerm || app.activeCategory !== 'all' || app.activeTag ? ` gefunden (zeige ${start}–${Math.min(start + PAGE_SIZE - 1, total)})` : ''}</span>`;
  }

  /* ---- search ---- */
  function doSearch() {
    const q = app.searchEl ? app.searchEl.value.trim().toLowerCase() : '';
    app.searchTerm = q;
    applyFilters();
  }

  function applyFilters() {
    let list = app.catalog;

    // category filter
    if (app.activeCategory !== 'all') {
      list = list.filter(function (a) { return a.category === app.activeCategory; });
    }

    // tag filter
    if (app.activeTag) {
      list = list.filter(function (a) { return a.tags && a.tags.some(function (t) { return t.toLowerCase() === app.activeTag.toLowerCase(); }); });
    }

    // search
    if (app.searchTerm) {
      const q = app.searchTerm;
      list = list.filter(function (a) {
        return (a.title && a.title.toLowerCase().indexOf(q) !== -1) ||
          (a.excerpt && a.excerpt.toLowerCase().indexOf(q) !== -1) ||
          (a.tags && a.tags.some(function (t) { return t.toLowerCase().indexOf(q) !== -1; }));
      });
    }

    app.filtered = list;
    app.currentPage = 1;
    renderCards();
    updateFilterPills();
  }

  function updateFilterPills() {
    // Update category pills
    document.querySelectorAll('.cat-pill').forEach(function (p) {
      p.classList.toggle('active', p.dataset.cat === app.activeCategory);
    });
    // Update tag pills if any
    document.querySelectorAll('.tag-pill').forEach(function (p) {
      p.classList.toggle('active', p.dataset.tag === app.activeTag);
    });
  }

  /* ---- tag cloud ---- */
  function renderTagCloud(containerId) {
    const el = document.getElementById(containerId);
    if (!el || !app.catalog.length) return;
    const tagCounts = {};
    app.catalog.forEach(function (a) {
      if (a.tags) a.tags.forEach(function (t) {
        const key = t.trim().toLowerCase();
        if (key) tagCounts[key] = (tagCounts[key] || 0) + 1;
      });
    });
    // Sort by frequency
    const sorted = Object.keys(tagCounts).sort(function (a, b) { return tagCounts[b] - tagCounts[a]; });
    const top = sorted.slice(0, 20);
    if (!top.length) { el.innerHTML = ''; return; }
    el.innerHTML = '<div class="tag-cloud">' + top.map(function (t) {
      const count = tagCounts[t];
      return `<a href="#" class="tag-pill" data-tag="${escapeHtml(t)}" data-count="${count}">${escapeHtml(t)} (${count})</a>`;
    }).join('') + '</div>';
    el.querySelectorAll('.tag-pill').forEach(function (pill) {
      pill.addEventListener('click', function (e) {
        e.preventDefault();
        const tag = this.dataset.tag;
        app.activeTag = app.activeTag === tag ? '' : tag;
        applyFilters();
      });
    });
  }

  /* ---- related articles ---- */
  function renderRelated(containerId, category, excludeSlug, count) {
    count = count || 3;
    const el = document.getElementById(containerId);
    if (!el || !app.catalog.length) { if (el) el.style.display = 'none'; return; }
    let pool = app.catalog.filter(function (a) {
      return a.category === category && a.slug !== excludeSlug;
    });
    if (!pool.length) {
      pool = app.catalog.filter(function (a) { return a.slug !== excludeSlug; });
    }
    pool.sort(function () { return 0.5 - Math.random(); });
    const items = pool.slice(0, count);
    if (!items.length) { el.style.display = 'none'; return; }
    el.style.display = 'block';
    el.innerHTML = '<h2 class="related-heading">📖 Weiterlesen</h2><div class="related-grid">' +
      items.map(function (a) {
        const catData = CAT_COLORS[a.category] || CAT_COLORS.gaming;
        const catLabel = CAT_LABELS[a.category] || a.category;
        return `
<article class="blog-card related-card">
  <a href="/artikel/${escapeHtml(a.slug)}.html" class="card-img-link">
    <div class="card-img" style="height:160px">
      <img src="/images/${escapeHtml(a.image)}" alt="${escapeHtml(a.title)}" loading="lazy" onerror="this.parentElement.innerHTML='<span class=\\'placeholder-icon\\' style=\\'font-size:2rem\\'>📄</span>'">
    </div>
  </a>
  <div class="card-body" style="padding:14px">
    <div class="card-meta"><span class="card-tag ${escapeHtml(a.category)}" style="background:${catData.bg};color:${catData.color}">${catLabel}</span><span>${a.date || ''}</span></div>
    <h3 style="font-size:1rem"><a href="/artikel/${escapeHtml(a.slug)}.html">${escapeHtml(a.title)}</a></h3>
  </div>
</article>`;
      }).join('') + '</div>';
  }

  /* ---- breadcrumbs ---- */
  function renderBreadcrumbs(items) {
    const el = document.getElementById('breadcrumbs');
    if (!el) return;
    let html = '<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Startseite</a>';
    items.forEach(function (item) {
      if (item.url) {
        html += `<span class="sep">›</span><a href="${item.url}">${escapeHtml(item.label)}</a>`;
      } else {
        html += `<span class="sep">›</span><span class="current">${escapeHtml(item.label)}</span>`;
      }
    });
    html += '</nav>';
    el.innerHTML = html;
  }

  /* ---- public API ---- */
  app.init = function (config) {
    if (!config || !config.gridId) return;
    app.gridEl = document.getElementById(config.gridId);
    app.searchEl = config.searchId ? document.getElementById(config.searchId) : null;
    app.filterEl = config.filterId ? document.getElementById(config.filterId) : null;
    app.paginationEl = config.paginationId ? document.getElementById(config.paginationId) : null;
    app.articleCountEl = config.articleCountId ? document.getElementById(config.articleCountId) : null;
    if (config.defaultCategory) app.activeCategory = config.defaultCategory;

    // Load data
    var xhr = new XMLHttpRequest();
    var self = this;
    xhr.open('GET', '/data/artikel.json', true);
    xhr.onload = function () {
      if (xhr.status === 200) {
        try {
          app.catalog = JSON.parse(xhr.responseText);
          app.filtered = app.catalog.slice();
          renderCards();
          if (app.searchEl) {
            var debounceTimer;
            app.searchEl.addEventListener('input', function () {
              clearTimeout(debounceTimer);
              debounceTimer = setTimeout(function () { doSearch(); }, 250);
            });
          }
          if (config.tagCloudId) renderTagCloud(config.tagCloudId);
          if (config.relatedConfig) {
            renderRelated(
              config.relatedConfig.containerId,
              config.relatedConfig.category,
              config.relatedConfig.excludeSlug,
              config.relatedConfig.count
            );
          }
          if (config.breadcrumbs) renderBreadcrumbs(config.breadcrumbs);
          // Bind category pills
          document.querySelectorAll('.cat-pill').forEach(function (p) {
            p.addEventListener('click', function (e) {
              e.preventDefault();
              app.activeCategory = this.dataset.cat;
              app.activeTag = '';
              applyFilters();
            });
          });
          // Reset link in search
          var resetBtn = document.getElementById('search-reset');
          if (resetBtn) resetBtn.addEventListener('click', function (e) { e.preventDefault(); app.resetFilters(); });
        } catch (e) { console.error('hostazar: JSON parse error', e); }
      }
    };
    xhr.onerror = function () { console.error('hostazar: failed to load artikel.json'); };
    xhr.send();
  };

  app.resetFilters = function () {
    app.searchTerm = '';
    app.activeCategory = 'all';
    app.activeTag = '';
    if (app.searchEl) app.searchEl.value = '';
    app.filtered = app.catalog.slice();
    app.currentPage = 1;
    renderCards();
    updateFilterPills();
  };

  app.goToPage = function (n) {
    if (n < 1 || n > Math.ceil(app.filtered.length / PAGE_SIZE)) return;
    app.currentPage = n;
    renderCards();
    if (app.gridEl) { window.scrollTo({ top: app.gridEl.offsetTop - 100, behavior: 'smooth' }); }
  };

  app.filterByTag = function (tag) {
    app.activeTag = app.activeTag === tag ? '' : tag;
    applyFilters();
  };

  window.hostazarApp = app;
})();
