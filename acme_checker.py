import dns.resolver

# Define a resolver instance globally to reuse for all queries
resolver = dns.resolver.Resolver()

def get_cname(domain):
    try:
        # Query for the CNAME record
        cname_answer = resolver.resolve('_acme-challenge.' + domain, 'CNAME')
        cname = cname_answer[0].target.to_text()
        return cname

    except dns.resolver.NoAnswer:
        return None
    except dns.resolver.NXDOMAIN:
        return None
    except dns.resolver.NoNameservers:
        return None

def main():
    # Improved error handling when the file is not found or inaccessible
    try:
        with open('acme_list.txt', 'r') as f:
            domains = f.read().splitlines()
    except FileNotFoundError:
        print("The file 'acme_list.txt' was not found.")
        return
    except IOError as e:
        print(f"An error occurred while trying to read the file: {e}")
        return

    for domain in domains:
        cname = get_cname(domain)
        if cname:
            print(f"CNAME for _acme-challenge.{domain} is {cname}")
        else:
            print(f"CNAME record missing for _acme-challenge.{domain}")

if __name__ == "__main__":
    main()
