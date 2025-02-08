import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import json
import time
from datetime import datetime
import os
from typing import List, Dict

class EbayMonitor:
    def __init__(self, search_terms: List[str], email_address: str):
        self.search_terms = search_terms
        self.email_address = email_address
        self.seen_items_file = "seen_items.json"
        self.seen_items = self.load_seen_items()
        
        # Email settings - replace with your email provider's SMTP settings
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.smtp_username = "lucpeloquin77@gmail.com"  # Sender email
        self.smtp_password = "your-app-password"     # Replace with your app password
        self.recipient_email = "flickowens@icloud.com"  # Recipient email
        
    def load_seen_items(self) -> Dict:
        """Load previously seen items from JSON file"""
        if os.path.exists(self.seen_items_file):
            with open(self.seen_items_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_seen_items(self):
        """Save seen items to JSON file"""
        with open(self.seen_items_file, 'w') as f:
            json.dump(self.seen_items, f)
    
    def fetch_ebay_listings(self, search_term: str) -> List[Dict]:
        """Fetch eBay listings for a given search term"""
        url = f"https://www.ebay.com/sch/i.html?_nkw={search_term}&_rss=1"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')
            
            listings = []
            for item in items:
                listing = {
                    'title': item.title.text,
                    'link': item.link.text,
                    'price': self.extract_price(item.title.text),
                    'pub_date': item.pubDate.text,
                    'search_term': search_term
                }
                listings.append(listing)
                
            return listings
            
        except requests.RequestException as e:
            print(f"Error fetching listings for '{search_term}': {e}")
            return []
    
    def extract_price(self, title: str) -> str:
        """Extract price from item title"""
        import re
        price_match = re.search(r'\$\d+(?:\.\d{2})?', title)
        return price_match.group(0) if price_match else 'N/A'
    
    def send_email(self, new_items: List[Dict]):
        """Send email notification for new items"""
        # Group items by search term
        items_by_term = {}
        for item in new_items:
            search_term = item['search_term']
            if search_term not in items_by_term:
                items_by_term[search_term] = []
            items_by_term[search_term].append(item)
        
        # Create email content
        subject = f"New eBay Items Found - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        body = f"Found {len(new_items)} new item(s) matching your search terms:\n\n"
        
        for search_term, items in items_by_term.items():
            body += f"\nSearch Term: '{search_term}'\n"
            body += f"{len(items)} new item(s) found:\n\n"
            
            for item in items:
                body += f"Title: {item['title']}\n"
                body += f"Price: {item['price']}\n"
                body += f"URL: {item['link']}\n"
                body += f"Listed: {item['pub_date']}\n"
                body += "-" * 50 + "\n"
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.smtp_username
        msg['To'] = self.email_address
        
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
        except Exception as e:
            print(f"Error sending email: {e}")
    
    def check_new_listings(self):
        """Check for new listings across all search terms"""
        new_items = []
        
        for search_term in self.search_terms:
            listings = self.fetch_ebay_listings(search_term)
            
            for item in listings:
                item_url = item['link']
                if item_url not in self.seen_items:
                    new_items.append(item)
                    self.seen_items[item_url] = {
                        'first_seen': datetime.now().isoformat(),
                        'title': item['title']
                    }
        
        if new_items:
            self.send_email(new_items)
            self.save_seen_items()
            print(f"Found {len(new_items)} new items. Email sent.")
        else:
            print("No new items found.")
    
    def run(self, check_interval: int = 300):
        """Run the monitor continuously"""
        print(f"Starting eBay monitor with {len(self.search_terms)} search terms...")
        print(f"Check interval: {check_interval} seconds")
        
        while True:
            print(f"\nChecking listings at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
            self.check_new_listings()
            time.sleep(check_interval)

if __name__ == "__main__":
    # Configuration
    SEARCH_TERMS = [
        "number (n)ine sneaker",
        "undercover scab",
        "vintage"
    ]
    EMAIL_ADDRESS = "your.email@example.com"
    CHECK_INTERVAL = 300  # 5 minutes
    
    # Create and run monitor
    monitor = EbayMonitor(SEARCH_TERMS, EMAIL_ADDRESS)
    monitor.run(CHECK_INTERVAL)
