c = open('index.html', 'r', encoding='utf-8').read()

# Make background #050505 again so it matches the image's average dark edge
c = c.replace(
    '<div id="pantalla-login" class="fixed inset-0 bg-black z-[100] flex flex-col items-center justify-center p-4">',
    '<div id="pantalla-login" class="fixed inset-0 bg-[#050505] z-[100] flex flex-col items-center justify-center p-4">'
)

# Replace the logo image tag to be much bigger and have a radial mask to hide the box edges perfectly
old_img = '<img src="logo.png" alt="MB BarberOS" class="h-72 object-contain mix-blend-screen">'
new_img = '<img src="logo.png" alt="MB BarberOS" class="h-[400px] object-contain mix-blend-screen" style="-webkit-mask-image: radial-gradient(circle at center, black 40%, transparent 75%); mask-image: radial-gradient(circle at center, black 40%, transparent 75%);">'
c = c.replace(old_img, new_img)

open('index.html', 'w', encoding='utf-8').write(c)

# Cache bust
import time, re
c = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', c)
open('index.html', 'w', encoding='utf-8').write(c)

print('Logo masked and enlarged.')
