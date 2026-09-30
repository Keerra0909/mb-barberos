import re, time

html = open('index.html', 'r', encoding='utf-8').read()

# 1. Add CSS
old_style = """        ::-webkit-scrollbar-thumb:hover { background: #71717a; }
    </style>"""
new_style = """        ::-webkit-scrollbar-thumb:hover { background: #71717a; }
        html.light-theme { filter: invert(1) hue-rotate(180deg); }
        html.light-theme img { filter: invert(1) hue-rotate(180deg); }
    </style>"""
html = html.replace(old_style, new_style)

# 2. Add Theme Toggle Button to Tabs
old_tabs = """                <button id="tab-reportes" class="py-4 text-[11px] tracking-[0.15em] uppercase border-b border-transparent text-zinc-600 hover:text-zinc-300 transition-colors">
                    Administración
                </button>
            </div>
        </div>"""
new_tabs = """                <button id="tab-reportes" class="py-4 text-[11px] tracking-[0.15em] uppercase border-b border-transparent text-zinc-600 hover:text-zinc-300 transition-colors">
                    Administración
                </button>
                <button onclick="toggleTheme()" class="ml-auto text-zinc-400 hover:text-white transition-colors" title="Cambiar Tema">
                    <i class="fa-solid fa-circle-half-stroke"></i>
                </button>
            </div>
        </div>"""
html = html.replace(old_tabs, new_tabs)

# Bust cache
html = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', html)
open('index.html', 'w', encoding='utf-8').write(html)
sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

# 3. Add toggle logic to app.js
js = open('app.js', 'r', encoding='utf-8').read()
new_js_code = """
// TEMA CLARO/OSCURO
window.toggleTheme = function() {
    document.documentElement.classList.toggle('light-theme');
    localStorage.setItem('mb_theme', document.documentElement.classList.contains('light-theme') ? 'light' : 'dark');
};
if(localStorage.getItem('mb_theme') === 'light') {
    document.documentElement.classList.add('light-theme');
}
"""
js = js + "\n" + new_js_code
open('app.js', 'w', encoding='utf-8').write(js)
