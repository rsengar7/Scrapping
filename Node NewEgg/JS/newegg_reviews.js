const puppeteer = require('puppeteer');
const axios = require('axios');
const fs = require('fs');
const csvWriter = require('csv-writer').createObjectCsvWriter;
const path = require('path');

// Arrays to store scraped data
let product_url = [];
let Rating = [];
let InDate = [];
let Title = [];
let DisplayName = [];
let EncryCustomerNumber = [];
let Comments = [];
let Pros = [];
let Cons = [];

// Read the existing CSV file to get URLs
const urlsFile = 'urls.csv';
const doneFile = 'Data/merged_file.csv';

async function main() {
    const doneUrls = new Set(); // Track already processed URLs

    // Read already processed URLs from merged_file.csv
    if (fs.existsSync(doneFile)) {
        const doneData = fs.readFileSync(doneFile, 'utf8');
        doneData.split('\n').forEach(line => {
            const values = line.split(',');
            doneUrls.add(values[2]); // Add processed URL to the Set
        });
    }

    // Read the product URLs from urls.csv
    const values = fs.readFileSync(urlsFile, 'utf8').split('\n').map(line => line.split(','));

    // Launch Puppeteer
    const browser = await puppeteer.launch({ headless: false }); // Change to true if you want headless mode
    const page = await browser.newPage();

    let failed_urls = [];
    
    for (let row of values) {
        const productLink = row[2];

        if (!doneUrls.has(productLink)) {
            try {
                console.log(`Processing: ${productLink}`);
                await page.goto(productLink);
                await page.waitForTimeout(5000); // Wait for the page to load

                // Click on the 'Reviews' section
                await page.waitForSelector("div[text='Reviews']");
                await page.click("div[text='Reviews']");
                await page.waitForTimeout(20000); // Wait for reviews to load

                // Next Page button selector
                const nextPageButton = '//button[@title="Next Page"]';

                while (true) {
                    try {
                        const button = await page.$x(nextPageButton);
                        if (button.length > 0) {
                            const disabled = await button[0].evaluate(btn => btn.disabled);
                            if (disabled) {
                                console.log('Next Page button is disabled, stopping.');
                                break;
                            }
                            await button[0].click(); // Click Next Page
                            console.log('Clicked on the Next Page button');
                            await page.waitForTimeout(1000); // Short wait before next click
                        } else {
                            break;
                        }
                    } catch (err) {
                        console.error(`Error clicking next page: ${err.message}`);
                        failed_urls.push(productLink);
                        break;
                    }
                }

                // Intercept and capture network requests to the ProductReview API
                const requests = [];
                page.on('response', async (response) => {
                    const request = response.request();
                    if (request.url().startsWith("https://www.newegg.com/product/api/ProductReview")) {
                        const responseBody = await response.json();
                        const customerReviews = responseBody.SearchResult.CustomerReviewList;

                        for (let review of customerReviews) {
                            product_url.push(productLink);
                            Rating.push(review.Rating || '');
                            InDate.push(review.InDate || '');
                            Title.push(review.Title || '');
                            DisplayName.push(review.DisplayName || '');
                            EncryCustomerNumber.push(review.EncryCustomerNumber || '');
                            Comments.push(review.Comments || '');
                            Pros.push(review.Pros || '');
                            Cons.push(review.Cons || '');
                        }
                    }
                });

                console.log(`Captured reviews for: ${productLink}`);

                // Write the captured data into CSV
                const writer = csvWriter({
                    path: `Data/api_url_${index}.csv`,
                    header: [
                        { id: 'product_url', title: 'Product URL' },
                        { id: 'Rating', title: 'Rating' },
                        { id: 'InDate', title: 'In Date' },
                        { id: 'Title', title: 'Title' },
                        { id: 'DisplayName', title: 'Display Name' },
                        { id: 'EncryCustomerNumber', title: 'Customer Number' },
                        { id: 'Comments', title: 'Comments' },
                        { id: 'Pros', title: 'Pros' },
                        { id: 'Cons', title: 'Cons' }
                    ]
                });

                const dataToWrite = product_url.map((url, index) => ({
                    product_url: url,
                    Rating: Rating[index],
                    InDate: InDate[index],
                    Title: Title[index],
                    DisplayName: DisplayName[index],
                    EncryCustomerNumber: EncryCustomerNumber[index],
                    Comments: Comments[index],
                    Pros: Pros[index],
                    Cons: Cons[index]
                }));

                await writer.writeRecords(dataToWrite);
                console.log(`Data saved for product: ${productLink}`);

            } catch (err) {
                console.error(`Failed to process: ${productLink}, Error: ${err.message}`);
                failed_urls.push(productLink);
            }
        }
    }

    // Close the browser
    await browser.close();

    // Log any failed URLs
    if (failed_urls.length > 0) {
        console.log('Failed URLs: ', failed_urls);
        fs.writeFileSync('failed_urls.txt', failed_urls.join('\n'), 'utf8');
    }
}

// Start the process
main().catch(err => {
    console.error('Error: ', err.message);
});
