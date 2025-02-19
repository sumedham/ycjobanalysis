from bs4 import BeautifulSoup
from requests_html import HTMLSession
from collections import Counter
import csv
import time
import json
import requests
import re

# Technology keywords to search for
TECH_KEYWORDS = {"aws", "gcp", "azure", "kubernetes", "docker", "terraform", "ansible", "jenkins", "prometheus", "ec2",
                 "datadog", "newrelic", "splunk", "cloudformation", "helm", "pulumi", "ci/cd", "kafka", "rabbitmq",
                 "postgres", "mongodb", "redis", "elasticsearch", "fluentd", "grafana", "istio", "linkerd", "fargate", "cloudfront", "wasm"
                 "vault", "consul", "nomad", "serverless", "lambda", "step functions", "ecs", "eks", "aks", "cloudflare", "vercel","supabase", "cloud run", "cloud functions", "azure functions", "container apps"}

def extract_technologies(job_url):
    """Extract technology mentions from a job posting."""
    print(f"\nAnalyzing job posting at: {job_url}")
    response = requests.get(job_url)
    if response.status_code != 200:
        print(f"Error fetching job: {response.status_code}")
        return []
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all prose divs that contain job details
    prose_divs = soup.find_all('div', class_='prose max-w-none prose-p:mb-2')
    
    # Initialize list to store all text content
    full_text = []
    
    # Extract text from each prose div
    for div in prose_divs:
        # Get text from paragraphs
        paragraphs = div.find_all('p')
        for p in paragraphs:
            full_text.append(p.get_text())
            
        # Get text from list items
        list_items = div.find_all('li')
        for li in list_items:
            full_text.append(li.get_text())
            
        # Get text from strong/bold elements
        strong_elements = div.find_all('strong')
        for strong in strong_elements:
            full_text.append(strong.get_text())
    
    # Combine all text and convert to lowercase for matching
    full_text = ' '.join(full_text).lower()
    
    
    found_techs = []
    for tech in TECH_KEYWORDS:
        # Use word boundaries to avoid partial matches
        if re.search(r'\b' + tech + r'\b', full_text):
            found_techs.append(tech)
        
    return found_techs
        

def main():
    """Main execution function."""
    print("Starting job analysis...")
    tech_counter = Counter()
    job_technologies = []  # List to store job-specific technology findings
    
    # Read job URLs from CSV
    try:
        with open('jobs.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                job_url = row['url']
                job_title = row['title']
                print(f"\n{'='*50}")
                print(f"Analyzing job: {job_title}")
                print(f"URL: {job_url}")
                
                technologies = extract_technologies(job_url)
                if technologies:
                    tech_counter.update(technologies)
                    job_technologies.append({
                        'title': job_title,
                        'url': job_url,
                        'technologies': technologies
                    })
                   
                time.sleep(1)  # Be nice to their servers
    
        # Print overall technology statistics
        print(f"\n{'='*50}")
        print("OVERALL TECHNOLOGY STATISTICS")
        print(f"{'='*50}")
        if tech_counter:
            print(f"\nFound technologies across {len(job_technologies)} jobs:")
            for tech, count in tech_counter.most_common():
                print(f"{tech}: {count} mentions")
            
            # Save results to a new CSV
            with open('technology_analysis.csv', 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(['Technology', 'Mentions'])
                for tech, count in tech_counter.most_common():
                    writer.writerow([tech, count])
            print("\nResults saved to technology_analysis.csv")
        else:
            print("\nNo technologies found in any job listings")
            
    except FileNotFoundError:
        print("jobs.csv file not found!")

if __name__ == "__main__":
    main() 