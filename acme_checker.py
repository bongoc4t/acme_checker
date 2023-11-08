# Import the dns.resolver module from the dnspython library
# This module will be used to query DNS records
import dns.resolver

# Define a function to get the CNAME record for a given domain
# specifically for the _acme-challenge subdomain used by Let's Encrypt
def get_cname(domain):
    try:
        # Resolve the CNAME record for the _acme-challenge subdomain of the given domain
        # The _acme-challenge subdomain is used for domain validation by ACME (Automated Certificate Management Environment)
        answers = dns.resolver.resolve('_acme-challenge.' + domain, 'CNAME')
        # If found, return the CNAME target as a text string
        return answers[0].target.to_text()
    # If there's no answer (NoAnswer) or a non-existent domain (NXDOMAIN) error,
    # it means there's no CNAME record set up for _acme-challenge
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        # Return None to indicate the absence of a CNAME record
        return None

# Define the main function that will be the entry point of the script
def main():
    # Open the file 'acme_list.txt' in read mode
    # This file is expected to contain a list of domains to check, one per line
    with open('acme_list.txt', 'r') as f:
        # Read the file and split it into a list of domain lines
        domains = f.read().splitlines()

    # Iterate over each domain in the list
    for domain in domains:
        # Get the CNAME record for the current domain
        cname = get_cname(domain)
        # If a CNAME record exists, print it out
        if cname:
            print(cname)
        # If no CNAME record exists, print a message indicating it's missing for this domain
        else:
            print(f"CNAME record missing for {domain}")

# Check if the script is being run directly (as opposed to being imported as a module)
if __name__ == "__main__":
    # If so, call the main function to start the script
    main()

