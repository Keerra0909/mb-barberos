const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', error => console.log('PAGE ERROR:', error.message));

  await page.goto('http://localhost:8080');
  await new Promise(r => setTimeout(r, 1000));

  // login as Admin
  await page.evaluate(() => {
     const btns = Array.from(document.querySelectorAll('button'));
     btns.find(b => b.innerText.includes('ADMINISTRADOR')).click();
  });
  
  await page.type('#pin-input', '9999');
  
  await page.evaluate(() => {
     const btns = Array.from(document.querySelectorAll('button'));
     btns.find(b => b.innerText.includes('ENTRAR')).click();
  });
  
  await new Promise(r => setTimeout(r, 1000));
  await page.click('#tab-reportes');
  await new Promise(r => setTimeout(r, 1000));
  
  await browser.close();
})();
