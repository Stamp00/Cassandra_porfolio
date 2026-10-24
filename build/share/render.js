// Renders card.html to assets/img/share.jpg. Run from the repo root: node build/share/render.js
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  await page.goto('file://' + path.resolve(__dirname, 'card.html'), { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.resolve(__dirname, '../../assets/img/share.jpg'), type: 'jpeg', quality: 88 });
  await browser.close();
})();
