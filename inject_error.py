c = open('index.html', 'r', encoding='utf-8').read()

script = """
<script>
window.addEventListener('error', function(e) {
    document.body.innerHTML = '<div style="color:red; background:white; position:fixed; z-index:9999; top:0; left:0; width:100%; padding:20px;">' + e.message + '<br>' + e.filename + ':' + e.lineno + '</div>' + document.body.innerHTML;
});
</script>
"""

# inject right after <head>
c = c.replace('<head>', '<head>\n' + script)
open('index.html', 'w', encoding='utf-8').write(c)
print('Error handler injected.')
