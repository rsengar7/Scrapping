const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const csvWriter = require('csv-writer').createObjectCsvWriter;

// Setup CSV Writer to save data
const csvWriterInstance = csvWriter({
  path: 'urls.csv',
  header: [
    { id: 'name', title: 'Names' },
    { id: 'url', title: 'Urls' },
  ],
});

(async () => {
  // Initialize Puppeteer browser
  const browser = await puppeteer.launch({
    headless: false, // Set to true if you want to run it headless
    args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage', '--start-maximized'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });

  let names = [];
  let urls = [];

  // Loop through pages
  for (let i = 1; i <= 20; i++) {
    const url = `https://www.newegg.com/p/pl?N=101702291&page=${i}`;
    console.log(`Navigating to: ${url}`);
    
    // Navigate to the page and wait until all content loads
    await page.goto(url, { waitUntil: 'networkidle2' });

    // Wait for the products to load by waiting for the selector
    await page.waitForSelector('a[title="View Details"]', { timeout: 10000 });

    // Scrape data (product names and URLs)
    const products = await page.$$eval('a[title="View Details"]', elements =>
      elements.map(el => ({
        name: el.textContent.trim(),
        url: el.href,
      }))
    );

    // Add the data to the arrays
    products.forEach(product => {
      names.push(product.name);
      urls.push(product.url);
      console.log(product.name, product.url);
      console.log('*'.repeat(100));
    });

    // Pause before scraping the next page
    // await page.waitForTimeout(5000);
    await new Promise(resolve => setTimeout(resolve, 5000));
  }

  // Save data to CSV
  const records = names.map((name, index) => ({ name, url: urls[index] }));
  await csvWriterInstance.writeRecords(records);
  console.log('Data saved to urls.csv');

  // Close the browser
  await browser.close();
})();
