c = open('index.html', 'r', encoding='utf-8').read()

# Replace font URL
c = c.replace(
    'family=Montserrat:wght@300;400;600;700&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&display=swap',
    'family=Inter:wght@300;400;500;600;700&display=swap'
)

# Replace Tailwind config
c = c.replace(
    "sans: ['Montserrat', 'sans-serif']",
    "sans: ['Inter', 'sans-serif']"
)

# Optional: Make text a bit brighter by replacing text-zinc-600 with text-zinc-400 in labels/headers where legibility is key
# Let's target some specific utility classes that are hard to read
c = c.replace('text-[10px] text-zinc-600', 'text-[10px] text-zinc-400')
c = c.replace('text-[11px] text-zinc-600', 'text-[11px] text-zinc-400 text-shadow-sm')
c = c.replace('text-xs text-zinc-600', 'text-xs text-zinc-400')

open('index.html', 'w', encoding='utf-8').write(c)
print("Font changed to Inter and contrast improved.")
