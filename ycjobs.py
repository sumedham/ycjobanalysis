import csv
from bs4 import BeautifulSoup
import re

def extract_job_urls(html_file):
    """Extract job URLs and titles from the HTML file."""
    print("Extracting job URLs and titles from HTML file...")
    
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    # Find all job links that match the pattern /jobs/NUMBER
    jobs = []
    job_links = soup.find_all('a', href=re.compile(r'https://www\.workatastartup\.com/jobs/\d+|/jobs/\d+'))
    
    for link in job_links:
        href = link.get('href')
        title = link.get_text().strip()
        
        if href.startswith('/jobs/'):
            full_url = f"https://www.workatastartup.com{href}"
            jobs.append({'url': full_url, 'title': title})
        elif href.startswith('https://www.workatastartup.com/jobs/'):
            jobs.append({'url': href, 'title': title})
    
    # Remove duplicates while preserving order
    seen = set()
    unique_jobs = []
    for job in jobs:
        if job['url'] not in seen:
            seen.add(job['url'])
            unique_jobs.append(job)
    
    # Save to CSV
    with open('jobs.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['url', 'title'])
        writer.writeheader()
        for job in unique_jobs:
            writer.writerow(job)
    
    print(f"Found {len(unique_jobs)} jobs")
    print("Jobs saved to jobs.csv")
    return unique_jobs

if __name__ == "__main__":
    extract_job_urls('myhtml.html')
