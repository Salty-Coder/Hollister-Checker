# Hollister Stock Checker

A Python-based automated stock monitoring tool for Hollister products. This script continuously monitors specific product variants (color, size, etc.) and sends a Discord notification when the item become available with the desired variants.

## Features

- 🔍 **Real-time Stock Monitoring**: Continuously checks product availability at configurable intervals
- 🎨 **Color & Size Selection**: Interactive selection of product colors and sizes to monitor
- 📱 **Discord Notifications**: Sends webhook notifications when items come back in stock
- 🌐 **Auto Browser Opening**: Automatically opens the product page when stock is found
- 🤖 **Headless Operation**: Runs in the background without displaying browser windows
- 🍪 **Cookie Handling**: Automatically handles cookie consent popups

## Requirements

- Python 3.7+
- Chrome browser
- ChromeDriver (automatically managed by Selenium)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/salty-coder/Hollister-Checker.git
cd Hollister-Checker
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Discord Webhook Setup

1. Create a Discord webhook in your desired channel:
   - Go to your Discord server settings
   - Navigate to Integrations → Webhooks
   - Create a new webhook and copy the URL

2. Replace the webhook URL in `checker.py`:
```python
webhook_url = 'YOUR_DISCORD_WEBHOOK_URL_HERE'
```

## Usage

1. Run the script:
```bash
python checker.py
```

2. Follow the interactive prompts:
   - **Product URL**: Enter the Hollister product page URL
   - **Color Selection**: Choose from available colors using arrow keys
   - **Primary Size**: Select the primary size option (e.g., S, M, L, XL)
   - **Secondary Size**: Select secondary size if available (e.g., Regular, Tall)
   - **Check Interval**: Set how often to check for stock (in minutes)

3. The script will:
   - Start monitoring the specified product variant
   - Display status updates in the console
   - Send Discord notifications when stock is found
   - Automatically open the product page in your browser

## How It Works

1. **Web Scraping**: Uses Selenium WebDriver to navigate Hollister's website
2. **Element Detection**: Identifies product options by CSS selectors and data attributes
3. **Stock Checking**: Monitors the `data-variant` attribute to determine availability
4. **Notification System**: Sends rich Discord embeds with product information
5. **User Interaction**: Provides a clean console interface with status updates

## Example Output

```
Product URL: https://www.hollisterco.com/shop/us/p/example-product
🔍 Monitoring product: Example Hoodie

Choose a color to monitor
❯ Dark Grey
  Light Blue
  Black

Choose a primary option to monitor
❯ S
  M
  L
  XL

Check interval (in minutes): 5

🔍 Monitoring S x Regular every 5.0 minutes...

❌ Primary option S is out of stock. Retrying in 5 minutes...
❌ Primary option S is out of stock. Retrying in 5 minutes...
✅ S x Regular IS IN STOCK! Opening browser...
```

## Script Components

### Main Functions

- `getTitle()`: Extracts product name from the page
- `check_stock()`: Performs stock availability checks
- `sendWebhook()`: Sends Discord notifications
- `isOptionInStock()`: Determines if a specific size/color is available
- `chooseColor()` / `choosePrimary()`: Selects product options

### Configuration Options

- **Headless Mode**: Runs without visible browser windows
- **User Agent Spoofing**: Mimics real browser behavior
- **Automatic Logging Suppression**: Reduces console noise
- **Cookie Rejection**: Automatically handles privacy popups

## Troubleshooting

### Common Issues

1. **ChromeDriver Not Found**
   - Ensure Chrome browser is installed
   - Selenium automatically manages ChromeDriver

2. **Product Not Loading**
   - Check if the URL is valid and accessible
   - Increase the sleep delays in `check_stock()`

3. **Elements Not Found**
   - Hollister may have updated their website structure
   - Check CSS selectors in the script

4. **Discord Webhook Failed**
   - Verify webhook URL is correct
   - Check Discord server permissions

## Known problems

In recent Chromedriver versions, some warnings may get printed to the console, which cannot be prevented/disabled. This can sometimes make the questionary menus more challenging to navigate.

## Legal Notice

This tool is for educational purposes only. Please respect Hollister's terms of service and use responsibly. Don't overload their servers with excessive requests.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
